from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from api.models import GeoIP

from annoying.decorators import ajax_request

import constants

import util
import json


def json_response(res):
    return HttpResponse(json.dumps(res),
                        content_type="application/json")


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
    res = {key: data.get(key) for key in constants.REQ_KEYS}
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
    if request.method == constants.POST:
        try:
            data = json.loads(request.body)
        except ValueError:
            data = {}
    if not len(data):
        data = dict(request.REQUEST)
    return data


def history(request, uuid):
    page, offset = _get_page(request)
    history = GeoIP.objects.filter(
        uuid=uuid).order_by('-created_at')[offset:offset+constants.PAGE_SIZE]

    r = map(lambda geoip: geoip.as_clean_dict(), history)
    return json_response(r)


def _get_page(request):
    page = util.atoi(request.GET.get("page"), 0)
    page = max(page - 1, 0)
    offset = page * constants.PAGE_SIZE
    return page, offset
