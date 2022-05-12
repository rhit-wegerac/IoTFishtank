# This is the general logger for the fish tank program.
import os,time
from datetime import datetime
logfile=""
#INIT the logger
def init_logger(file):
   global logfile
   time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
   if(not os.path.exists(file)):
       open(file,"w+").write("======== [ LOG CREATION: "+str(time)+" ] ========\n")
   else:
   	open(file,"a").write("======== [ RESTART: "+time+" ] ========\n")
   logfile=file
# Set the log file
def set_logfile(file):
   global logfile
   time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
   logfile=file
   if(not os.path.exists(file)):
       print("[LOGGER] : NOTE: Creating non-existant logfile: "+str(file))
       open(file,"w+").write("======== [ LOG CREATION: "+str(time)+" ] ========\n")
# Log an error
def log_err(caller,text):
    global logfile
    time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    os.system("tput setaf 1")
    open(logfile,"a").write("["+str(time)+"]["+caller+"] : ERROR : "+text+"\n")
    print("["+caller+"] : ERROR: "+text)
    os.system("tput setaf 7")
# Log an info
def log_info(caller,text):
    global logfile
    time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    os.system("tput setaf 12")
    open(logfile,"a").write("["+str(time)+"]["+caller+"] : NOTE: "+text+"\n")
    print("["+caller+"] : "+text)
    os.system("tput setaf 7")
# Log a warning
def log_warn(caller,text):
    global logfile
    time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    os.system("tput setaf 11")
    open(logfile,"a").write("["+str(time)+"]["+caller+"] : WARN:"+text+"\n")
    print("["+caller+"] : WARN: "+text)
    os.system("tput setaf 7")
