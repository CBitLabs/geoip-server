from django.views.decorators.csrf import csrf_exempt
from annoying.decorators import ajax_request

from ratings.query_manager import rating_manager
from ratings.util import get_res_dict

from common.util import get_client_ip


@csrf_exempt
@ajax_request
def get_rating(request):
    """
        retrieve a single rating for a network
    """
    bssid = request.GET.get("bssid")
    ssid = request.GET.get("ssid")
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")
    ip = get_client_ip(request)

    rating = rating_manager(ip, bssid, ssid, lat, lng)
    return get_res_dict(rating)


@csrf_exempt
@ajax_request
def scan_ratings(request):
    """
        send back a list of rating objects
        can be found by searching by bssid or ssid
    """
    bssids = request.GET.getlist("bssid")
    ssids = request.GET.getlist("ssid")

    ip = get_client_ip(request)

    # ratings found by bssid
    bssid_ratings = {
        bssid: rating_manager(ip, bssid=bssid).as_clean_dict()
        for bssid in bssids
    }

    # ratings found by ssid
    ssid_ratings = {
        ssid: rating_manager(ip, ssid=ssid).as_clean_dict()
        for ssid in ssids
    }

    bssid_ratings.update(ssid_ratings)

    return bssid_ratings
