from django.db import models

from api.constants import NO_LOC, NO_SEC

from ratings.models import Rating
from ratings.util import get_clean_rating_dict

from common.models import Base

import datetime
import humanize


class GeoIP(Base):

    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)
    loc = models.CharField(max_length=300, default=NO_LOC)

    bssid = models.CharField(max_length=80, default="", db_index=True)
    ssid = models.CharField(max_length=80, default="", db_index=True)
    uuid = models.CharField(max_length=80, default="")

    security = models.CharField(max_length=80, default=NO_SEC)
    isEnterprise = models.BooleanField(default=False)

    remote_addr = models.GenericIPAddressField()
    ip = models.GenericIPAddressField()

    datasrc = models.CharField(max_length=80, default="")
    created_at = models.DateTimeField(default=datetime.datetime.utcnow)

    rating = models.ForeignKey(Rating, null=True)

    def as_clean_dict(self):
        as_dict = self.as_dict()

        transforms = [
            ('created_at_human', lambda geoip:
             humanize.naturaltime(geoip['created_at'].replace(tzinfo=None))),
            ('created_at', lambda geoip:
             str(geoip['created_at'])),
            ('rating', lambda geoip: get_clean_rating_dict(geoip['rating']))
        ]

        import util
        util.apply_transforms(transforms, as_dict)
        return as_dict
