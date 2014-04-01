from django.core.management.base import NoArgsCommand

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from retrying import retry

from geoip.config import AWS
from ratings.constants import FILENAME


class Command(NoArgsCommand):
    help = "Daily cron to download the results of the hadoop job from S3"

    def handle(self, **options):
        c = S3Connection(AWS['ACCESS_KEY'], AWS['SECRET_KEY'])
        bucket = AWS['BUCKET']
        key = AWS['KEY']

        self.stdout.write("Connected to S3")

        b = c.get_bucket(bucket)
        self.download_file(b, key)

    @retry(wait='exponential_sleep',
           wait_exponential_multiplier=1000,
           wait_exponential_max=60 * 60 * 1000)
    def download_file(self, bucket, key):
        k = Key(bucket)
        k.key = key
        success = k.exists()

        if success:
            k.get_contents_to_filename(FILENAME)
            msg = "Success! Downloaded ip-stats file."
            k.delete()

        else:
            msg = "Key missing, retrying."

        self.stdout.write(msg)

        return success
