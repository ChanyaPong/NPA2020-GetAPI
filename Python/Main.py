import requests, json, string, time
import urllib.request as request
import Message
import Location

# Personal acess token = ZGFkODEwZWMtZDE5Ny00YmMxLWI0ODItM2Y4NGM1ODQ5ZTI4NGM4YzE3MGQtMTM1_P0A1_c1cccb6a-5e2d-4f80-86f9-f0dcefbd12f8
access_token = input("Enter Personal Access Token : ")
# Room Webex Team
room_id = { 0: ["Webex space for Chanya", "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vMDBkMWZlODAtNTg4Yy0xMWViLWJhOTEtMmYyZjkyZDI5YTMx"],
            1: ["NPA2020@ITKMITL", "Y2lzY29zcGFyazovL3VzL1JPT00vNjA5Nzk5NDAtNTU3My0xMWViLWEzNzUtY2JkMGE4ZjAxYTA3"]}
print("Please select your room :\n\t[0] : Webex space for Chanya\n\t[1] : NPA2020@ITKMITL")
room_id = room_id[int(input("Select your room : "))]

while True:
    text = Message.GetMessage(access_token, room_id)
    if text == "None":
        continue
    elif text.lower() == "location":
        print(".........................................Location Mode")
        url = 'https://webexapis.com/v1/messages'
        headers = {
            'Authorization': 'Bearer {}'.format(access_token),
            'Content-Type': 'application/json'
        }
        params = {'roomId': room_id[1], 'markdown': "Please Enter Location..."}
        requests.post(url, headers=headers, json=params)
        Location.CheckText(text, access_token, room_id)
    time.sleep(5)
