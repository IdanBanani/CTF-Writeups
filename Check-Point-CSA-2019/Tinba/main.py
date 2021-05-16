from collections import defaultdict
from datetime import datetime
import operator

ranges = [(datetime.strptime('2019-05-27 18:00:00', '%Y-%m-%d %H:%M:%S'),
           datetime.strptime('2019-05-28 06:00:00', '%Y-%m-%d %H:%M:%S')),
          (datetime.strptime('2019-05-28 18:00:00', '%Y-%m-%d %H:%M:%S'),
           datetime.strptime('2019-05-29 06:00:00', '%Y-%m-%d %H:%M:%S'))]

dest_conn = defaultdict(int)
ips_in_range = defaultdict(set)

print("Counting...")

with open("fw.log") as f:
    for line in f:
        try:
            date, time, src_ip, dest_ip = line.split()
            entry_time = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S')
            for start_time, end_time in ranges:
                # if start_time <= entry_time <= end_time:
                if start_time < entry_time < end_time:
                    # dest_conn[dest_ip] += 1
                    ips_in_range[dest_ip].add(src_ip)

        except:
            pass

print("Sorting...")

# sorted_common_ips = sorted(dest_conn.items(), key=operator.itemgetter(1), reverse=True)
# sorted_common_ips = sorted(ips_in_range.items(), key=operator.itemgetter(1), reverse=True)

top_candidates = sorted(ips_in_range.items(), key=lambda x: len(x[1]), reverse=True)
top5 = top_candidates[:5]
print(top5)
# top_dest_ip = sorted_common_ips[:1000]
#
# with open("fw.log") as f:
#     for line in f:
#         try:
#             date, time, src_ip, dest_ip = line.split()
#             if dest_ip in dest_conn:

        #
        #
        #
        # except:
        #     pass

    # print(ips_in_range)
print("Result:")
# for ip, count in top_dest_ip:
#     if len(ips_in_range[ip]):
#         print("IP: {}\tTotal Count: {}\tCount in Range: {}".format(ip, count, len(ips_in_range[ip])))

