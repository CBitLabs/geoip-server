from django.core.management.base import NoArgsCommand

from common.utils import get_conn

import csv
import os


IN_FILE = "/tmp/ip-stats-dl.csv"
OUT_FILE = "/tmp/ip-stats.csv"

SQL = """CREATE TABLE ratings_ipevent_tmp (LIKE ratings_ipevent);
copy ratings_ipevent_tmp FROM '%(data_file)s' DELIMITER ',' CSV HEADER;

BEGIN;
DROP INDEX IF EXISTS addr_idx;
CREATE INDEX addr_idx ON ratings_ipevent_tmp (ip);
ALTER TABLE ratings_ipevent RENAME TO ratings_ipevent_old;
ALTER TABLE ratings_ipevent_tmp RENAME TO ratings_ipevent;
DROP TABLE ratings_ipevent_old;
COMMIT;
""" % {
    'data_file': OUT_FILE,
}


class Command(NoArgsCommand):
    help = "Daily cron to extra entity data and load into the django db"
    args = "filepath to data"

    def handle(self, **options):
        self._log('Beginning update...\n')

        self.add_id_col()
        self.load_data()
        self.cleanup()

        self._log('Update complete')

    def add_id_col(self):
        """
            insert an id column to the downloaded csv for postgres ingestion
        """
        self._log("Adding index column...")
        with open(IN_FILE) as f_in, open(OUT_FILE, 'w') as f_out:
            reader = csv.reader(f_in)
            writer = csv.writer(f_out)

            for index, line in enumerate(reader):
                new_row = [index]
                new_row.extend(line)
                writer.writerow(new_row)

                if index > 0 and not index % 100:
                    self._log("Wrote %d entries" % index)

    def load_data(self):
        self._log("Loading data...")
        conn = get_conn()
        conn.execute(SQL)

    def cleanup(self):
        self._log("Cleaning up...")
        os.remove(IN_FILE)
        os.remove(OUT_FILE)

    def _log(self, msg):
        self.stdout.write(msg)
