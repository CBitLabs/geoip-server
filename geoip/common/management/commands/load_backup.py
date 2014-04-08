from django.core.management.base import BaseCommand

from common.util import get_conn
import subprocess

SQL = """DROP DATABASE IF EXISTS geoip_bak;
    ALTER TABLE geoip RENAME geoip_bak;
    CREATE DATABASE geoip;
"""


class Command(BaseCommand):

    """
        Command to load a backup in case of failure or to 
        initilize a dev environment
    """
    help = "Load database file into local store"
    args = "filepath"

    def handle(self, *args, **options):
        self.stdout.write('Beginning update...\n')
        assert(len(args) == 1)

        filepath = args[0]
        self.setup_db()
        self.load_file(filepath)

        self.stdout.write('Update complete')

    def setup_db(self):
        conn = get_conn()
        conn.execute(SQL)

    def load_file(self, filepath):
        self.stdout.write("Loading file from %s" % filepath)
        cmd = "psql geoip < %s" % filepath
        subprocess.check_output([cmd])
