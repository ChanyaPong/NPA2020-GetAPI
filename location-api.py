import requests
import urllib.request as request
import json
import time
import string

# Personal acess token
access_token = 'YmNmODU2NjgtMzY0Ny00NjgxLTkzNzItMjIwMDQ4ODNjNjc1YzI3MjBiNDEtYTA4_P0A1_c1cccb6a-5e2d-4f80-86f9-f0dcefbd12f8'
# Room WebEx space for me
room_id = 'Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vMDBkMWZlODAtNTg4Yy0xMWViLWJhOTEtMmYyZjkyZDI5YTMx'
# Room NPA2020 IT KMITL
# room_id = 'Y2lzY29zcGFyazovL3VzL1JPT00vNjA5Nzk5NDAtNTU3My0xMWViLWEzNzUtY2JkMGE4ZjAxYTA3'
# MapQuest Key
mapquest_key = 'BjrBow9vWa9goDG7zxKeQVeqMnJYk2Tp'

def GetMessage(access_token, room_id):
    """ Get message from WebEx """
    url = 'https://webexapis.com/v1/messages?roomId={}'.format(room_id)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }
    res = requests.get(url, headers=headers)
    markdown = res.json()["items"][0]["text"] # Dont forgot change 'text' to 'markdown'
    message_time = res.json()["items"][0]["created"]

    if markdown[0] == '/':
        return [markdown[1:], message_time]
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
 
def CreateMessage(access_token, room_id, latlon, markdown):
    """ Get ISS Location and send message to WebEx """
    with request.urlopen("http://api.open-notify.org/iss-pass.json?lat=" + latlon[0] + "&lon=" + latlon[1]) as response:
        source = response.read()
        data = json.loads(source)
    date = data['request']['datetime']
    dulation = data['response'][0]['duration']

    date = CovertSecond(date)
    date = PassDay(date, str(markdown[1]))

    message = "ISS will pass " + markdown[0] + " by " + str(date) + " duration " + str(dulation) + " second."
    url = 'https://webexapis.com/v1/messages'
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }
    params = {'roomId': room_id, 'markdown': message}
    requests.post(url, headers=headers, json=params)

    print("Message is \"%s\"."%message)

def CovertSecond(sec):
    """ Convert seconds to year, month, day, hours and minute """
    date = {"year":0, "month":0, "day":0, 'hours':0, "mins":0, "sec":sec}
    if date["sec"] >= 31556926:
        date["year"] = int(date["sec"]/312556926)
        date["sec"] = date["sec"]%312556926
    if date["sec"] >= 2629743:
        date["month"] = int(date["sec"]/2629743)
        date["sec"] = date["sec"]%2629743
    if date["sec"] >= 86400:
        date["day"] = int(date["sec"]/86400)
        date["sec"] = date["sec"]%86400
    if date["sec"] >= 3600:
        date["hours"] = int(date["sec"]/3600)
        date["sec"] = date["sec"]%3600
    if date["sec"] >= 60:
        date["mins"] = int(date["sec"]/60)
        date["sec"] = date["sec"]%60
    return date

def PassDay(date, text):
    """ Find Day what ISS Pass in this position """
    markdown = markdown.replace("-", " ").replace(":", " ").replace(".", " ").replace("T", " ").split() # Markdown = [year, month, day, hours, mins, sec]
    markdown.pop(-1)
    markdown[0] = str(int(markdown[0]) + date["year"])
    markdown[1] = str(int(markdown[1]) + date["month"])
    markdown[2] = str(int(markdown[2]) + date["day"])
    markdown[3] = str(int(markdown[3]) + date["hours"])
    markdown[4] = str(int(markdown[4]) + date["mins"])
    markdown[5] = str(int(markdown[5]) + date["sec"])
    return " ".join(markdown)

# Loop every 10 sec
while True:
    markdown = GetMessage(access_token, room_id) # markdown[0] = Message, markdown[1] = Time
    if markdown:
        latlon = GetLatLon(mapquest_key, markdown[0])
        CreateMessage(access_token, room_id, latlon, markdown)
        print("Send message to " " success!")
    else:
        print("None")
        time.sleep(5)
