import json
from stockfish import Stockfish

f = open("sample.json", "r")
data = json.loads(f.read())

for game in data:

