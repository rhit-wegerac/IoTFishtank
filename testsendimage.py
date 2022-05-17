


import requests
import json

url = "https://content.dropboxapi.com/2/files/upload"


headers = {
    "Authorization": "Bearer <TOKEN>",
    "Content-Type": "application/octet-stream",
    "Dropbox-API-Arg": "{\"path\":\"/image.jpg\",\"mode\":{\".tag\":\"overwrite\"}}"
}
data = open("image.jpg","rb").read()
r = requests.post(url, headers=headers,data=data)
print(r.content)

url = "https://api.dropboxapi.com/2/files/get_temporary_link"

headers = {
    "Authorization": "Bearer <TOKEN>",
    "Content-Type": "application/json"
}

data = {
    "path": "/image.jpg"
}

r = requests.post(url, headers=headers, data=json.dumps(data))
print(r.content.json())
