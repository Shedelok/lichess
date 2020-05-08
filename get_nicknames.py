import ndjson
import requests

from collections import defaultdict

MILLISECONDS_IN_MINUTE = 60000


def IDENTITY(x):
    return x


def readValue(message, mapper, checker):
    while True:
        result = mapper(raw_input(message))
        if checker(result):
            return result


tournamentId = readValue('Enter tournament id: ', IDENTITY, lambda (x): x != '')
minimumMinutes = readValue('Enter minimum number of minutes (usually 60): ', int, lambda (x): x >= 0)

games = requests.get(
    'https://lichess.org/api/tournament/' + tournamentId + '/games',
    headers={'Accept': 'application/x-ndjson'},
    params={'tags': 'false'}
).json(cls=ndjson.Decoder)


def countPlayerStat(f):
    result = defaultdict(int)
    for game in games:
        for color in 'white', 'black':
            player = game['players'][color]['user']['name']
            result[player] = f(result[player], game)
    return result


def countGamesPlayed():
    return countPlayerStat(lambda old, _: old + 1)


def countTimePlayedInMillis():
    return countPlayerStat(lambda old, game: old + game['lastMoveAt'] - game['createdAt'])


def getFirstGameStart():
    return countPlayerStat(lambda old, game: game['createdAt'] if old == 0 else min(old, game['createdAt']))


def getLastGameEnd():
    return countPlayerStat(lambda old, game: max(old, game['lastMoveAt']))


gamesPlayed = countGamesPlayed()
timePlayed = countTimePlayedInMillis()

tooFewMinutes = []
ok = []
for name in timePlayed:
    if timePlayed[name] < minimumMinutes * MILLISECONDS_IN_MINUTE:
        tooFewMinutes.append(name)
    else:
        ok.append(name)
tooFewMinutes.sort(key=lambda (x): timePlayed[x], reverse=True)
ok.sort()

print
print('Players played at least 1 game: ' + str(len(gamesPlayed)))
print('============================')
print

if len(tooFewMinutes) > 0:
    firstGameStart = getFirstGameStart()
    lastGameEnd = getLastGameEnd()
    print('Players played too few minutes: ' + str(len(tooFewMinutes)))
    print('============================')
    for name in tooFewMinutes:
        print(name + ' minutes: ' + str((1. * timePlayed[name]) / MILLISECONDS_IN_MINUTE) + ' games: '
              + str(gamesPlayed[name]) + ' minutes with pauses: '
              + str((1. * (lastGameEnd[name] - firstGameStart[name])) / MILLISECONDS_IN_MINUTE))
    print

print('Players meet criteria: ' + str(len(ok)))
print('============================')
for name in ok:
    print(name)
