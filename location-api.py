import requests
import urllib.request as request
import json
import time

access_token = 'MmNiNmFhMjItZTc3MS00YTE0LWFmYzMtZmQ2YWE4ZjhlNmNjZmRmYTQ5MDktOTJi_P0A1_c1cccb6a-5e2d-4f80-86f9-f0dcefbd12f8'
# Room WebEx space for me
room_id = 'Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vMDBkMWZlODAtNTg4Yy0xMWViLWJhOTEtMmYyZjkyZDI5YTMx'
# Room NPA2020 IT KMITL
# room_id = 'Y2lzY29zcGFyazovL3VzL1JPT00vNjA5Nzk5NDAtNTU3My0xMWViLWEzNzUtY2JkMGE4ZjAxYTA3'
mapquest_key = 'BjrBow9vWa9goDG7zxKeQVeqMnJYk2Tp'

def GetMessage(access_token, room_id):
    """ Get message every 1 min """
    url = 'https://webexapis.com/v1/messages?roomId={}'.format(room_id)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }
    res = requests.get(url, headers=headers)
    markdown = res.json()["items"][0]["text"] # Dont forgot change 'text' to 'markdown'

    if markdown[0] == '/':
        return markdown[1:]
    else:
        return 0

def GetLatLon(mapquest_key, markdown):
    """ Get Latitude and Longitude from Mapquest API """
    url = 'https://www.mapquestapi.com/geocoding/v1/address?key=' + mapquest_key + '&location=' + markdown
    with request.urlopen(url) as response:
        source = response.read()
        data = json.loads(source)
        
        lat = data["results"][0]["locations"][0]["displayLatLng"]["lat"]
        lon = data["results"][0]["locations"][0]["displayLatLng"]["lng"]
        
        return [str(lat), str(lon)]
 
def CreateMessage(access_token, room_id, latlon):
    with request.urlopen("http://api.open-notify.org/iss-pass.json?lat=" + latlon[0] + "&lon=" + latlon[1]) as response:
        source = response.read()
        data = json.loads(source)
    date = data[]
    dulation = data['response'][0]['duration']

    message = "ISS will pass " + markdown + " by " # + Date + Time + " duration " +  + "second"
    url = 'https://webexapis.com/v1/messages'
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }
    params = {'roomId': room_id, 'markdown': message}
    res = requests.post(url, headers=headers, json=params)

while True:
    markdown = GetMessage(access_token, room_id)
    if markdown:
        latlon = GetLatLon(mapquest_key, markdown)
        CreateMessage(access_token, room_id, latlon)
        print("Send message success!")
    else:
        print("None")
        time.sleep(10)
