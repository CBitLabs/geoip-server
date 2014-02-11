from django.test import TestCase

from ratings.models import EntityValue


class EntityValueTestCase(TestCase):

    def setUp(self):
        data = {
            'date': 16000,
            'address': '127.0.0.1',
            'spam_count': 1,
            'spam_freq': 1,
            'bot_count': 1,
            'bot_freq': 1,
            'unexp_count': 1,
            'unexp_freq': 1,
        }
        EntityValue.objects.create(**data)

    def test_total_freq(self):
        ev = EntityValue.objects.get(date=16000, address="127.0.0.1")
        self.assertEqual(ev.total_freq(), 3)

    def test_total_count(self):
        ev = EntityValue.objects.get(date=16000, address="127.0.0.1")
        self.assertEqual(ev.total_count(), 3)
