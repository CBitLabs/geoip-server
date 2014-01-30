from django.db import models

from pygeocoder import Geocoder, GeocoderError

from api.constants import NO_LOC

import util
import datetime
import humanize


class GeoIP(models.Model):

    lat = models.FloatField()
    lng = models.FloatField()
    loc = models.CharField(max_length=300, default=NO_LOC)

    bssid = models.CharField(max_length=80, default="")
    ssid = models.CharField(max_length=80, default="")
    uuid = models.CharField(max_length=80, default="")

    ip = models.GenericIPAddressField()
    remote_addr = models.GenericIPAddressField()

    datasrc = models.CharField(max_length=80, default="")
    created_at = models.DateTimeField(default=datetime.datetime.utcnow())

    def as_dict(self):
        return {field.name: getattr(self, field.name)
                for field in self._meta.fields}

    @staticmethod
    def _reverse_geo(lat, lng):
        try:
            return Geocoder.reverse_geocode(lat, lng).formatted_address
        except GeocoderError:
            return NO_LOC

    def as_clean_dict(self):
        as_dict = self.as_dict()

        transforms = [
            ('created_at_human', lambda geoip:
             humanize.naturaltime(geoip['created_at'].replace(tzinfo=None))),
            ('created_at', lambda geoip:
             str(geoip['created_at'])),
        ]

        util.apply_transforms(transforms, as_dict)
        return as_dict

    def __unicode__(self):
        return str(self.as_dict())
