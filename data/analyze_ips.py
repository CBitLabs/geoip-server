"""
    query datadump in ip_events postgres table from ip_stats hadoop job
    to find data to contruct pipeline
"""

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

QUERY = """SELECT COALESCE(SUM(spam_count), 0), 
                COALESCE(SUM(spam_freq), 0), 
                COALESCE(SUM(bot_count), 0), 
                COALESCE(SUM(bot_freq), 0), 
                COALESCE(SUM(unexp_count), 0), 
                COALESCE(SUM(unexp_freq), 0) 
            FROM ip_events WHERE address%(op)sINET '%(ip)s';"""

IN_FILE = "ip_list.csv"


def main():

    print "\nLoading ips..."
    ips = load_ips()

    print "\nBuilding stats..."
    ip_stats, subnet_stats = get_stats(ips)

    print "\nPrinting IP stats..."
    print_stats(ip_stats)

    print "="*60

    print "\nPrinting subnet stats..."
    print_stats(subnet_stats)


def load_ips(in_file=IN_FILE):
    with open(in_file) as f:
        reader = csv.reader(f)
        return [row[0] for row in reader]


def get_stats(ips):
    """walk through list of ip addresses and gather sum across events"""
    cur = get_cursor()
    ip_stats = {}
    subnet_stats = {}
    for i, ip in enumerate(ips):
        ip_stats[ip] = sum_query(cur, ip, "=")
        subnet = get_subnet(ip)
        subnet_stats[subnet] = sum_query(cur, subnet, "<<")

        if not i % 100:
            print "Queried %d rows." % i

    return ip_stats, subnet_stats


def get_cursor(auth=AUTH):
    conn = pg.connect("dbname=%(dbname)s user=%(user)s password=%(password)s"
                      % AUTH)

    return conn.cursor()


def sum_query(cur, ip, op):
    query = make_query(ip, op)
    cur.execute(query)

    rows = cur.fetchall()
    assert len(rows) == 1
    return as_dict(rows[0])


def make_query(ip, op):
    return QUERY % {
        'ip': ip,
        'op': op
    }


def as_dict(row):
    return {k: v for k, v in zip(EVENTS, row)}

def get_subnet(ip):
    return ".".join(ip.split(".")[:-1]) + "/24"

def print_stats(ip_stats):
    """
        dictionary of form {
            'ip' : {
                ROW
            }
        }

    print the min, max, avg type of each event for each ip
    print the number of ips with no events
    """
    for event in EVENTS:
        print_int_stat("max", event, *get_max(ip_stats, event))
        print_int_stat("min", event, *get_min(ip_stats, event))
        print_float_stat("avg", event, get_avg(ip_stats, event))
        print_float_stat("stdev", event, get_stdev(ip_stats, event))
        print


def print_int_stat(stat, event, ip, stats_dict):

    val = stats_dict[event]
    print "%s of %s from %s is %d." % (stat, event, ip, val)


def print_float_stat(stat, event, val):
    print "%s of %s is %03f." % (stat, event, val)


def get_max(ip_stats, event):
    return max(ip_stats.iteritems(), key=lambda kv: kv[1][event])


def get_min(ip_stats, event):
    return min(ip_stats.iteritems(), key=lambda kv: kv[1][event])


def get_avg(ip_stats, event):
    return sum(
        map(
            lambda kv: kv[1][event], ip_stats.iteritems())) / float(len(ip_stats))


def get_stdev(ip_stats, event):
    vals = map(lambda kv: kv[1][event], ip_stats.iteritems())
    return np.std(vals)


if __name__ == "__main__":
    main()
