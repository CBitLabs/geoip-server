from django.core.management.base import NoArgsCommand

from api.models import GeoIP
from api.util import _reverse_geo
import api.constants as constants


class Command(NoArgsCommand):

    """
        Command is used to help add loaction information
         when we are rate limited by the Google API. Location is 
         displayed as part of the history object, not mission critical 
         if it's missing
    """
    help = "Add location to objects. Runs as daily cron."

    def handle(self, **options):
        self.stdout.write('Beginning update...\n')

        objs = GeoIP.objects.all()
        count = constants.QUERY_LIMIT_AMOUNT

        for index, obj in enumerate(objs):

            if count == 0:
                self.stdout.write("Exceeded query amount")
                break

            if self.should_update(obj):
                obj.loc = _reverse_geo(obj.lat, obj.lng)
                obj.save()
                if obj.loc != constants.NO_LOC:
                    count -= 1
                elif obj.loc == constants.QUERY_LIMIT:
                    count = 0

            if index > 0 and not index % 100:
                self.stdout.write("Updated %d entries" % index)

    def should_update(obj):
        has_lat = obj.lat != 0 and obj.lng != 0
        valid_type = obj.loc == constants.NO_LOC \
            and obj.datasrc != constants.SCAN
        return has_lat and valid_type
