import re
import constants

EXPRS = {
    "float" : "[-+]?\d*\.\d+|\d+",
    "ip" : "[0-9]+(?:\.[0-9]+){3}",
    "ssid" : "[^.]+"
}

DNS_EXPR = r"(.{1})\.(?P<lat>%(float)s)\.(?P<lng>%(float)s)\.(?P<ssid>%(ssid)s)\.(?P<bssid>\w+)\.(?P<uuid>\w+)\.(?P<ip>%(ip)s)\..*" % EXPRS

def atoi(val, default=None):
    return _convert(val, default, int)

def atof(val, default=None):
    return _convert(val, default, float)

def _convert(val, default, func):
    try:
        return func(val)
    except (ValueError, TypeError) as e:
        return default

def apply_transforms(transforms, d):
    for key, func in transforms:
        d[key] = func(d)

def parse_dns(d):
    """
        input:
        d: input dictionary with form data
            expect {dns : dns string}
        output:
        {
            'lat' : req,
            'lng' : req,
            'ip' : req,
            'bssid' : req,
            'ssid' : req,
            'uuid' : req,
        }

        where keys are None if they cannot be parsed
    """
    try:
        return re.match(DNS_EXPR, d.get("dns", "")).groupdict()
    except AttributeError:
        return {key : None for key in constants.REQ_KEYS}