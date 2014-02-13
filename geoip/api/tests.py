from django.test.client import RequestFactory
from django.test import TestCase, Client

from api.models import GeoIP
from api.query_manager import history_manager
import api.constants as constants

from common.constants import IP, UUID, SSID
from common.util import get_test_geoip_obj

import random
import json


def assert_res_code(func, code=200):
    def wrapped(self, *args, **kwargs):
        res = func(self, *args, **kwargs)
        self.assertEqual(res.status_code, code)
        return res
    return wrapped


def as_json(func):
    def wrapped(self, *args, **kwargs):
        res = func(self, *args, **kwargs)
        return json.loads(res.content)
    return wrapped


def assert_loc(func):
    def wrapped(self, *args, **kwargs):
        res = func(self, *args, **kwargs)
        self.assertNotEqual(res['loc'], constants.NO_LOC)
    return wrapped


class ApiTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def gen_valid_report(self):
        obj = get_test_geoip_obj()
        del obj['remote_addr']  # added by request
        return obj

    def gen_invalid_report(self):
        report = self.gen_valid_report()
        del report[random.choice(report.keys())]
        return report

    def gen_valid_dns_request(self):
        return {
            'qname': 'd.42.3953404.-71.1456972.Equity_eWireless.06026fc50cd3.xrig9u9j6vaq.101.12.210.74.geo.cbitlabs.com',
            'srcip': IP,
        }

    def gen_invalid_dns_request(self):
        data = self.gen_valid_report()
        data['qname'] = ''
        return data

    @as_json
    @assert_res_code
    def get_history(self, uuid):
        res = self.client.get('/history/%s' % uuid)
        return res

    @as_json
    @assert_res_code
    def post_add(self, data):
        res = self.client.post('/add', data=data)
        return res

    @as_json
    @assert_res_code
    def post_dnsadd(self, data):
        res = self.client.post('/dnsadd', data=data)
        return res

    @as_json
    @assert_res_code
    def get_add(self, data):
        res = self.client.get('/add', data=data)
        return res

    @as_json
    @assert_res_code
    def get_dnsadd(self, data):
        res = self.client.get('/dnsadd', data=data)
        return res

    def assert_history(self, count, uuid=UUID):
        self.assertEqual(len(self.get_history(uuid)), count)

    @assert_loc
    def test_post_valid_report(self):
        res = self.post_add(self.gen_valid_report())
        self.assertTrue(res['success'])
        return res

    def test_post_invalid_report(self):
        res = self.post_add(self.gen_invalid_report())
        self.assertFalse(res['success'])
        return res

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
    def test_get_valid_report(self):
        res = self.get_add(self.gen_valid_report())
        self.assertTrue(res['success'])
        return res

    def test_get_invalid_report(self):
        res = self.get_add(self.gen_invalid_report())
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

    def test_history_count(self):
        count = 0
        self.assert_history(count)

        # add valid report
        self.post_add(self.gen_valid_report())
        count += 1
        self.assert_history(count)

        self.post_dnsadd(self.gen_valid_dns_request())
        count += 1
        self.assert_history(count)

        # don't add invalid
        self.post_add(self.gen_invalid_report())
        self.assert_history(count)

        self.post_dnsadd(self.gen_invalid_dns_request())
        self.assert_history(count)
        return count

    def test_history_order(self):
        """
            test correct order by filter for history
        """
        self.test_history_count()
        history = self.get_history(UUID)
        self.assertGreaterEqual(history[0]['created_at'],
                                history[-1]['created_at'])


class HistoryQueryManagerTest(TestCase):

    def setUp(self):
        self.type1 = get_test_geoip_obj(ssid=SSID + "1")
        self.type2 = get_test_geoip_obj(ssid=SSID + "2")
        self.type3 = get_test_geoip_obj(ssid=SSID + "3")
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
        request = self.factory.get('/history/%s' % UUID)
        history = history_manager(request, UUID)
        self.assertEqual(len(history), constants.PAGE_SIZE)
        self.assert_count(history, 1)

        request = self.factory.get('/history/%s?page=2' % UUID)
        history = history_manager(request, UUID)
        self.assertEqual(len(history), constants.PAGE_SIZE)
        self.assert_count(history, 1)
