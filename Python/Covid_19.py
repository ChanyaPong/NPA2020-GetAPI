import requests, json, string
import urllib.request as request
import time
import Message
import Location
import Marketstack

def GetCovidData(text):
    """ Get Covid Data from Country """
    url = 'https://covid-api.mmediagroup.fr/v1/cases?country=' + text
    with request.urlopen(url) as response:
       source = response.read()
       data = json.loads(source)["All"]

       return data

def CreateMessage(access_token, room_id, data):
    """ Send Message to WebEx Room """
    country = data["country"]
    message = "%s | Confirmed : %d\tRecovered : %d\tDeaths : %d"%(country, data["confirmed"], data["recovered"], data["deaths"])
    url = 'https://webexapis.com/v1/messages'
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }
    params = {'roomId': room_id[1], 'markdown': message}
    requests.post(url, headers=headers, json=params)

    print("Message : \"%s\""%message)

def CheckText(text, access_token, room_id):
    """ Check Message from WebEx Room """
    while True:
        text = Message.GetMessage(access_token, room_id)
        if text == "None" or text.lower() == "covid":
            continue
        elif text.lower() == "end":
            print("...................................Leave Covid-19 Mode")
            break
        # Location Mode
        elif text.lower() == "location":
            print("...................................Leave Covid-19 Mode")
            print(".........................................Location Mode")
            url = 'https://webexapis.com/v1/messages'
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-Type': 'application/json'
            }
            params = {'roomId': room_id[1], 'markdown': "Please Enter Location..."}
            requests.post(url, headers=headers, json=params)
            Location.CheckText(text, access_token, room_id)
        # Market Stack Mode
        elif text.lower() == "market":
            print("...................................Leave Covid-19 Mode")
            print(".....................................Market Stack Mode")
            url = 'https://webexapis.com/v1/messages'
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-Type': 'application/json'
            }
            params = {'roomId': room_id[1], 'markdown': "Please Enter Symbol..."}
            requests.post(url, headers=headers, json=params)
            Marketstack.CheckText(text, access_token, room_id)
        elif text:
            data = GetCovidData(text)
            CreateMessage(access_token, room_id, data)
            print("Send message to " + room_id[0] + " success!")
        time.sleep(5)
