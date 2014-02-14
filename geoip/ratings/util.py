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
