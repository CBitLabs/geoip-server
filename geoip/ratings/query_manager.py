"""
    Generate and retrieve ratings for networks
"""
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned
from annoying.functions import get_object_or_None

from ratings.util import get_epoch_days, get_network_score, get_event_counts
from ratings.models import Rating, IpEvent

from api.constants import DNS_D, SCAN
from api.models import GeoIP

from common.constants import RADIUS
from common.util import calc_dist


def rating_manager(ip, bssid=None, ssid=None,
                   lat=None, lng=None, use_cache=True):
    """
        bssid: used for primary grouping of IPS to rating
        ssid: used in conjunction w/lat, lng to cluster on 
        larger networks.
        Returns the rating for the current day w/ the given parameters
    """
    if bssid is None:
        geoip = bssid_from_ip(ip)  # try to match by ip

        if geoip is not None:
            bssid = geoip.bssid

    if ssid is not None:
        geoip = geoip_from_ssid(ip)  # try to match by ip

        if geoip is not None:
            bssid = geoip.bssid

    if bssid is None:
        bssid = ""

    if use_cache:
        rating = get_from_cache(bssid)
        if rating is not None:
            return rating

    return create_rating(bssid, ssid, lat, lng)


def bssid_from_ip(ip):
    return GeoIP.objects.filter(ip=ip).first()


def geoip_from_ssid(ssid):
    return GeoIP.objects.filter(ssid=ssid).first()


def get_from_cache(bssid):
    """
        Check if the rating object is already computed for this day.
    """

    epoch_day = get_epoch_days()
    try:
        rating = get_object_or_None(Rating, bssid=bssid, date=epoch_day)
    except MultipleObjectsReturned:
        ratings = Rating.objects.filter(bssid=bssid)
        rating = ratings.first()
        for rating in ratings[1:]:
            rating.delete()

    return rating


def create_rating(bssid, ssid, lat, lng):
    """
        Creates and returns a rating object.
        Uses the bssid to cluster IPs to generate a score
        Uses the ssid, lat, lng, if all present to gather further IPs
    """
    bssid_ips = get_ips_by_bssid(bssid)
    ssid_ips = get_ips_by_ssid(ssid, lat, lng)

    ips = set(bssid_ips).union(set(ssid_ips))
    events = IpEvent.objects.filter(ip__in=ips)
    score = get_network_score(events)
    is_valid = len(events) > 0
    event_counts = get_event_counts(events)
    rating = Rating.objects.create(
        raw_score=score, bssid=bssid, is_valid=is_valid, **event_counts)
    return rating


def get_ips_by_bssid(bssid):
    objs = _get_geoip(bssid=bssid)
    return _extract_ips(objs)


def get_ips_by_ssid(ssid, lat, lng):
    if not all([ssid, lat, lng]):
        return []

    objs = _get_geoip(ssid__icontains=ssid)
    objs = filter_by_loc(lat, lng, objs)
    return _extract_ips(objs)


def _get_geoip(**kwargs):
    return GeoIP.objects.filter(~Q(datasrc__in=[DNS_D, SCAN]), **kwargs)


def _extract_ips(geoip_objs):
    return map(lambda o: o.ip, geoip_objs)


def filter_by_loc(lat, lng, objs):
    """
        Exclude object that are outside of RADISU meters
    """
    filtered_objs = []
    for o in objs:
        if calc_dist(lat, lng, o.lat, o.lng) < RADIUS:
            filtered_objs.append(o)
    return filtered_objs
