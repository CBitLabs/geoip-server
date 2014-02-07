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

COLORS = ['b', 'g', 'r', 'c', 'm', 'y']

QUERY = """SELECT COALESCE(SUM(spam_count), 0),
                COALESCE(SUM(spam_freq), 0), 
                COALESCE(SUM(bot_count), 0), 
                COALESCE(SUM(bot_freq), 0), 
                COALESCE(SUM(unexp_count), 0), 
                COALESCE(SUM(unexp_freq), 0) 
            FROM ip_events_%(days)d WHERE address%(op)sINET '%(ip)s';"""

IN_FILE = "ip_list.csv"


def main(days, useSubnet):

    print "\nLoading ips..."
    ips = load_ips()

    print "\nBuilding stats..."
    ip_stats, subnet_stats = get_stats(ips, days, useSubnet)

    print "\nPrinting IP stats..."
    print_stats(ip_stats)

    if useSubnet:
        print "=" * 60

        print "\nPrinting subnet stats..."
        print_stats(subnet_stats)

    plt.show()


def load_ips(in_file=IN_FILE):
    with open(in_file) as f:
        reader = csv.reader(f)
        return [row[0] for row in reader]


def get_stats(ips, days, useSubnet):
    """walk through list of ip addresses and gather sum across events"""
    cur = get_cursor()
    ip_stats = {}
    subnet_stats = {}
    for i, ip in enumerate(ips):
        ip_stats[ip] = sum_query(cur, ip, "=", days)

        if useSubnet:
            subnet = get_subnet(ip)
            subnet_stats[subnet] = sum_query(cur, subnet, "<<", days)

        if not i % 100:
            print "Queried %d rows." % i

    plot_stats("IP stats", ip_stats)

    if useSubnet:
        plot_stats("subnet stats", subnet_stats)

    return ip_stats, subnet_stats


def get_cursor(auth=AUTH):
    conn = pg.connect("dbname=%(dbname)s user=%(user)s password=%(password)s"
                      % AUTH)

    return conn.cursor()


def sum_query(cur, ip, op, days):
    query = make_query(ip, op, days)
    cur.execute(query)

    rows = cur.fetchall()
    assert len(rows) == 1
    return as_dict(rows[0])


def make_query(ip, op, days):
    return QUERY % {
        'ip': ip,
        'op': op,
        'days': days
    }


def as_dict(row):
    return {k: v for k, v in zip(EVENTS, row)}


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

    # get event stats
    for event in EVENTS:
        vals = get_vals(stats, event)
        print_dict_stat("max", event, *get_max(stats, event))
        print_dict_stat("min", event, *get_min(stats, event))
        print_float_stat("avg", event, get_avg(vals))
        print_float_stat("stdev", event, get_stdev(vals))
        print_percent_stat("zeros", event, get_zero_percent(vals))
        print

    print "-" * 60 + "\n"
    # get tot stats
    print_tot_stats("freq", sum_freq(stats))
    print_tot_stats("count", sum_count(stats))


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
    return round(num_zeros / float(len(stats)), 2)


def plot_stats(title, stats):
    plt.figure()
    bins = len(stats) / 100
    plt.hist(sum_count(stats), bins=bins,
             histtype='stepfilled',
             color='r', label="count")

    plt.hist(sum_freq(stats), bins=bins,
             histtype='stepfilled',
             color='b', label="freq")

    plt.title(title)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()
    plt.draw()


def sum_count(stats):
    return sum_stats(get_to_zip(stats, "freq"))


def sum_freq(stats):
    return sum_stats(get_to_zip(stats, "count"))


def get_to_zip(stats, keyword):
    return [get_vals(stats, e) for e in EVENTS if keyword in e]


def sum_stats(to_zip, ):
    return map(sum, zip(*to_zip))


def get_vals(stats, event):
    return map(lambda kv: kv[1][event], stats.iteritems())

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-d", "--days", default=50, dest="days",
                      help="Number of days, either 50 or 100. Default 50.")
    parser.add_option("-s", "--subnet",
                      action="store_false", dest="useSubnet", default=True,
                      help="compute subnet stats")

    (options, args) = parser.parse_args()
    main(options.days, options.useSubnet)
