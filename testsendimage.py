import requests
from requests.auth import HTTPBasicAuth
import os
from time import sleep
os.system("libcamera-jpeg -o tank.jpg -n")

url = 'https://smartfish.ddns.net/upload.php'
files = {'fileimage': open('tank.jpg', 'rb')}
response=requests.post(url, files=files,auth = HTTPBasicAuth('iot', 'fishtank'))
print(response.content)





