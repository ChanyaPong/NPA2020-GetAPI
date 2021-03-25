import requests

access_token = 'MmNiNmFhMjItZTc3MS00YTE0LWFmYzMtZmQ2YWE4ZjhlNmNjZmRmYTQ5MDktOTJi_P0A1_c1cccb6a-5e2d-4f80-86f9-f0dcefbd12f8'
room_id = 'Y2lzY29zcGFyazovL3VzL1JPT00vNjA5Nzk5NDAtNTU3My0xMWViLWEzNzUtY2JkMGE4ZjAxYTA3'
person_email = 'new-user@example.com'
url = 'https://webexapis.com/v1/memberships'
headers = {
 'Authorization': 'Bearer {}'.format(access_token),
 'Content-Type': 'application/json'
 }
params = {'roomId': room_id, 'personEmail': person_email}
res = requests.post(url, headers=headers, json=params)
print(res.json())
