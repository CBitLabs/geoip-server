from pygeocoder import Geocoder, GeocoderError

import api.models as models

import constants
import re


EXPRS = {
    "float": "[-+]?\d*\.\d+|\d+",
    "ip": "[0-9]+(?:\.[0-9]+){3}",
    "ssid": "[^.]+"
}

DNS_EXPR = r"(?P<resolver>[sd]{1})\.(?P<lat>%(float)s)\.(?P<lng>%(float)s)\.(?P<ssid>%(ssid)s)\.(?P<bssid>\w+)\.(?P<uuid>\w+)\.(?P<ip>%(ip)s)\..*" % EXPRS


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
    for key, func in transforms:
        d[key] = func(d)


def parse_dns(d, expr=DNS_EXPR):
    """
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


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_datasrc(res):
    """
        datasrc type can be:
            dns
            dns-s
            dns-d
    """
    return "%s-%s" % (constants.DNS, res.get("resolver", ""))


def process_res(request, res, src):
    transforms = [
        ('lat', lambda d: atof(d['lat'])),
        ('lng', lambda d: atof(d['lng'])),
    ]

    apply_transforms(transforms, res)
    success = is_valid(res)
    res["datasrc"] = src
    res["remote_addr"] = get_client_ip(request)
    if success:
        res["loc"] = _reverse_geo(res["lat"], res["lng"])
        res = write_db(res)

    res["success"] = success
    return res


def is_valid(res):
    for k, v in res.iteritems():
        if v is None:
            return False
    return True


def _reverse_geo(lat, lng):
    try:
        return Geocoder.reverse_geocode(lat, lng).formatted_address
    except GeocoderError:
        return constants.NO_LOC


def write_db(d):
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
