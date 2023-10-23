import requests
import urllib3
import time
import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ip = 'https://127.0.0.1:55795/lol-chat/v1/me'
headers = {'accept': 'application/json',
           'Authorization': 'Basic cmlvdDpYdm1ib1JYYnVIUE5vLW5aaGRNLU9n',
           'Content-Type': 'application/json'
           }
data1 = '{"statusMessage": "'
data2 = '"}'
old = datetime.datetime.now()
skipped = False
while(1):
    if datetime.datetime.now().second == old.second:
        if skipped == False:
            skipped = True
            time.sleep(.98)
        continue
    skipped = False

    old = datetime.datetime.now()

    hour = str(old.hour)
    minute = str(old.minute)
    second = str(old.second)
    
    bi = " am"

    if old.hour > 12:
        bi = " pm"
        hour = str(int(old.hour) - 12)
    if int(hour) < 10:
        hour = '0' + hour
    if old.minute < 10:
        minute = '0' + minute
    if old.second < 10:
        second = '0' + second
        
    status = hour + ':' + minute + ':' + second + bi
    data = data1 + status + data2
    r = requests.put(ip, verify=False, headers=headers, data=data)
    if r.status_code != 201:
        print(r.json())
    else:
        print(r.json()["statusMessage"])
