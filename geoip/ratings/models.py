from django.db import models
from adaptor.model import CsvDbModel

import datetime


class EntityValue(models.Model):

    """
        Model to hold data pulled from EntityValues table
        via ip_stats hadoop job. Updated daily and queried
        to build a rating object.
    """

    date = models.IntegerField()
    address = models.GenericIPAddressField()
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
            self.address, self.total_count, self.total_freq)


class EntityValueCSV(CsvDbModel):

    """
        used to extract data from csv
    """
    class Meta:
        dbModel = EntityValue
        delimiter = ","


class Rating(models.Model):

    """
        TODO: tweak fields
    """

    raw_score = models.IntegerField()
    bssid = models.CharField(max_length=80, default="")

    created_at = models.DateTimeField(default=datetime.datetime.utcnow)

    def __unicode__(self):
        return "score: %d, bssid: %s" % (self.raw_score, self.bssid)
