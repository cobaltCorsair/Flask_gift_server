from pprint import pprint
import requests
from app_crud import UpdateTables

resp = requests.get('https://dis.f-rpg.me/api.php?method=users.get&group_id=1,5,11&limit=500')
# print(resp.status_code)
# pprint(resp.json())
answer = resp.json()
# print(answer['response']['users'])
for key in answer['response']['users']:
    print(key['username'], key['user_id'])
    UpdateTables.add_new_user(key['username'], key['user_id'])
