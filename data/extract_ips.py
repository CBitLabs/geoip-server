import csv
import glob
import fileinput

IN_FILE = "*.csv"
OUT_FILE = "ip_list.csv"


def extract_ips(in_file=IN_FILE, out_file=OUT_FILE):
    ips = set([])
    with open(out_file, 'w') as f_out:
        inp = fileinput.input(glob.glob(in_file))
        reader = csv.reader(inp)
        for line in reader:
            try:
                ip = line[1]
                ssid = _get_ssid(line[2])
                row = "%s,%s" % (ip, ssid)
                ips.add(row)
            except IndexError:
                pass
        ips = filter(lambda ip: len(ip) > 1, ips)
        f_out.write("\n".join(ips))


def _get_ssid(dns_query):
    return dns_query.split(".")[5]

if __name__ == "__main__":
    extract_ips()
