from django.core.management.base import NoArgsCommand

from api.models import GeoIP
from api.util import _reverse_geo
from api.constants import NO_LOC, QUERY_LIMIT_AMOUNT, QUERY_LIMIT


class Command(NoArgsCommand):
    help = "One time data dump of old dns query data"

    def handle(self, **options):
        self.stdout.write('Beginning update...\n')

        objs = GeoIP.objects.all()
        count = QUERY_LIMIT_AMOUNT

        for index, obj in enumerate(objs):

            if count == 0:
                self.stdout.write("Exceeded query amount")
                break

            if obj.lat != 0 and obj.lng != 0 and obj.loc == NO_LOC:
                obj.loc = _reverse_geo(obj.lat, obj.lng)
                obj.save()
                if obj.loc != NO_LOC:
                    count -= 1
                elif obj.loc == QUERY_LIMIT:
                    count = 0

            if index > 0 and not index % 100:
                self.stdout.write("Updated %d entries" % index)
