from flask import Flask, request, render_template, jsonify
import json
import os

app = Flask(__name__)

PLAYERS_FILE = "players.json"

# Cria o arquivo se não existir
if not os.path.exists(PLAYERS_FILE):
    with open(PLAYERS_FILE, "w") as f:
        json.dump({}, f)

# Recebe dados do plugin Listening
@app.route("/api/players", methods=["POST"])
def add_player():
    data = request.json
    with open(PLAYERS_FILE, "r") as f:
        players = json.load(f)

    # Remove jogador se action for remove
    if data.get("action") == "remove":
        players.pop(data["name"], None)
    else:
        players[data["name"]] = {
            "ping": data.get("ping"),
            "ip": data.get("ip")
        }

    with open(PLAYERS_FILE, "w") as f:
        json.dump(players, f, indent=4)

    return jsonify({"status": "success"})

# Página web para mostrar os jogadores online
@app.route("/")
def index():
    with open(PLAYERS_FILE, "r") as f:
        players = json.load(f)
    return render_template("index.html", players=players)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
