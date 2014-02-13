from django.test import TestCase

from ratings.models import IpEvents, Rating
from ratings.query_manager import rating_manager, get_ips_by_bssid, get_ips_by_ssid

from api.models import GeoIP

from common.constants import IP, BSSID, SSID, LAT, LNG


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
        ev = IpEvents.objects.get(date=16000, ip=IP)
        self.assertEqual(ev.total_freq(), 3)

    def test_total_count(self):
        ev = IpEvents.objects.get(date=16000, ip=IP)
        self.assertEqual(ev.total_count(), 3)


class RatingTest(TestCase):

    def test_basic_rating_manager(self):
        created = Rating.objects.create(raw_score=55, bssid=BSSID)
        retrieved = rating_manager(BSSID)
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

    def test_filter_by_dist(self):
        """
            test the filter on radius
        """
        # lat/lng outside of radius
        far_lat = LAT + 0.1
        far_lng = LNG + 0.1

        GeoIP.objects.create(ssid=SSID, lat=LAT, lng=LNG,
                             ip=IP, remote_addr=IP)

        GeoIP.objects.create(ssid=SSID, lat=far_lat, lng=far_lng,
                             ip=IP, remote_addr=IP)

        retrieved = get_ips_by_ssid(SSID, LAT, LNG)
        self.assertEqual([IP], retrieved)
