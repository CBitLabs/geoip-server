"""
    Generate and retrieve ratings for networks
"""

from ratings.util import get_epoch_days, calc_dist, get_network_score
from ratings.models import Rating, IpEvents
from api.models import GeoIP

from annoying.functions import get_object_or_None

RADIUS = 100  # meters


def get_rating(bssid, ssid=None, lat=None, lng=None):
    """
        bssid: used for primary grouping of IPS to rating
        ssid: used in conjunction w/lat, lng to cluster on 
        larger networks.
        Returns the rating for the current day w/ the given parameters
    """
    rating = get_from_cache(bssid)
    if rating:
        return rating

    return create_rating(bssid, ssid, lat, lng)


def get_from_cache(bssid):
    """
        Check if the rating object is already computed for this day.
    """

    epoch_day = get_epoch_days()
    return get_object_or_None(Rating, bssid=bssid, date=epoch_day)


def create_rating(bssid, ssid, lat, lng):
    """
        Creates and returns a rating object.
        Uses the bssid to cluster IPs to generate a score
        Uses the ssid, lat, lng, if all present to gather further IPs
    """
    bssid_ips = get_ips_by_bssid(bssid)
    ssid_ips = get_ips_by_ssid(ssid, lat, lng)
    ips = set(bssid_ips).union(set(ssid_ips))
    events = IpEvents.objects.filter(ips__in=ips)
    score = get_network_score(events)
    rating = Rating.objects.create(raw_score=score, bssid=bssid)
    return rating


def get_ips_by_bssid(bssid):
    objs = GeoIP.objects.filter(bssid=bssid)
    return _extract_ips(objs)


def get_ips_by_ssid(ssid, lat, lng):
    objs = GeoIP.objects.filter(ssid__icontains=ssid)
    objs = filter_by_loc(lat, lng, objs)
    return _extract_ips(objs)


def _extract_ips(geoip_objs):
    return map(lambda o: o.ip, geoip_objs)


def filter_by_loc(lat, lng, objs):
    filtered_objs = []
    for o in objs:
        if calc_dist(lat, lng, o.lat, o.lng) < RADIUS:
            filtered_objs.append(o)
    return filtered_objs
