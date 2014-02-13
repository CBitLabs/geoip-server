from geopy import distance, Point
import time

SECONDS_IN_DAY = 60 * 60 * 24


def get_epoch_days():
    seconds = time.time()
    return int(seconds / SECONDS_IN_DAY)


def calc_dist(lat1, lng1, lat2, lng2):
    point1 = Point(_get_point(lat1, lng1))
    point2 = Point(_get_point(lat2, lng2))
    return distance.distance(point1, point2).meters


def _get_point(lat, lng):
    return "%s;%s" % (lat, lng)


def get_network_score(events):
    """
        Takes in a list of IpEvent objects clustered for a single network
        and calculates a score for the given set
    """
    # TODO
    return sum(map(lambda o: o.total_count() + o.total_freq(), events))


def get_res_dict(rating):
    success = rating is not None
    data = {}

    if success:
        data = rating.as_clean_dict()

    return {
        "success": success,
        "data": data
    }


def get_clean_rating_dict(rating):
    if rating is None:
        return {}
    return rating.as_clean_dict()
