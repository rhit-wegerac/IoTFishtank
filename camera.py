import requests
from requests.auth import HTTPBasicAuth
import os
from time import sleep
import subprocess
logger=None
MY_NAME="CAM"
def set_logger(l):
	global logger
	logger=l
	l.log_info(MY_NAME,"logger linked!")
def take_pic(dummy):
	global logger
	logger.log_info(MY_NAME,"Taking picture...")
#	subprocess.check_output("/usr/bin/libcamera-jpeg -o tank.jpg -n --immediate",shell=True)
	os.system("libcamera-jpeg -o tank.jpg --immediate -n")
	logger.log_info(MY_NAME,"Uploading picture...")

	url = 'https://smartfish.ddns.net/upload.php'
	files = {'fileimage': open('tank.jpg', 'rb')}
	response=requests.post(url, files=files,auth = HTTPBasicAuth('iot', 'fishtank'))
	logger.log_info(MY_NAME,"Uploaded with response: "+str(response))
	return



