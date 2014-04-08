import time

SECONDS_IN_DAY = 60 * 60 * 24


def get_epoch_days():
    seconds = time.time()
    return int(seconds / SECONDS_IN_DAY)


def get_network_score(events):
    """
        Takes in a list of IpEvent objects clustered for a single network
        and calculates a score for the given set
    """
    return sum(map(lambda o: o.total_count() + o.total_freq(), events))


def get_event_counts(events):
    """
        returns a dictionary for spam, bot, and unexp counts and freqs
    """
    from common.util import dsum
    count_dicts = map(lambda e: e.get_event_counts(), events)
    return dsum(count_dicts)


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
