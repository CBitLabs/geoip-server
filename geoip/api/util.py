import re
import constants

EXPRS = {
    "float": "[-+]?\d*\.\d+|\d+",
    "ip": "[0-9]+(?:\.[0-9]+){3}",
    "ssid": "[^.]+"
}

DNS_EXPR = r"(.{1})\.(?P<lat>%(float)s)\.(?P<lng>%(float)s)\.(?P<ssid>%(ssid)s)\.(?P<bssid>\w+)\.(?P<uuid>\w+)\.(?P<ip>%(ip)s)\..*" % EXPRS


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


def parse_dns(d):
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
        res = re.match(DNS_EXPR, d.get("qname", "")).groupdict()
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
