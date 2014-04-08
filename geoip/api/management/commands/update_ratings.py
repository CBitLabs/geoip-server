"""
    USE WITH CAUTION.
    Will overwrite any GeoIp objects with a new rating.
    Use if the scoring algorithm is changed or you want to
    change the score of past item.
"""

from django.core.management.base import NoArgsCommand

from api.models import GeoIP
from ratings.query_manager import rating_manager


class Command(NoArgsCommand):

    help = "One time data dump of old dns query data"

    def handle(self, **options):
        self.stdout.write('Beginning update...\n')

        objs = GeoIP.objects.all()

        for index, geoip in enumerate(objs):

            rating = rating_manager(
                geoip.ip, bssid=geoip.bssid, ssid=geoip.ssid,
                lat=geoip.lat, lng=geoip.lng, use_cache=False)
            geoip.rating_id = rating.id
            geoip.save()

            if index > 0 and not index % 100:
                self.stdout.write("Updated %d entries" % index)
