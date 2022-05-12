# SPDX-FileCopyrightText: 2019 Mikey Sklar for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import glob
import time
import traceback
MY_NAME = "TEMP"
logger = None
def set_logger(l):
    global logger
    logger = l
    l.log_info(MY_NAME,"Logger linked!")
try:
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
except:
    try:
        logger.log_err(MY_NAME,"Unable to find device!")
    except:
        print("[TEMP] : Unable to find device!")
        print("[TEMP] : WARN: No logger initialized! Error will be lost!")
#    print("[TEMP] : Temp Failure: Unable to find device!")
#    exit(1)

def read_temp_raw():
    global logger
    try:
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
    except Exception as ex:
#        print("[TEMP] : Failed to Read RAW Temp! : "+str(ex))
        logger.log_err(MY_NAME,"Failed to read RAW temp! : "+str(ex))
def read_temp():
    try:
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c, temp_f
    except Exception as ex:
#        print("[TEMP] : Failed to Read Temp! : "+str(ex))
        logger.log_err(MY_NAME,"Failed to read temp! : " + str(ex))
#while True:
#    print(read_temp())
#    time.sleep(1)
#def __init__(self):
#	print("Temp Init.")
print("[TEMP] : Temp sensor started!")
