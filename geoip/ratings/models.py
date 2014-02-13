from django.db import models

from ratings.util import get_epoch_days

import datetime


class IpEvents(models.Model):

    """
        Model to hold data pulled from EntityValues table
        via ip_stats hadoop job. Updated daily and queried
        to build a rating object.
    """

    date = models.IntegerField(db_index=True)
    ip = models.GenericIPAddressField(db_index=True)
    spam_count = models.IntegerField()
    spam_freq = models.IntegerField()
    bot_count = models.IntegerField()
    bot_freq = models.IntegerField()
    unexp_count = models.IntegerField()
    unexp_freq = models.IntegerField()

    def total_count(self):
        return sum(self._get_vals("count"))

    def total_freq(self):
        return sum(self._get_vals("freq"))

    def _get_vals(self, keyword):
        return map(lambda name: getattr(self, name), self._get_fields(keyword))

    def _get_fields(self, keyword):
        return [field.name
                for field in self._meta.fields
                if keyword in field.name]

    def __unicode__(self):
        return "Ip: %s, total count: %d, total freq: %d" % (
            self.ip, self.total_count(), self.total_freq())


class Rating(models.Model):

    """
        TODO: tweak fields
    """
    date = models.IntegerField(default=get_epoch_days, db_index=True)
    raw_score = models.IntegerField()
    bssid = models.CharField(max_length=80, default="", db_index=True)

    created_at = models.DateTimeField(default=datetime.datetime.utcnow)

    def as_clean_dict(self):
        return {
            'raw_score': self.raw_score,
            'bssid': self.bssid,
        }

    def __unicode__(self):
        return "score: %d, bssid: %s" % (self.raw_score, self.bssid)
