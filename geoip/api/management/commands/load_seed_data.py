from django.core.management.base import BaseCommand

from api.models import GeoIP
import api.util as util

import csv
import glob
import fileinput

IN_FILE = "*.csv"
FIELDS = ["timestamp", "srcip", "qname"]

DNS_EXPR_OLD = r"(?P<resolver>[sd]{1})\.(?P<lat>%(float)s)\.(?P<lng>%(float)s)\.(?P<ssid>%(ssid)s)\.(?P<bssid>\w+)\..*" % util.EXPRS


class Command(BaseCommand):
    help = "One time data dump of old dns query data"
    args = "filepath"

    def handle(self, *args, **options):
        self.stdout.write('Beginning update...\n')
        assert(len(args) == 1)
        filepath = "%s/%s" % (args[0], IN_FILE)

        self.stdout.write("Looking for data in %s" % filepath)
        valid = 0
        invalid = 0

        inp = fileinput.input(glob.glob(filepath))
        reader = csv.DictReader(inp, fieldnames=FIELDS)

        for line in reader:
            geoip = self.extract_record(line)
            if util.is_valid(geoip):
                valid += 1
            else:
                print line
                invalid += 1

        self.stdout.write(
            'Update complete. valid: %d, invalid: %d.\n' % (valid, invalid))

    def extract_record(self, line):

        geoip = util.parse_dns(line, DNS_EXPR_OLD)
        if not util.is_valid(geoip):
            geoip = util.parse_dns(line)

        return geoip
