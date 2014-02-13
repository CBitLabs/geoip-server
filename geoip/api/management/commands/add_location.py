from django.core.management.base import NoArgsCommand

from api.models import GeoIP
from api.util import _reverse_geo
from api.constants import NO_LOC


class Command(NoArgsCommand):
    help = "One time data dump of old dns query data"

    def handle(self, **options):
        self.stdout.write('Beginning update...\n')

        objs = GeoIP.objects.all()

        for index, obj in enumerate(objs):

            if obj.lat != 0 and obj.lng != 0 and obj.loc == NO_LOC:
                obj.loc = _reverse_geo(obj.lat, obj.lng)
                obj.save()

            if index > 0 and not index % 100:
                self.stdout.write("Updated %d entries" % index)
