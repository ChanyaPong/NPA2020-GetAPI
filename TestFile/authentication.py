import requests
import json

access_token = 'MmNiNmFhMjItZTc3MS00YTE0LWFmYzMtZmQ2YWE4ZjhlNmNjZmRmYTQ5MDktOTJi_P0A1_c1cccb6a-5e2d-4f80-86f9-f0dcefbd12f8'
url = 'https://webexapis.com/v1/people/me'
headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}
res = requests.get(url, headers=headers)
print(json.dumps(res.json(), indent=4))