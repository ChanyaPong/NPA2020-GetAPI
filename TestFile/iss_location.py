import requests
import urllib.request as request
import json
import time

""" Get ISS Location and send message to WebEx """
with request.urlopen("http://api.open-notify.org/iss-pass.json?lat=39.738453&lon=-104.984853") as response:
    source = response.read()
    data = json.loads(source)
print(data)