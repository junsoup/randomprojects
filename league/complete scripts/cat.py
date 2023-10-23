import requests
import time
import urllib3
import json
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# eyJraWQiOiJzMSIsImFsZyI6IlJTNTEyIn0.eyJzY3AiOiJMT0wiLCJzdWIiOiI4MWFlMmY0ZS03NjIwLTVlNGYtYjZkMS0yOGMzODM1YmM2ZmEiLCJwcm9kdWN0IjoiTE9MIiwibGlkIjoiOXJCcktORVUyS1czZm1fMjB5em9TdyIsImNuYW1lIjoibGN1IiwiaGJjIjoidXNhIiwiYWN0aWQiOjIwNzQ2NzYxNCwiaXNzIjoiaHR0cHM6XC9cL3Nlc3Npb24uZ3BzcnYucHZwLm5ldCIsInJpZCI6IjBNeF9pMVRHT1ZjIiwicmZhIjoxNjg0ODA5MDMxLCJzaWQiOiI5NGQ5YWNkYS01ODFlLTRhZjMtODk1Ni03NWU4ZmY1ODkyNGEiLCJieXBhc3MiOmZhbHNlLCJmZWRlcmF0ZWRfaWRlbnRpdHlfcHJvdmlkZXJzIjpbXSwicmVnIjoiTkExIiwiZGF0Ijp7InIiOiJOQTEiLCJ1IjoyMDc0Njc2MTR9LCJyZm8iOjM0NCwiZXhwIjoxNjg0ODA5Mjg3LCJpYXQiOjE2ODQ4MDg2ODcsImp0aSI6IjBiYjc1MWI5LWEzNDYtNGUwYS1hZjkwLTAyYTAwMzU3ZDFlNiIsImNpZCI6Imxzc19sb2wiLCJzaXQiOjE2ODQ4MDcwODN9.UmUtBzD5RZLH6_pLdOl7zYlOtwabsdb68za-Ho_xjMWGNpdK04pj-o867qLGmjV0zD14aZslVaeoKqx9hc9zmZo0miDPfaNE_cShkMK9H-DjjE43-8ixy4087ce6zPSJPBhUF1ajTHln2n5pIB_d7K39IZpwO7yjWaKG7G4g52QXCWXkSUg3r_lUeUwhGGZjWAHMiDChVaXmaXvC_JD4SXs7FOe-q-riMwTkR1FoyOEY6sErRIOv87SyjKeDIvALI2mFaL1YJFrzogZyRgSWOoSl78on9Z_2OROeFjAKUsIW6wOunRTtT8nraOIi42m39MG_ELt3l1qygWTyy5_JgA
# Access
ip = 'https://127.0.0.1:50351/lol-chat/v1/me'
headers = {'accept': 'application/json',
           'Authorization': 'Basic cmlvdDpuRV9JalRhdjZ3ODBOUlp2MGVIWDNB',
           'Content-Type': 'application/json'
           }

dataText = {"statusMessage": ""}
emotions = ["/ᐠ • □ • ᐟ\\ﾉ",  
            "/ᐠ . ‸ . ᐟ\\ﾉ",
            "/ᐠ . _ . ᐟ\\ﾉ",
            "/ᐠ • ˰ • ᐟ\\ﾉ",
            "/ᐠ • ᴗ • ᐟ\\ﾉฅ"]
feeling = 2

while(1):
    time.sleep(3)
    feelingDelta = random.randint(-1,1)
    if feelingDelta == 0:
        continue
    feeling += feelingDelta
    feeling = max(feeling, 0)
    feeling = min(feeling, 4)
    out = {"statusMessage": emotions[feeling]}
    data = json.dumps(out, ensure_ascii=False).encode('utf-8')
    r = requests.put(ip, verify=False, headers=headers, data=data)
    if r.status_code != 201:
        print(r.json())
    else:
        print(r.json()["statusMessage"])
