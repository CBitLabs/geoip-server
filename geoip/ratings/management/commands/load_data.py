from django.core.management.base import NoArgsCommand

import csv
import subprocess
import os


IN_FILE = "/tmp/ip-stats-dl.csv"
OUT_FILE = "/tmp/ip-stats.csv"
PATH = os.path.dirname(os.path.realpath(__file__))
SCRIPT = "%s/load_data.sh" % PATH


class Command(NoArgsCommand):
    help = "Daily cron to extra entity value data and load it into the django db"
    args = "filepath to data"

    def handle(self, **options):
        self.log('Beginning update...\n')

        self.add_id_col()
        self.load_data()
        self.cleanup()

        self.log('Update complete')

    def add_id_col(self):
        """
            insert an id column to the downloaded csv for postgres ingestion
        """
        self.log("Adding index column...")
        with open(IN_FILE) as f_in, open(OUT_FILE, 'w') as f_out:
            reader = csv.reader(f_in)
            writer = csv.writer(f_out)

            for index, line in enumerate(reader):
                new_row = [index]
                new_row.extend(line)
                writer.writerow(new_row)

                if index > 0 and not index % 100:
                    self.log("Wrote %d entries" % index)

    def load_data(self):
        self.log("Loading data...")
        subprocess.check_output([SCRIPT],
                                stderr=subprocess.STDOUT)

    def cleanup(self):
        self.log("Cleaning up...")
        os.remove(IN_FILE)
        os.remove(OUT_FILE)

    def log(self, msg):
        self.stdout.write(msg)
