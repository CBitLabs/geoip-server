import os
import server
import unittest
import tempfile
import random
import json

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
        server.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s" % server.app.config['DATABASE']
        server.db.create_all()
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(server.app.config['DATABASE'])

    def gen_valid_report(self):
        return { key : 0 for key in server.REQ_KEYS }

    def gen_invalid_report(self):
        report = self.gen_valid_report()
        del report[random.choice(server.REQ_KEYS)]
        return report

    def gen_valid_dns_request(self):
        return {
            'qname' : 'd.42.3953404.-71.1456972.Equity_eWireless.06026fc50cd3.xrig9u9j6vaq.101.12.210.74.geo.spf.gladstonefamily.net',
            'srcip' : '192.168.1.1',
        }

    def gen_invalid_dns_request(self):
        data = self.gen_valid_report()
        data['qname'] = ''
        return data

    def get_history(self, uuid, as_json=True):
        res = self.app.get('/history/%s' % uuid)
        
        if as_json:
            return self.as_json(res)
        return res

    def post_add(self, data, as_json=True):
        res = self.app.post('/add', data=data)

        if as_json:
            return self.as_json(res)
        return res

    def post_dnsadd(self, data, as_json=True):
        res = self.app.post('/dnsadd', data=data)

        if as_json:
            return self.as_json(res)
        return res

    def as_json(self, res):
        return json.loads(res.data)

    def test_add_valid_report(self):
        res = self.post_add(self.gen_valid_report())
        self.assertTrue(res['success'])

    def test_add_invalid_report(self):
        res = self.post_add(self.gen_invalid_report())
        self.assertFalse(res['success'])

    def test_history_count(self):
        uuid = 0
        self.assertEqual(len(self.get_history(uuid)), 0)
        
        #add valid report
        self.post_add(self.gen_valid_report())
        self.assertEqual(len(self.get_history(uuid)), 1)
        
        #don't add invalid
        self.post_add(self.gen_invalid_report())
        self.assertEqual(len(self.get_history(uuid)), 1)

    def test_dns_valid(self):
        res = self.post_dnsadd(self.gen_valid_dns_request())
        self.assertTrue(res['success'])

    def test_dns_invalid(self):
        res = self.post_dnsadd(self.gen_invalid_dns_request())
        self.assertFalse(res['success'])


if __name__ == '__main__':
    unittest.main()