import requests, json, string
import urllib.request as request
import time
import Message
import Location
import Covid_19

# Market Stack Key
market_key = ''

def GetMarketData(market_key, text):
    """ Get Market Price on Marget Stack """
    # Get Name of Finance
    url = 'http://api.marketstack.com/v1/tickers?access_key=' + market_key + '&symbols=' + text
    response = requests.get(url)
    name = response.json()["data"][0]["name"]
    
    # Get Another Data
    url = 'http://api.marketstack.com/v1/eod?access_key=' + market_key + '&symbols=' + text
    response = requests.get(url)
    data = response.json()["data"][0]

    return [name, data]

def CreateMessage(access_token, room_id, market_data, text):
    """ Send Message to WebEx Room """
    date = market_data[1]["date"][:10]
    data = market_data[1]

    message = "%s | Date : %s\nOpen : %.2f$\tHigh : %.2f$\tLow : %.2f$\tClose : %.2f$"%(market_data[0], date, data["open"], data["high"], data["low"], data["close"])
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
        if text == "None" or text.lower() == "market":
            continue
        elif text.lower() == "end":
            print("...............................Leave Market Stack Mode")
            break
        # Location Mode
        elif text.lower() == "location":
            print("...............................Leave Market Stack Mode")
            print(".........................................Location Mode")
            url = 'https://webexapis.com/v1/messages'
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-Type': 'application/json'
            }
            params = {'roomId': room_id[1], 'markdown': "Please Enter Location..."}
            requests.post(url, headers=headers, json=params)
            Location.CheckText(text, access_token, room_id)
        # Covid-19 Mode
        elif text.lower() == "covid":
            print("...............................Leave Market Stack Mode")
            print(".........................................Covid-19 Mode")
            url = 'https://webexapis.com/v1/messages'
            headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'Content-Type': 'application/json'
            }
            params = {'roomId': room_id[1], 'markdown': "Please Enter Country..."}
            requests.post(url, headers=headers, json=params)
            Covid_19.CheckText(text, access_token, room_id)
        elif text:
            market_data = GetMarketData(market_key, text)
            CreateMessage(access_token, room_id, market_data, text)
            print("Send message to " + room_id[0] + " success!")
        time.sleep(5)
