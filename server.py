from flask import Flask, request, jsonify
from flask_cors import CORS
import chess
import chess.engine
import random
import time


app = Flask(__name__)
CORS(app)

engine = chess.engine.SimpleEngine.popen_uci(["python", "./chess-engine.py"])


@app.route("/move", methods=["POST"])
def ai_move():
    data = request.get_json()
    fen = data.get("fen")
    # check is valid FEN
    try:
        game = chess.Board(fen)
    except:
        return jsonify({"error": "Invalid FEN"}), 400

    if game.is_game_over():
        return jsonify({"error": "Game is over"}), 400
    # return random move
    # legal_moves = list(game.legal_moves)
    # if not legal_moves:
    #     return jsonify({"next_move": ""})
    # random_move = random.choice(legal_moves)
    # return jsonify({"next_move": random_move.uci()})

    print(game.fen())
    # print execution time
    start_time = time.time()
    result = engine.play(game, chess.engine.Limit(time=200.0))
    end_time = time.time()
    print("Time:", end_time - start_time)
    print(result)
    return jsonify({"next_move": result.move.uci()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8099)
