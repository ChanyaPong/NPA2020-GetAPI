import requests
import urllib.request as request
import json

access_token = 'MmNiNmFhMjItZTc3MS00YTE0LWFmYzMtZmQ2YWE4ZjhlNmNjZmRmYTQ5MDktOTJi_P0A1_c1cccb6a-5e2d-4f80-86f9-f0dcefbd12f8'
# Room WebEx space for me
room_id = 'Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vMDBkMWZlODAtNTg4Yy0xMWViLWJhOTEtMmYyZjkyZDI5YTMx'
# Room NPA2020 IT KMITL
# room_id = 'Y2lzY29zcGFyazovL3VzL1JPT00vNjA5Nzk5NDAtNTU3My0xMWViLWEzNzUtY2JkMGE4ZjAxYTA3'

with request.urlopen('http://data.nba.net/prod/v2/2018/teams.json') as response:
    source = response.read()
    data = json.loads(source)

def GetMessage(access_token, room_id):
    """ Get message every 1 min """
    url = 'https://webexapis.com/v1/messages?roomId={}'.format(room_id)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }
    res = requests.get(url, headers=headers)
    print(res.json())
    markdown = res.json()["items"][0]["text"] # Dont forgot change 'text' to 'markdown'

    print(markdown) # Last Update

def GetLatLon():
    """ Get Latitude and Longitude from Mapquest API """

GetMessage(access_token, room_id)