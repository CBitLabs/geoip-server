from django.test import TestCase, Client
from api.constants import *

import random
import json

IP = "192.168.1.1"
UUID = "xrig9u9j6vaq"


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


class ApiTestCase(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def gen_valid_report(self):
        res = {key: 0 for key in REQ_KEYS}
        res['ip'] = IP
        res['remote_addr'] = IP
        res['uuid'] = UUID
        return res

    def gen_invalid_report(self):
        report = self.gen_valid_report()
        del report[random.choice(REQ_KEYS)]
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

    def test_post_valid_report(self):
        res = self.post_add(self.gen_valid_report())
        self.assertTrue(res['success'])

    def test_post_invalid_report(self):
        res = self.post_add(self.gen_invalid_report())
        self.assertFalse(res['success'])

    def test_postdns_valid(self):
        res = self.post_dnsadd(self.gen_valid_dns_request())
        self.assertTrue(res['success'])

    def test_postdns_invalid(self):
        res = self.post_dnsadd(self.gen_invalid_dns_request())
        self.assertFalse(res['success'])

    def test_get_valid_report(self):
        res = self.get_add(self.gen_valid_report())
        self.assertTrue(res['success'])

    def test_get_invalid_report(self):
        res = self.get_add(self.gen_invalid_report())
        self.assertFalse(res['success'])

    def test_getdns_valid(self):
        res = self.get_dnsadd(self.gen_valid_dns_request())
        self.assertTrue(res['success'])

    def test_getdns_invalid(self):
        res = self.get_dnsadd(self.gen_invalid_dns_request())
        self.assertFalse(res['success'])

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
