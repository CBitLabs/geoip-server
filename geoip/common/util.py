from django.http import HttpResponse
from django.conf import settings
from sqlalchemy import create_engine
from collections import defaultdict

from ratings.models import IpEvent
from api.models import GeoIP
from api.constants import NO_SEC

from common.constants import LAT, LNG, SSID, BSSID, UUID, IP

from geopy import distance, Point
import json


def calc_dist(lat1, lng1, lat2, lng2):
    """
        Returns the distance in meters between
        two lat lng pairs
    """
    point1 = Point(_get_point(lat1, lng1))
    point2 = Point(_get_point(lat2, lng2))
    return distance.distance(point1, point2).meters


def _get_point(lat, lng):
    return "%s;%s" % (lat, lng)


def dsum(dicts):
    """
        helper to sum the values of a dictionary
    """
    ret = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            ret[k] += v
    return dict(ret)


# commands
def get_conn():
    uri = "postgresql://%(USER)s:%(PASSWORD)s@%(HOST)s/%(NAME)s"
    eng = create_engine(uri % settings.POSTGRES)
    return eng.connect()


# view methods
def json_response(res):
    return HttpResponse(json.dumps(res),
                        content_type="application/json")


def get_client_ip(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# testing methods
def create_test_geoip(lat=LAT, lng=LNG, ssid=SSID,
                      bssid=BSSID, uuid=UUID, ip=IP):
    return GeoIP.objects.create(
        **get_test_geoip_dict(lat, lng,
                              ssid, bssid,
                              uuid, ip
                              )
    )


def create_test_ipevent(date=16000, ip=IP,
                        spam_count=1, spam_freq=1,
                        bot_count=1, bot_freq=1,
                        unexp_count=1, unexp_freq=1):
    return IpEvent.objects.create(
        **get_test_ipevent_dict(date, ip,
                                spam_count, spam_freq,
                                bot_count, bot_freq,
                                unexp_count, unexp_freq
                                )
    )


def get_test_geoip_dict(lat=LAT, lng=LNG, ssid=SSID,
                        bssid=BSSID, uuid=UUID, ip=IP,
                        security=NO_SEC, isEnterprise=False):
    """
        Used to testing purposes
    """
    return {
        "lat": lat,
        "lng": lng,
        "ssid": ssid,
        "bssid": bssid,
        "uuid": uuid,
        "ip": ip,
        "remote_addr": ip,
        "security": security,
        "isEnterprise": isEnterprise,
    }


def get_test_ipevent_dict(date, ip,
                          spam_count, spam_freq,
                          bot_count, bot_freq,
                          unexp_count, unexp_freq):
    return {
        'date': date,
        'ip': ip,
        'spam_count': spam_count,
        'spam_freq': spam_freq,
        'bot_count': bot_count,
        'bot_freq': bot_freq,
        'unexp_count': unexp_count,
        'unexp_freq': unexp_freq,
    }


def get_test_event_count(spam_count=1, spam_freq=1,
                         bot_count=1, bot_freq=1,
                         unexp_count=1, unexp_freq=1):
        return {
            'spam_count': spam_count,
            'spam_freq': spam_freq,
            'bot_count': bot_count,
            'bot_freq': bot_freq,
            'unexp_count': unexp_count,
            'unexp_freq': unexp_freq,
        }


def assert_res_code(func):
    def wrapped(self, *args, **kwargs):
        res = func(self, *args, **kwargs)
        self.assertEqual(res.status_code, 200)
        return res
    return wrapped


def as_json(func):
    def wrapped(self, *args, **kwargs):
        res = func(self, *args, **kwargs)
        return json.loads(res.content)
    return wrapped
