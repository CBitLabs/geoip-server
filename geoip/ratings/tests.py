from django.test import TestCase, Client

from ratings.models import IpEvent, Rating
from ratings.query_manager import rating_manager, get_ips_by_bssid, get_ips_by_ssid
from ratings.util import get_network_score, get_res_dict

from common.constants import IP, BSSID, SSID, LAT, LNG
from common.util import create_test_geoip, create_test_ipevent, assert_res_code, as_json


class EntityValueTest(TestCase):

    def setUp(self):
        create_test_ipevent()

    def test_total_freq(self):
        event = IpEvent.objects.get(date=16000, ip=IP)
        self.assertEqual(event.total_freq(), 3)

    def test_total_count(self):
        event = IpEvent.objects.get(date=16000, ip=IP)
        self.assertEqual(event.total_count(), 3)


class RatingTest(TestCase):

    def test_rating_manager_cache(self):
        created = Rating.objects.create(raw_score=55, bssid=BSSID)
        retrieved = rating_manager(IP, BSSID)
        self.assertEqual(created, retrieved)
        self.assertEqual(len(Rating.objects.all()), 1)

    def test_rating_manager_create(self):
        rating_manager(IP, BSSID)
        self.assertEqual(len(Rating.objects.all()), 1)

    def test_rating_manager_by_ip(self):
        create_test_geoip()
        event = create_test_ipevent()
        created = Rating.objects.create(raw_score=get_network_score([event]),
                                        bssid=BSSID)
        retrieved = rating_manager(IP)
        self.assertEqual(created, retrieved)

    def test_get_network_score(self):
        event = create_test_ipevent()
        create_test_geoip()
        score = get_network_score([event])
        rating = rating_manager(IP, BSSID)
        self.assertEqual(rating.raw_score, score)

    def test_get_ips_by_bssid(self):
        create_test_geoip()
        retrieved = get_ips_by_bssid(BSSID)
        self.assertEqual([IP], retrieved)

    def test_get_ips_by_ssid(self):
        create_test_geoip()
        retrieved = get_ips_by_ssid(SSID, LAT, LNG)
        self.assertEqual([IP], retrieved)

    def test_filter_by_dist(self):
        """
            test the filter on radius
        """
        # lat/lng outside of radius
        far_lat = LAT + 0.1
        far_lng = LNG + 0.1

        create_test_geoip()

        create_test_geoip(lat=far_lat, lng=far_lng)

        retrieved = get_ips_by_ssid(SSID, LAT, LNG)
        self.assertEqual([IP], retrieved)


class RatingViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        create_test_ipevent()
        create_test_geoip()

    @as_json
    @assert_res_code
    def get_rating(self, data={}):
        res = self.client.get('/ratings/get_rating', data=data)
        return res

    def test_get_rating_view(self):
        res = self.get_rating({'bssid': BSSID})
        objs = Rating.objects.all()
        self.assertEqual(len(objs), 1)
        rating_dict = get_res_dict(objs.first())
        self.assertEqual(rating_dict, res)
