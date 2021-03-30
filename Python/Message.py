import requests, json
import urllib.request as request

def GetMessage(access_token, room_id):
    """ Get message from WebEx """
    url = 'https://webexapis.com/v1/messages?roomId={}'.format(room_id[1])
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }
    res = requests.get(url, headers=headers)
    text = res.json()["items"][0]["text"]

    if text[0] == '/':
        return text[1:]
    else:
        return "None"