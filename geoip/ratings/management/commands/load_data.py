from django.core.management.base import NoArgsCommand

import csv
import shlex
import subprocess
import os

IN_FILE = "ip-stats-dl.csv"
OUT_FILE = "ip-stats.csv"
SCRIPT = "./load_data.sh"


class Command(NoArgsCommand):
    help = "Daily cron to extra entity value data and load it into the django db"
    args = "filepath to data"

    def handle(self, **options):
        self.stdout.write('Beginning update...\n')

        self.add_id_col()
        self.load_data()
        self.cleanup()

        self.stdout.write('Update complete')

    def add_id_col(self):
        """
            insert an id column to the downloaded csv for postgres ingestion
        """
        with open(IN_FILE) as f_in, open(OUT_FILE, 'w') as f_out:
            reader = csv.reader(f_in)
            writer = csv.writer(f_out)

            for index, line in enumerate(reader):
                new_row = [index]
                new_row.extend(line)
                writer.writerow(new_row)

                if index > 0 and not index % 100:
                    self.stdout.write("Added %d entries" % index)

    def load_data(self):
        cmd = "psql geoip < load_data.sql"
        subprocess.check_output(shlex.split(cmd),
                                stderr=subprocess.STDOUT)

    def cleanup(self):
        os.remove(IN_FILE)
        os.remove(OUT_FILE)
