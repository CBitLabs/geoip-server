from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from api.models import GeoIP

from annoying.decorators import ajax_request
from constants import *
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
    res = {key: data.get(key) for key in REQ_KEYS}
    res = _process_res(request, res, HTTP)
    return res


@csrf_exempt
@ajax_request
def dns_add(request):
    """
        Endpoint to process dns forwarding
    """
    data = _get_data(request)
    res = util.parse_dns(data)
    res = _process_res(request, res, DNS)

    return res


def _get_data(request):
    if request.method == POST:
        try:
            data = json.loads(request.body)
        except ValueError:
            data = {}
    if not len(data):
        data = dict(request.REQUEST)
    return data


def _process_res(request, res, src):
    transforms = [
        ('lat', lambda d: util.atof(d['lat'])),
        ('lng', lambda d: util.atof(d['lng'])),
    ]

    util.apply_transforms(transforms, res)
    success = _is_valid(res)
    res["datasrc"] = src
    res["remote_addr"] = util.get_client_ip(request)

    if success:
        res = _write_db(res)

    res["success"] = success

    return res


def _is_valid(res):
    for k, v in res.iteritems():
        if v is None:
            return False
    return True


def _write_db(d):
    geoip = GeoIP(**d)
    geoip.save()

    d.update(geoip.as_clean_dict())
    return d


def history(request, uuid):
    page, offset = _get_page(request)
    history = GeoIP.objects.filter(
        uuid=uuid).order_by('created_at')[offset:PAGE_SIZE]

    r = map(lambda geoip: geoip.as_clean_dict(), history)
    return json_response(r)


def _get_page(request):
    page = util.atoi(request.GET.get("page"), 0)
    page = max(page - 1, 0)
    offset = page * PAGE_SIZE
    return page, offset
