import os
import server
import unittest
import tempfile
import random
import json

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
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

    def as_json(self, res):
        return json.loads(res.data)

    def test_add_valid_report(self):
        data = self.post_add(self.gen_valid_report())
        self.assertTrue(data['success'])

    def test_add_invalid_report(self):
        data = self.post_add(self.gen_invalid_report())
        self.assertFalse(data['success'])

    def test_history_count(self):
        uuid = 0
        self.assertEqual(len(self.get_history(uuid)), 0)
        
        #add valid report
        self.post_add(self.gen_valid_report())
        self.assertEqual(len(self.get_history(uuid)), 1)
        
        #don't add invalid
        self.post_add(self.gen_invalid_report())
        self.assertEqual(len(self.get_history(uuid)), 1)


if __name__ == '__main__':
    unittest.main()