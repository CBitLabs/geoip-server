from django.test.client import RequestFactory
from django.test import TestCase, Client

from api.models import GeoIP
from api.query_manager import history_manager
import api.constants as constants

from common.constants import IP, UUID, SSID
from common.util import get_test_geoip_dict, assert_res_code, as_json
import common.no_warnings

import random
import json

SCAN_COUNT = 5


def assert_loc(func):
    def wrapped(self, *args, **kwargs):
        res = func(self, *args, **kwargs)
        self.assertNotEqual(res['loc'], constants.NO_LOC)
    return wrapped


class ApiTest(TestCase):

    def setUp(self):
        self.client = Client()

    def gen_valid_wifi_report(self):
        obj = get_test_geoip_dict()
        del obj['remote_addr']  # added by request
        return obj

    def gen_invalid_wifi_report(self):
        report = self.gen_valid_wifi_report()
        del report[random.choice(report.keys())]
        return report

    def gen_valid_scan_report(self):
        return [self.gen_valid_wifi_report() for _ in range(SCAN_COUNT)]

    def gen_invalid_scan_report(self):
        return [self.gen_invalid_wifi_report() for _ in range(SCAN_COUNT)]

    def gen_valid_dns_request(self):
        return {
            'qname': 'd.42.3953404.-71.1456972.Equity_eWireless.06026fc50cd3.xrig9u9j6vaq.101.12.210.74.geo.cbitlabs.com',
            'srcip': IP,
        }

    def gen_invalid_dns_request(self):
        data = self.gen_valid_wifi_report()
        data['qname'] = ''
        return data

    @as_json
    @assert_res_code
    def post_dnsadd(self, data):
        return self.client.post('/dnsadd', data=data)

    @as_json
    @assert_res_code
    def get_dnsadd(self, data):
        return self.client.get('/dnsadd', data=data)

    @as_json
    @assert_res_code
    def post_wifi_report(self, data):
        return self.client.post('/wifi_report', data=data)

    @as_json
    @assert_res_code
    def get_wifi_report(self, data):
        return self.client.get('/wifi_report', data=data)

    @as_json
    @assert_res_code
    def post_scan_report(self, data):
        return self.client.post('/scan_report',
                                content_type="application/json",
                                data=json.dumps(data))

    @as_json
    @assert_res_code
    def get_history(self, uuid):
        return self.client.get('/history/%s' % uuid)


class WifiReportTest(ApiTest):

    @assert_loc
    def test_post_valid_wifi_report(self):
        res = self.post_wifi_report(self.gen_valid_wifi_report())
        self.assertTrue(res['success'])
        return res

    def test_post_invalid_wifi_report(self):
        res = self.post_wifi_report(self.gen_invalid_wifi_report())
        self.assertFalse(res['success'])
        return res

    @assert_loc
    def test_get_valid_wifi_report(self):
        res = self.get_wifi_report(self.gen_valid_wifi_report())
        self.assertTrue(res['success'])
        return res

    def test_get_invalid_wifi_report(self):
        res = self.get_wifi_report(self.gen_invalid_wifi_report())
        self.assertFalse(res['success'])
        return res


class ScanReportTest(ApiTest):

    def test_post_valid_scan_report(self):
        res = self.post_scan_report(self.gen_valid_scan_report())
        self.assertTrue(res['success'])

        for rating in res['res']:
            self.assertEqual(rating['loc'], constants.NO_LOC)
        return res

    def test_post_invalid_scan_report(self):
        res = self.post_scan_report(self.gen_invalid_scan_report())
        self.assertFalse(res['success'])
        return res


class DnsReportTest(ApiTest):

    @assert_loc
    def test_postdns_valid(self):
        res = self.post_dnsadd(self.gen_valid_dns_request())
        self.assertTrue(res['success'])
        return res

    def test_postdns_invalid(self):
        res = self.post_dnsadd(self.gen_invalid_dns_request())
        self.assertFalse(res['success'])
        return res

    @assert_loc
    def test_getdns_valid(self):
        res = self.get_dnsadd(self.gen_valid_dns_request())
        self.assertTrue(res['success'])
        return res

    def test_getdns_invalid(self):
        res = self.get_dnsadd(self.gen_invalid_dns_request())
        self.assertFalse(res['success'])
        return res


class HistoryTest(ApiTest):

    def assert_history(self, count, uuid=UUID):
        self.assertEqual(GeoIP.objects.filter(uuid=uuid).count(), count)

    def test_history_count(self):
        count = 0
        self.assert_history(count)

        # add valid report
        self.post_wifi_report(self.gen_valid_wifi_report())
        count += 1
        self.assert_history(count)

        self.post_dnsadd(self.gen_valid_dns_request())
        count += 1
        self.assert_history(count)

        # don't add invalid
        self.post_wifi_report(self.gen_invalid_wifi_report())
        self.assert_history(count)

        self.post_dnsadd(self.gen_invalid_dns_request())
        self.assert_history(count)

        self.post_scan_report(self.gen_valid_scan_report())
        count += SCAN_COUNT
        self.assert_history(count)
        return count

    def test_history_order(self):
        """
            test correct order by filter for history
        """
        self.test_history_count()  # setup history items
        history = self.get_history(UUID)
        self.assertGreaterEqual(history[0]['created_at'],
                                history[-1]['created_at'])


class HistoryQueryManagerTest(ApiTest):

    def setUp(self):
        self.type1 = get_test_geoip_dict(ssid=SSID + "1")
        self.type2 = get_test_geoip_dict(ssid=SSID + "2")
        self.type3 = get_test_geoip_dict(ssid=SSID + "3")
        self.factory = RequestFactory()

    def create_duplicated_objs(self):
        """
            create objects ordered to remove dups
        """
        self.create_objs(self.type1)
        self.create_objs(self.type2)
        self.create_objs(self.type3)

    def create_unordered_objs(self):
        self.create_objs([self.type1, self.type2, self.type3])

    def create_objs(self, data_arr):
        if not isinstance(data_arr, list):
            data_arr = [data_arr]
        for _ in xrange(constants.PAGE_SIZE):
            for data in data_arr:
                GeoIP.objects.create(**data)

    def assert_count(self, objs, size):
        for obj in objs:
            self.assertEqual(obj['count'], size)

    def get_history(self, page=0):
        request = self.factory.get('/history/%s?page=%s' % (UUID, page))
        return history_manager(request, UUID)

    def test_dup_history_count(self):
        self.create_duplicated_objs()
        history = self.get_history(page=0)
        self.assertEqual(len(history), 1)
        self.assert_count(history, constants.PAGE_SIZE)

        history = self.get_history(page=1)
        self.assertEqual(len(history), 1)
        self.assert_count(history, constants.PAGE_SIZE)

        history = self.get_history(page=2)
        self.assertEqual(len(history), 1)
        self.assert_count(history, constants.PAGE_SIZE)

    def test_nodup_history_count(self):
        self.create_unordered_objs()
        history = self.get_history(page=1)
        self.assertEqual(len(history), constants.PAGE_SIZE)
        self.assert_count(history, 1)

        history = self.get_history(page=2)
        self.assertEqual(len(history), constants.PAGE_SIZE)
        self.assert_count(history, 1)

    def test_no_scan_history(self):
        self.post_scan_report(self.gen_valid_scan_report())
        history = self.get_history()
        self.assert_count(history, 0)
