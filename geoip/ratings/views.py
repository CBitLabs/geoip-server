from django.views.decorators.csrf import csrf_exempt

from rating.query_manager import rating_manager

from annoying.decorators import ajax_request


@csrf_exempt
@ajax_request
def get_rating(request):
    bssid = request.GET.get("bssid")
    ssid = request.GET.get("ssid")
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")
    ip = request.remote_addr

    rating = rating_manager(ip, bssid, ssid, lat, lng)
    return rating.as_clean_dict()
