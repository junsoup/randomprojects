from lcu_connector import Connector

conn = Connector(start=True)

res = conn.get('/lol-summoner/v1/current-summoner')
print(res.json())