from django.views.decorators.csrf import csrf_exempt
from annoying.decorators import ajax_request

from common.util import json_response
import common.no_warnings

from api.query_manager import history_manager
from api.models import PrefReport
import api.constants as constants
import api.util as util

import json


@csrf_exempt
@ajax_request
def wifi_report(request):
    """
        Endpoint to process a geo-ip request.
        Input values: {
            'lat' : req,
            'lng' : req,
            'ip' : req,
            'bssid' : req,
            'ssid' : req,
            'uuid' : req,
            'security' : req,
            'isEnterprise' : req
        }
    """

    data = _get_data(request)
    res = {
        key: data.get(key)
        for key in constants.REQ_KEYS
    }

    res = util.validate_report(request, res, constants.HTTP)

    return res


@csrf_exempt
@ajax_request
def scan_report(request):
    """
        Endpoint to process a scan request.
        Takes a list of GeoIp type objects
    """

    data = _get_data(request)
    res = []
    success = True
    for el in data:
        geoip = {
            key: el.get(key)
            for key in constants.REQ_KEYS
        }

        geoip = util.validate_report(request, geoip, constants.SCAN)
        success = success and geoip['success']
        res.append(geoip)

    return {
        'success': success,
        'res': res,
    }


@csrf_exempt
@ajax_request
def dns_add(request):
    """
        Endpoint to process dns forwarding
    """
    data = _get_data(request)
    res = util.parse_dns(data)
    datasrc = util.get_datasrc(res)
    res = util.validate_report(request, res, datasrc)

    return res


@csrf_exempt
@ajax_request
def pref_report(request):
    """
        Endpoint to log user preferences for watched networks
    """

    data = _get_data(request)
    KEYS = ["uuid", "ssid"]
    success = len(data) == len(KEYS)

    for k in KEYS:
        if k not in data:
            success = False

    if success:
        pref = PrefReport(**data)
        pref.save()

    return {
        'success': success
    }


def _get_data(request):
    """
        Helper to return data from request as a dict.
        Most methods support both GET and POST requests,
        this method abstracts retrieving the data from either
    """
    data = {}
    if request.method == constants.POST:
        try:
            data = json.loads(request.body)
        except ValueError:
            pass
    if not len(data):
        data = dict(request.REQUEST)
    return data


def history(request, uuid):
    """
        Endpoint to process history requests.
        The history_manager does the heavy lifting of returning
        a sorted list of history data without duplicates.
    """
    history_json = history_manager(request, uuid)
    return json_response(history_json)
