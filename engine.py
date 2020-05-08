import re

from stockfish import Stockfish
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

LEVEL = 18

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

@app.route('/engine/report', methods=['POST', 'GET'])
def report():
    global LEVEL
    stockfish = Stockfish('/usr/games/stockfish')
    stockfish.set_skill_level(LEVEL)
    moves = request.args.get('moves', '').split(',')
    ret = []
    for i in range(len(moves)):
        move = moves[i]
        stockfish.set_position(moves[0:i+1])
        move_eval = stockfish.eval()
        best_move = stockfish.get_best_move()
        item = { "index": i, "move": move, "eval": move_eval, "best_move": best_move }
        if i > 0 and move == ret[-1]["best_move"]:
            item["match"] = True
        else:
            item["match"] = False
        ret.append(item)

    return jsonify({"moves": ret})


@app.route('/engine/position', methods=['POST', 'GET'])
def position():
    global LEVEL
    stockfish = Stockfish('/usr/games/stockfish')
    stockfish.set_skill_level(LEVEL)
    moves = request.args.get('moves', '').split(',')
    index = request.args.get('index', '')
    if index:
        index = int(index)
        index = min(index, len(moves) - 1)
        moves = moves[0:(index + 1)]
    else:
        index = len(moves) - 1
    stockfish.set_position(moves)
    return { "eval": stockfish.eval(), "best_move": stockfish.get_best_move(), "index": index }
