from django.http import HttpResponse

from common.constants import LAT, LNG, SSID, BSSID, UUID, IP

import json


def json_response(res):
    return HttpResponse(json.dumps(res),
                        content_type="application/json")


def get_test_geoip_obj(lat=LAT, lng=LNG, ssid=SSID,
                       bssid=BSSID, uuid=UUID, ip=IP):
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
        "remote_addr": ip
    }
