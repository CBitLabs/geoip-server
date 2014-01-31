from django.core.management.base import BaseCommand

import api.util as util

import csv
import glob
import fileinput
import datetime

IN_FILE = "*.csv"
FIELDS = ["created_at", "srcip", "qname"]

DNS_EXPR_OLD = r"(?P<resolver>[sd]{1})\.(?P<lat>%(float)s)\.(?P<lng>%(float)s)\.(?P<ssid>%(ssid)s)\.(?P<bssid>\w+)\..*" % util.EXPRS


class Command(BaseCommand):
    help = "One time data dump of old dns query data"
    args = "filepath"

    def handle(self, *args, **options):
        self.stdout.write('Beginning update...\n')
        assert(len(args) == 1)
        filepath = "%s/%s" % (args[0], IN_FILE)

        self.stdout.write("Looking for data in %s" % filepath)

        inp = fileinput.input(glob.glob(filepath))
        reader = csv.DictReader(inp, fieldnames=FIELDS)

        for index, line in enumerate(reader):
            geoip = self.extract_record(line)
            if util.is_valid(geoip):
                datasrc = util.get_datasrc(geoip)
                geoip = util.process_res(
                    None, geoip, datasrc, remote_addr=line["srcip"])

            if not index % 100:
                self.stdout.write("Updated %d entries" % index)

        self.stdout.write(
            'Update complete')

    def extract_record(self, line):

        geoip = util.parse_dns(line)
        if not util.is_valid(geoip):
            geoip = util.parse_dns(line, DNS_EXPR_OLD)
            geoip["ip"] = line["srcip"]
            geoip["created_at"] = self.extract_datetime(line)

        return geoip

    def extract_datetime(self, line):
        return datetime.datetime.fromtimestamp(int(line["created_at"]))
