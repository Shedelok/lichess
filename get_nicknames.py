import ndjson
import requests

from collections import defaultdict

tournamentId = raw_input("Enter tournament id: ")
minimumGames = int(raw_input("Enter minimum number of games: "))

requestUrl = 'https://lichess.org/api/tournament/' + tournamentId + '/games'

print("Requesting data from lichess...")
response = requests.get(requestUrl, headers = {'Accept' : 'application/x-ndjson'}, params = {'moves' : 'false', 'tags' : 'false'})
games = response.json(cls = ndjson.Decoder)

print("Counting games...")
gamesPlayed = defaultdict(int)
for game in games:
    players = game['players']
    for color in 'white', 'black':
        gamesPlayed[players[color]['user']['name']] += 1

print("Filtering by number of games...")
names = sorted(map(lambda (name, games): name, filter(lambda (name, games): games >= minimumGames, gamesPlayed.items())))

print
print("Players with at least " + str(minimumGames) + " games in tournament " + tournamentId + ":")
print

for name in names:
    print(name)

