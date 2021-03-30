import requests, json, string
import urllib.request as request
import datetime, time
import Message

# MapQuest Key
mapquest_key = 'BjrBow9vWa9goDG7zxKeQVeqMnJYk2Tp'

def GetMessage(access_token, room_id):
    """ Get message from WebEx """
    url = 'https://webexapis.com/v1/messages?roomId={}'.format(room_id[1])
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }
    res = requests.get(url, headers=headers)
    text = res.json()["items"][0]["text"]
    message_time = res.json()["items"][0]["created"]

    if text[0] == '/':
        return [text[1:], message_time]
    else:
        return 0

def GetLatLon(mapquest_key, text, access_token, room_id):
    """ Get Latitude and Longitude from Mapquest API """
    url = 'https://www.mapquestapi.com/geocoding/v1/address?key=' + mapquest_key + '&location=' + text.replace(" ","")
    with request.urlopen(url) as response:
        source = response.read()
        data = json.loads(source)
        
        lat = data["results"][0]["locations"][0]["displayLatLng"]["lat"]
        lon = data["results"][0]["locations"][0]["displayLatLng"]["lng"]

        url = 'https://webexapis.com/v1/messages'
        message = "%s : Latitude is %f, Longitude is %f."%(text, lat, lon)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token),
            'Content-Type': 'application/json'
        }
        params = {'roomId': room_id[1], 'markdown': message}
        requests.post(url, headers=headers, json=params)

        print(message)
        
        return [str(lat), str(lon)]
 
def CreateMessage(access_token, room_id, latlon, text):
    """ Get ISS Location and send message to WebEx """
    with request.urlopen("http://api.open-notify.org/iss-pass.json?lat=" + latlon[0] + "&lon=" + latlon[1]) as response:
        source = response.read()
        data = json.loads(source)
    date = data['request']['datetime']
    dulation = data['response'][0]['duration']

    date = datetime.datetime.fromtimestamp(date).strftime("%A, %B %d, %Y %I:%M:%S")

    message = "ISS will pass " + text + " by " + date + " duration " + str(dulation) + " seconds."
    url = 'https://webexapis.com/v1/messages'
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }
    params = {'roomId': room_id[1], 'markdown': message}
    requests.post(url, headers=headers, json=params)

    print("Message : \"%s\""%message)

def CheckText(text, access_token, room_id):
    while True:
        text = Message.GetMessage(access_token, room_id)
        if text == "None" or text.lower() == "location":
            continue
        elif text.lower():
            latlon = GetLatLon(mapquest_key, text, access_token, room_id)
            CreateMessage(access_token, room_id, latlon, text)
            print("Send message to " + room_id[0] + " success!")
        time.sleep(5)
