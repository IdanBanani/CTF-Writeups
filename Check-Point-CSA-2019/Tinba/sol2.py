import datetime
import os
import re

TINBA_IP = "216.218.185.162"
FW_FILE = "fw.log"
TIME_SYNTAX = "%Y-%m-%d %H:%M:%S"

unique_infected_machines = []

print(os.getcwd())
count = 0
with open(FW_FILE, "r") as fw_log:
    fw_log.readline()
    outbound_connection_row = fw_log.readline()
    while outbound_connection_row:
        outbound_connection_row = outbound_connection_row.replace("\n", "")
        ftime, src_ip, dst_ip = re.split(r'\t+', outbound_connection_row)

        ftime = datetime.datetime.strptime(ftime, TIME_SYNTAX)

        if (ftime.hour / 12 >= 1 and ftime.hour % 12 >= 6) or (ftime.hour / 12 < 1 and ftime.hour < 6):
            if dst_ip == TINBA_IP:
                count += 1
                if not src_ip in unique_infected_machines:
                    unique_infected_machines.append(src_ip)
                    print(unique_infected_machines)

        outbound_connection_row = fw_log.readline()

print('Count is: ', count)
print(unique_infected_machines)
print("length of infected machiness: " + str(len(unique_infected_machines)))
