from django.views.decorators.csrf import csrf_exempt

from api.query_manager import history_manager
from common.util import json_response

from annoying.decorators import ajax_request

import api.constants as constants
import api.util as util

import json


@csrf_exempt
@ajax_request
def add(request):
    """
        Endpoint to process a geo-ip request.
        Input values: {
            'lat' : req,
            'lng' : req,
            'ip' : req,
            'bssid' : req,
            'ssid' : req,
            'uuid' : req,
        }
    """

    data = _get_data(request)
    res = {
        key: data.get(key)
        for key in constants.REQ_KEYS
    }

    res = util.process_res(request, res, constants.HTTP)

    return res


@csrf_exempt
@ajax_request
def dns_add(request):
    """
        Endpoint to process dns forwarding
    """
    data = _get_data(request)
    res = util.parse_dns(data)
    datasrc = util.get_datasrc(res)
    res = util.process_res(request, res, datasrc)

    return res


def _get_data(request):
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
    history_json = history_manager(request, uuid)
    return json_response(history_json)
