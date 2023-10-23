import requests
import bisect
import time
import random

MATCHLENGTHTHRESHOLD = 50
KEYS = ["RGAPI-...",
        "RGAPI-...",
        "RGAPI-...",
        "RGAPI-..."]
APIDELAY = 1200
TIMERSNA1 = [0,0,0,0]
TIMERSAMERICA = [0,0,0,0]
OLDESTGAME = 4794218107
OUTFILE = "C:/Users/junsu/Desktop/leagueai2/out3.txt"


def checkRank(summonerId, keyUsed):
    key, _ = getKey(0, keyUsed)
    playerInfo = requests.get("https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + summonerId + "?api_key=" + key)
    if playerInfo.status_code != 200:
        print("checkRank", playerInfo.json())
        return False
    playerInfoJson = playerInfo.json()
    for league in playerInfoJson:
        if league["queueType"] != "RANKED_SOLO_5x5":
            continue
        else:
            match league["tier"]:
                case "IRON":
                    return False
                case "BRONZE":
                    return False
                case "SILVER":
                    return False
            return True
    return False


def getMatchData(match):
    key, keyUsed = getKey(1, None)
    matchData = requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/NA1_" + str(match) + "?api_key=" + key)
    if matchData.status_code != 200:
        print("getMatchData", matchData.json(), "https://americas.api.riotgames.com/lol/match/v5/matches/NA1_" + str(match) + "?api_key=" + key)
        return None, keyUsed

    return matchData.json(), keyUsed


def getGames(matchList, usedList, ids, keyUsed):
    for id in ids:
        if checkRank(id[1], keyUsed):
            print("Getting additional games from user: ", id[2])
            matchHistory = playerMatchHistory(id[0], keyUsed)
            for playerMatch in matchHistory:
                # more efficient check case for optimizing required
                matchid = int(playerMatch[4:])
                if  matchid > OLDESTGAME and matchid not in matchList and matchid not in usedList:
                    bisect.insort(matchList, matchid)

def playerMatchHistory(puuid, keyUsed):
    key, _ = getKey(1, keyUsed)
    data = requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?queue=420&start=0&count=20&api_key="+key)
    if data.status_code != 200:
        print("playerMatchHistory", matchData.json())
        return None
    return data.json()

def saveMatchData(data):
    dataOut = ""

    champs = []
    for i in range(10):
        champs.append(data["participants"][i]["championId"])

    # swap sides to keep winning team first
    if not data["teams"][0]["win"]:
        champs = champs[5:] + champs[:5]

    for champ in champs:
        dataOut += str(champ) + ','

    dataOut = dataOut[:-1] + '\n'

    with open(OUTFILE, "ab") as file:
        file.write(dataOut.encode("ascii"))
        file.close()

def getKey(server, keyUsed):
    while(True):
        currentTime = int(time.time() * 1000)
        if server == 0:
            for i in range(len(KEYS)):
                if keyUsed is not None and keyUsed != i:
                    continue
                if currentTime > TIMERSNA1[i] + APIDELAY:
                    TIMERSNA1[i] = currentTime
                    return KEYS[i], i
        else:
            for i in range(len(KEYS)):
                if keyUsed is not None and keyUsed != i:
                    continue
                if currentTime > TIMERSAMERICA[i] + APIDELAY:
                    TIMERSAMERICA[i] = currentTime
                    return KEYS[i], i

def main():
    globalMatches = [4795636804]
    globalExhaustedMatches = []
    while(True):

        # pop one game from global list
        match = globalMatches.pop()

        # append popped game to used list
        if len(globalExhaustedMatches) > 1000:
            globalExhaustedMatches.pop(0)
        bisect.insort(globalExhaustedMatches, match)

        # get the match
        matchInfo, keyUsed = getMatchData(match)
        if matchInfo is None:
            continue

        # get some extra games if list is running short
        if len(globalMatches) < MATCHLENGTHTHRESHOLD:
            listOfPlayersInGame = []
            listOfParticipants = matchInfo["info"]["participants"]
            for participant in listOfParticipants:
                if random.random() < .3:
                    listOfPlayersInGame.append((participant["puuid"], participant["summonerId"], participant["summonerName"]))
            getGames(globalMatches, globalExhaustedMatches, listOfPlayersInGame, keyUsed)

        print(matchInfo["metadata"]["matchId"])
        saveMatchData(matchInfo["info"])
        
main()
