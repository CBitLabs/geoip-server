from django.views.decorators.csrf import csrf_exempt
from annoying.decorators import ajax_request

from ratings.query_manager import rating_manager
from ratings.util import get_res_dict

from common.util import get_client_ip


@csrf_exempt
@ajax_request
def get_rating(request):
    bssid = request.GET.get("bssid")
    ssid = request.GET.get("ssid")
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")
    ip = get_client_ip(request)

    rating = rating_manager(ip, bssid, ssid, lat, lng)
    return get_res_dict(rating)
