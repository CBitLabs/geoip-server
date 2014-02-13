from api.models import GeoIP
import api.constants as constants
import api.util as util


def history_manager(request, uuid):
    """
        Manager for querying history objects.
        Groups history items to reduce duplicated view clutter on clients
    """
    start, end = get_slice(request)
    history = GeoIP.objects.filter(
        uuid=uuid).order_by('-created_at')[start:end]
    json = collapse_history_dups(history)
    return json


def get_slice(request):
    offset = _get_offset(request)
    return offset, offset + constants.PAGE_SIZE


def _get_offset(request):
    page = util.atoi(request.GET.get("page", 0), 0)
    page = max(page - 1, 0)
    offset = page * constants.PAGE_SIZE
    return offset


def collapse_history_dups(geoip_objs):
    """
        collapses items that are from the same 
        ssid into a single entry.
        returns a list of ordered json entries 
        for each GeoIP object. Adds a count field
        for the number of collapsed items.
    """

    res = []
    i = 0
    while i < len(geoip_objs):
        obj = geoip_objs[i]
        json = obj.as_clean_dict()
        count = 0
        for o in geoip_objs[i:]:
            if o.ssid != obj.ssid:
                break

            count += 1

        json['count'] = count
        res.append(json)
        i += count

    return res
