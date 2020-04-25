import re

from stockfish import Stockfish
from flask import Flask
from flask import request

app = Flask(__name__)

stockfish = Stockfish('/usr/games/stockfish')
stockfish.set_skill_level(10)

def eval(self):
    self.stockfish.stdin.write(f"eval\n")
    self.stockfish.stdin.flush()
    text = self.stockfish.stdout.readline().strip()
    while True:
        text = self.stockfish.stdout.readline().strip()
        if text.startswith("Total Evaluation"):
            return re.findall(r"[-+]?\d*\.\d+|\d+", text)[0]
            break

Stockfish.eval = eval

@app.route('/best_move', methods=['POST', 'GET'])
def best_move():
    moves = request.args.get('moves', '').split(',')
    stockfish.set_position(moves)
    return { "best_move": stockfish.get_best_move() }

@app.route('/eval', methods=['POST', 'GET'])
def eval():
    moves = request.args.get('moves', '').split(',')
    stockfish.set_position(moves)
    return { "eval": stockfish.eval() }
