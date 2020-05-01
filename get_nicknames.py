import ndjson
import requests

from collections import defaultdict

while True:
    tournamentId = raw_input("Enter tournament id: ")
    if tournamentId != '':
        break

while True:
    minimumGames = int(raw_input("Enter positive minimum number of games (usually 8): "))
    if minimumGames > 0:
        break

while True:
    minimumAverageMoves = int(raw_input("Enter minimum average number of two-side moves (usually 10): "))
    if minimumAverageMoves >= 0:
        break

games = requests.get(
    'https://lichess.org/api/tournament/' + tournamentId + '/games',
    headers={'Accept': 'application/x-ndjson'},
    params={'tags': 'false'}
).json(cls=ndjson.Decoder)

gamesPlayed = defaultdict(int)
movesPlayed = defaultdict(float)
for game in games:
    for color in 'white', 'black':
        player = game['players'][color]['user']['name']
        gamesPlayed[player] += 1
        movesPlayed[player] += len(game['moves'].split()) / 2.

tooFewGames = []
tooFewMoves = []
ok = []
for name in gamesPlayed:
    if gamesPlayed[name] < minimumGames:
        tooFewGames.append(name)
    elif movesPlayed[name] < minimumAverageMoves * gamesPlayed[name]:
        tooFewMoves.append(name)
    else:
        ok.append(name)
tooFewGames.sort()
tooFewMoves.sort()
ok.sort()

print
print('Players played at least 1 game: ' + str(len(gamesPlayed)))
print

if len(tooFewGames) != 0:
    print('=======================================================')
    print('Players played too few games: ' + str(len(tooFewGames)))
    for name in tooFewGames:
        print(name + ' ' + str(gamesPlayed[name]))
    print('=======================================================')
    print

if len(tooFewMoves) != 0:
    print('=======================================================')
    print('Players played too few moves: ' + str(len(tooFewMoves)))
    for name in tooFewMoves:
        print(name + ' ' + str(1. * movesPlayed[name] / gamesPlayed[name]))
    print('=======================================================')
    print

print('=======================================================')
print('Players meet criteria: ' + str(len(ok)))

for name in ok:
    print(name)
