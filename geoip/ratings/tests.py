from django.test import TestCase

from ratings.models import IpEvents, Rating
from ratings.query_manager import get_rating, get_ips_by_bssid, get_ips_by_ssid

from api.models import GeoIP

BSSID = "testbssid"
SSID = "testssid"
LAT = 42.3557695
LNG = -71.0985843
IP = '127.0.0.1'


class EntityValueTestCase(TestCase):

    def setUp(self):
        data = {
            'date': 16000,
            'ip': IP,
            'spam_count': 1,
            'spam_freq': 1,
            'bot_count': 1,
            'bot_freq': 1,
            'unexp_count': 1,
            'unexp_freq': 1,
        }
        IpEvents.objects.create(**data)

    def test_total_freq(self):
        ev = IpEvents.objects.get(date=16000, ip="127.0.0.1")
        self.assertEqual(ev.total_freq(), 3)

    def test_total_count(self):
        ev = IpEvents.objects.get(date=16000, ip="127.0.0.1")
        self.assertEqual(ev.total_count(), 3)


class RatingTest(TestCase):

    def test_basic_get_rating(self):
        created = Rating.objects.create(raw_score=55, bssid=BSSID)
        retrieved = get_rating(BSSID)
        self.assertEqual(created, retrieved)

    def test_get_ips_by_bssid(self):
        GeoIP.objects.create(bssid=BSSID, lat=0, lng=0,
                             ip=IP, remote_addr=IP)
        retrieved = get_ips_by_bssid(BSSID)
        self.assertEqual([IP], retrieved)

    def test_get_ips_by_ssid(self):
        GeoIP.objects.create(ssid=SSID, lat=LAT, lng=LNG,
                             ip=IP, remote_addr=IP)
        retrieved = get_ips_by_ssid(SSID, LAT, LNG)
        self.assertEqual([IP], retrieved)
