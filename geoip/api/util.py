from pygeocoder import Geocoder, GeocoderError

from ratings.query_manager import rating_manager
from ratings.util import get_clean_rating_dict

from common.util import get_client_ip

import api.constants as constants
import api.models as models

import re


EXPRS = {
    "float": r"[-+]?\d*\.\d+|\d+",
    "ipv4": r"[0-9]+(?:\.[0-9]+){3}",
    "ssid": r"[^.]+"
}

DNS_EXPR = r"(?P<resolver>[sd]{1})\.(?P<lat>%(float)s)\.(?P<lng>%(float)s)\.(?P<ssid>%(ssid)s)\.(?P<bssid>\w+)\.(?P<uuid>\w+)\.(?P<ip>%(ipv4)s)\..*" % EXPRS


def atoi(val, default=None):
    return _convert(val, default, int)


def atof(val, default=None):
    return _convert(val, default, float)


def _convert(val, default, func):
    try:
        return func(val)
    except (ValueError, TypeError):
        return default


def apply_transforms(transforms, d):
    """
        Functions take in a dictionary and
        apply a transform to the values.
        Used to clean data for serialization
    """
    for key, func in transforms:
        d[key] = func(d)


def parse_dns(d, expr=DNS_EXPR):
    """
        Parses data sent by the DNS server.
        input:
        d: input dictionary with form data
            expect {
                qname : dns string,
                srcip : originating IP address
            }
        output:
        {
            'lat' : lat,
            'lng' : lng,
            'ip' : ip,
            'bssid' : bssid,
            'ssid' : ssid,
            'uuid' : uuid,
            'remote_addr' : srcip
        }

        where keys are None if they cannot be parsed
    """
    try:
        res = re.match(expr, d.get("qname", "")).groupdict()
        res['remote_addr'] = d.get('srcip')
        return res
    except AttributeError:
        return {key: None for key in constants.REQ_KEYS}


def get_datasrc(res):
    """
        Tool to format the DNS type.
        datasrc type can be:
            dns-
            dns-s
            dns-d
    """
    return "%s-%s" % (constants.DNS, res.get("resolver", ""))


def validate_report(request, res, src, remote_addr=None):
    """
        Takes in a request object for wifi reports
        and validates the data.
        If valid, a GeoIP object is created.
    """
    transforms = [
        ('lat', lambda d: atof(d['lat'])),
        ('lng', lambda d: atof(d['lng'])),
    ]

    apply_transforms(transforms, res)
    res["datasrc"] = src

    if remote_addr is None:
        remote_addr = get_client_ip(request)
    res["remote_addr"] = remote_addr

    rating = rating_manager(remote_addr, res['bssid'],
                            res['ssid'], res['lat'], res['lng'])

    res['rating'] = rating

    success = is_valid(res)

    if success:
        if src != constants.SCAN:
            res["loc"] = _reverse_geo(res["lat"], res["lng"])
        res = write_db(res)
    else:
        res['rating'] = get_clean_rating_dict(rating)

    res["success"] = success
    return res


def is_valid(res):
    for k, v in res.iteritems():
        if v is None:
            return False
    return True


def _reverse_geo(lat, lng):
    """
        Attempt to find a human readable address from 
        the Google Geocoder
    """
    if _is_null_loc(lat, lng):
        loc = constants.NO_LOC

    try:
        loc = Geocoder.reverse_geocode(lat, lng).formatted_address
    except GeocoderError, e:
        if constants.QUERY_LIMIT in e:
            loc = constants.QUERY_LIMIT
        else:
            loc = constants.NO_LOC
    return loc


def _is_null_loc(lat, lng):
    return lat == 0 or lng == 0


def write_db(d):
    """
        Create a new GeoIP object and
        return a cleaned dictionary of the object
        for serialization.
    """
    d = _validate(d)
    geoip = models.GeoIP(**d)
    geoip.save()
    d.update(geoip.as_clean_dict())
    return d


def _validate(res):
    # clean out entries not part of model
    valid_fields = set(
        map(lambda field: field.name, models.GeoIP._meta.fields))
    return {k: v for k, v in res.iteritems() if k in valid_fields}
