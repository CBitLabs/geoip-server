"""
    query datadump in ip_events postgres table from ip_stats hadoop job
    to find data to contruct pipeline
"""

from optparse import OptionParser

import matplotlib.pyplot as plt
import psycopg2 as pg
import numpy as np
import os
import csv

AUTH = {

    "dbname": "postgres",
    "user": "jblum",
    "password": os.environ.get("POSTGRES")
}

EVENTS = [
    "spam_count",
    "spam_freq",
    "bot_count",
    "bot_freq",
    "unexp_count",
    "unexp_freq",
]

SUM_QUERY = """SELECT COALESCE(SUM(spam_count), 0),
                COALESCE(SUM(spam_freq), 0), 
                COALESCE(SUM(bot_count), 0), 
                COALESCE(SUM(bot_freq), 0), 
                COALESCE(SUM(unexp_count), 0), 
                COALESCE(SUM(unexp_freq), 0) 
            FROM ip_events_%(days)d WHERE address%(op)s INET '%(ip)s';"""

IN_FILE = "ip_list.csv"

LIMIT = 100


def main(days, use_subnet, compute_all):

    if compute_all:
        days = [50, 100]
    else:
        days = [days]

    for day in days:
        print "\nLoading ips..."
        ips = load_ips()

        print "\nBuilding stats..."
        ip_stats, subnet_stats = get_stats(ips, day, use_subnet)

        print "\nPrinting IP stats..."
        print_stats(ip_stats)

        if use_subnet:
            print "=" * 60
            print "=" * 60

            print "\nPrinting subnet stats..."
            print_stats(subnet_stats)

        get_ssid_stats(ip_stats, day)

    plt.show()


def load_ips(in_file=IN_FILE):
    with open(in_file) as f:
        reader = csv.reader(f)
        return set([row[0] for row in reader])


def load_ip_ssid_map(in_file=IN_FILE):
    with open(in_file) as f:
        reader = csv.reader(f)
        return {ip: ssid for ip, ssid in reader}


def get_stats(ips, days, use_subnet):
    """walk through list of ip addresses and gather sum across events"""
    cur = get_cursor()
    ip_stats = {}
    subnet_stats = {}
    for i, ip in enumerate(ips):
        ip_stats[ip] = sum_query(cur, ip, "=", days)

        if use_subnet:
            subnet = get_subnet(ip)
            subnet_stats[subnet] = sum_query(cur, subnet, "<<", days)

        if not i % 100:
            print "Queried %d rows." % i

    plot_stats("IP stats", ip_stats, days, bins=10)

    if use_subnet:
        plot_stats("subnet stats", subnet_stats,
                   days, bins=len(subnet_stats) / 10)

    return ip_stats, subnet_stats


def get_cursor(auth=AUTH):
    conn = pg.connect("dbname=%(dbname)s user=%(user)s password=%(password)s"
                      % AUTH)

    return conn.cursor()


def sum_query(cur, ip, op, days):
    query = make_sum_query(ip, op, days)
    rows = _fetch(cur, query)
    assert len(rows) == 1
    return sum_query_as_dict(rows[0])


def make_sum_query(ip, op, days):
    return _make_query(SUM_QUERY, ip, op, days)


def sum_query_as_dict(row):
    row_dict = {k: v for k, v in zip(EVENTS, row)}
    row_dict['freq'] = sum_freq(row_dict)
    row_dict['count'] = sum_count(row_dict)
    return row_dict


def _make_query(query, ip, op, days):
    return query % {
        'ip': ip,
        'op': op,
        'days': days

    }


def _fetch(cur, query):
    cur.execute(query)
    return cur.fetchall()


def get_subnet(ip):
    return ".".join(ip.split(".")[:-1]) + "/24"


def print_stats(stats):
    """
        dictionary of form {
            'ip' : {
                ROW
            }
        }

    print the min, max, avg type of each event for each ip
    print the number of ips with no events
    """
    print "Found %d events" % len(stats)

    get_event_stats(stats)
    get_tot_stats(stats)


def get_event_stats(stats):
    for event in EVENTS:
        vals = get_vals(stats, event)
        print_dict_stat("max", event, *get_max(stats, event))
        print_dict_stat("min", event, *get_min(stats, event))
        print_float_stat("avg", event, get_avg(vals))
        print_float_stat("stdev", event, get_stdev(vals))
        print_percent_stat("zeros", event, get_zero_percent(vals))
        print


