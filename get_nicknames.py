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
    minimumMoves = int(raw_input("Enter minimum number of two-side moves (usually 10): "))
    if minimumMoves >= 0:
        break

games = requests.get(
    'https://lichess.org/api/tournament/' + tournamentId + '/games',
    headers={'Accept': 'application/x-ndjson'},
    params={'tags': 'false'}
).json(cls=ndjson.Decoder)

gamesPlayed = defaultdict(int)
notCounted = defaultdict(list)
for game in games:
    isShort = len(game['moves'].split()) < minimumMoves * 2
    for color in 'white', 'black':
        if isShort and ('winner' not in game or game['winner'] != color):
            notCounted['https://lichess.org/' + game['id']].append(color)
            gamesPlayed[game['players'][color]['user']['name']] += 0
        else:
            gamesPlayed[game['players'][color]['user']['name']] += 1

names = sorted(map(lambda (name, games): name,
                   filter(lambda (name, games): games >= minimumGames, gamesPlayed.items())))

totalNotCounted = sum(map(lambda (link, sides): len(sides), notCounted.items()))

print
print('Players played at least 1 game: ' + str(len(gamesPlayed)))
print('Players meet criteria: ' + str(len(names)))
print('Total games played: ' + str(len(games)))
print('Not counted games: ' + str(totalNotCounted)
      + (' (' + str(100 * totalNotCounted / (len(games) * 2)) + '%)' if len(games) > 0 else ''))
print

for p in sorted(notCounted.items()):
    print(p[0] + ' ' + str(sorted(p[1])))
print

for name in names:
    print(name)
