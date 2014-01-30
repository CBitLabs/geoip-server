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
                ips.add(line[1])
            except IndexError:
                pass
        ips = filter(lambda ip: len(ip) > 0, ips)
        f_out.write(",\n".join(ips))

if __name__ == "__main__":
    extract_ips()
