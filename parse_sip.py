#!/usr/bin/python3

"""
Calculate MOS score in a SIP call log and output a csv with the same filename
"""

import sys
import pandas as pd
import mos_score as mos
import time
from datetime import date

def txt(filename = "", colname = "MOS Score"):
    if (filename):
        if len(filename.split('_')) == 4:
            log_date = filename.split('_')[3][:10] #YYYY-MM-DD
        else:
            # use today
            log_date = date.today().strftime("%Y-%m-%d")
        
        with open(filename, 'r') as fp:
            line = fp.readline()
            with open(filename + ".csv", 'w') as emtpy_csv:
                pass
            prevline = ""
            cnt = 1
            RX = False
            latency = ""
            jitter = ""
            loss = ""
            col = []
            timestamp = 0

            while line:
                if ("pjsua_app_common.c !" in line):
                    log_time = line.split()[0]
                    time_struct = time.strptime(log_date + "-" + log_time,  "%Y-%m-%d-%H:%M:%S.%f")
                    timestamp = time.mktime(time_struct) + float('0.' + log_time.split('.')[-1])
                if ("Call time:" in line):
                    row = ""
                    latency = ""
                    jitter = ""
                    loss = ""
                if ("RX " in line):
                    RX = True
                if ("TX " in line):
                    RX = False
                if RX:
                    if ("pkt loss" in line):
                        split_line = line.split()
                        loss = split_line[2][1:-3]
                    if ("jitter" in line):
                        split_line = line.split()
                        jitter = split_line[3]
                if ("RTT" in line):
                    split_line = line.split()
                    latency = split_line[4]
                    mos_value = mos.calculate_mos(latency, jitter, loss, timestamp)
                    col.append(str(mos_value))
                if ("DISCONNECTED" in line or ".PJSUA destroyed" in line):
                    try:
                        csv_input = pd.read_csv(filename + ".csv")
                    except pd.errors.EmptyDataError:
                        fr = pd.DataFrame(col, columns=[colname])
                        fr.to_csv(filename + ".csv", index=False)
                    else:
                        csv_input[colname] = pd.Series(col)
                        csv_input.to_csv(filename + ".csv", index=False)
                
                prevline = line
                line = fp.readline()
                cnt += 1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if len(sys.argv) == 2:
            txt(sys.argv[1])
        elif len(sys.argv) == 3:
            txt(sys.argv[1], sys.argv[2])
        else:
            print("Incorrect Args")
    else:
        print("Please specify file name.")
    