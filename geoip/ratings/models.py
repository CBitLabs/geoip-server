from django.db import models

from ratings.util import get_epoch_days
from ratings.constants import EVENTS

from common.models import Base

import datetime


class RatingBase(Base):

    """
        Rating object for data that comes out of BS pipeline.
    """
    spam_count = models.IntegerField(default=0)
    spam_freq = models.IntegerField(default=0)
    bot_count = models.IntegerField(default=0)
    bot_freq = models.IntegerField(default=0)
    unexp_count = models.IntegerField(default=0)
    unexp_freq = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def total_count(self):
        return sum(self._get_vals("count"))

    def total_freq(self):
        return sum(self._get_vals("freq"))

    def get_event_counts(self):
        return {k: v for k, v in
                zip(self._get_fields(EVENTS), self._get_vals(EVENTS))}

    def _get_vals(self, keywords):
        return map(lambda name: getattr(self, name), self._get_fields(keywords))

    def _get_fields(self, keywords):
        if not isinstance(keywords, list):
            keywords = [keywords]
        fields = []
        for field in self._meta.fields:
            name = field.name
            for keyword in keywords:
                if keyword in name:
                    fields.append(name)
        return fields


class IpEvent(RatingBase):

    """
        Model to hold data pulled from EntityValues table
        via ip_stats hadoop job. Updated daily and queried
        to build a rating object.
    """

    date = models.IntegerField(db_index=True)
    ip = models.GenericIPAddressField(db_index=True)

    def __unicode__(self):
        return "Ip: %s, total count: %d, total freq: %d" % (
            self.ip, self.total_count(), self.total_freq())


class Rating(RatingBase):

    """
        Object to hold rating information, keyed on bssid
    """
    date = models.IntegerField(default=get_epoch_days, db_index=True)
    bssid = models.CharField(max_length=80, default="", db_index=True)

    raw_score = models.IntegerField()
    is_infected = models.BooleanField(default=False)
    # flag to say if we have a rating at all
    is_valid = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=datetime.datetime.utcnow)

    def as_clean_dict(self):
        as_dict = self.as_dict()
        del as_dict['date']
        del as_dict['created_at']
        return as_dict

    def set_is_infected(self):
        """
            used to set the boolean field is_infected during save.
            subject to change as definition does.
        """
        return self.raw_score > 0

    def save(self, *args, **kwargs):
        self.is_infected = self.set_is_infected()

        super(Rating, self).save(*args, **kwargs)

    def __unicode__(self):
        return "score: %d, bssid: %s" % (self.raw_score, self.bssid)