def get_tot_stats(stats):
    print "-" * 60 + "\n"
    print "Printing totals...\n"
    print_tot_stats("freq", get_vals(stats, "freq"))
    print_tot_stats("count", get_vals(stats, "count"))


def print_tot_stats(name, stats):
    print_int_stat("max", name, max(stats))
    print_int_stat("min", name, min(stats))
    print_float_stat("avg", name, get_avg(stats))
    print_float_stat("stdev", name, get_stdev(stats))
    print_percent_stat("zeros", name, get_zero_percent(stats))
    print


def print_dict_stat(stat, event, ip, stats_dict):
    val = stats_dict[event]
    print "%s of %s from %s is %d." % (stat, event, ip, val)


def print_int_stat(stat, event, val):
    _print_stat(stat, event, "%d", val)


def print_float_stat(stat, event, val):
    _print_stat(stat, event, "%3f", val)


def print_percent_stat(stat, event, val):
    _print_stat(stat, event, "%.2f%%", val)


def _print_stat(stat, event, fmt, val):
    string = "%s of %s is %s." % (stat, event, fmt)
    print string % val


def get_max(stats, event):
    return max(stats.iteritems(), key=lambda kv: kv[1][event])


def get_min(stats, event):
    return min(stats.iteritems(), key=lambda kv: kv[1][event])


def get_avg(stats):
    return np.average(stats)


def get_stdev(stats):
    return np.std(stats)


def get_zero_percent(stats):
    num_zeros = len(filter(lambda x: x == 0, stats))
    return round(num_zeros / float(len(stats)), 2) * 100


def sum_count(stats):
    return sum(agg_type(stats, "count"))


def sum_freq(stats):
    return sum(agg_type(stats, "freq"))


def agg_type(stats, keyword):
    return [stats[e] for e in EVENTS if keyword in e]


def get_vals(stats, keyword):
    return map(lambda kv: kv[1][keyword], stats.iteritems())


def get_ssid_stats(stats, days):
    ip_ssid_map = load_ip_ssid_map()
    freq_ips = get_sorted_stats(stats, ip_ssid_map, "freq")
    count_ips = get_sorted_stats(stats, ip_ssid_map, "count")
    
    print "Top %d ssids" % LIMIT
    print_ssid_stats(freq_ips, "freq")
    print_ssid_stats(count_ips, "count")


def get_sorted_stats(stats, ip_ssid_map, keyword, limit=LIMIT):
    stats = sorted(stats.iteritems(),
                   key=lambda kv: kv[1][keyword], reverse=True)
    return map(lambda el: (ip_ssid_map[el[0]], el[0], el[1][keyword]), stats)[:limit]


def print_ssid_stats(ssid_stats, keyword):
    for ssid, ip, val in ssid_stats:
        print "ssid: %s, ip: %s, event_%s: %d" % (ssid, ip, keyword, val)


def plot_stats(title, stats, days, bins=5):
    plot_count(title, stats, bins, days)
    plot_freq(title, stats, bins, days)


def plot_count(title, stats, bins, days):
    plt.figure()

    plt.hist(get_vals(stats, "count"), bins=bins,
             histtype='stepfilled',
             color='r', label="count")
    configure_plot(title, "count", days)


def plot_freq(title, stats, bins, days):
    plt.figure()
    plt.hist(get_vals(stats, "freq"), bins=bins,
             histtype='stepfilled',
             color='b', label="freq")
    configure_plot(title, "freq", days)


def configure_plot(title, kind, days):
    plt.title("%s %s for %d days" % (title, kind, days))
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()
    plt.draw()


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-d", "--days", default=50, dest="days",
                      help="Number of days, either 50 or 100. Default 50.")
    parser.add_option("-s", "--subnet",
                      action="store_false", dest="use_subnet", default=True,
                      help="compute subnet stats")

    parser.add_option("-a", "--all",
                      action="store_true", dest="compute_all", default=False,
                      help="use 50 and 100 day data")

    (options, args) = parser.parse_args()
    main(options.days, options.use_subnet, options.compute_all)
