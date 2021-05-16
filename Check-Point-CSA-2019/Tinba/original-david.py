from collections import defaultdict
from datetime import datetime
import operator

ranges = [(datetime.strptime('2019-05-27 18:00:00', '%Y-%m-%d %H:%M:%S'),
           datetime.strptime('2019-05-28 06:00:00', '%Y-%m-%d %H:%M:%S')),
          (datetime.strptime('2019-05-28 18:00:00', '%Y-%m-%d %H:%M:%S'),
           datetime.strptime('2019-05-29 06:00:00', '%Y-%m-%d %H:%M:%S'))]

common_ips = defaultdict(int)
ips_in_range = defaultdict(int)

print
"Counting..."

with open("fw.log") as f:
    for line in f:
        try:
            date, time, src_ip, dest_ip = line.split()
            common_ips[dest_ip] += 1

            entry_time = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S')
            for (start_time, end_time) in ranges:
                if start_time <= entry_time < end_time:
                    ips_in_range[dest_ip] += 1
        except:
            pass

print
"Sorting..."

sorted_common_ips = sorted(common_ips.items(), key=operator.itemgetter(1), reverse=True)

print
"Result:"

for ip, count in sorted_common_ips[:5]:
    print
    "DST IP: {}\tTotal Count: {}\tCount in Range: {}".format(ip, count, ips_in_range[ip])