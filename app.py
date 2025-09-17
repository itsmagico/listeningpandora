from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Lista de players recebidos pelo plugin
players = []

# Rota principal do site
@app.route("/")
def home():
    return render_template("index.html", players=players)

# Rota para o plugin enviar dados
@app.route("/api/player", methods=["POST"])
def add_player():
    data = request.json
    if not data or "nome" not in data or "ping" not in data or "ip" not in data:
        return jsonify({"error": "Dados inválidos"}), 400
    
    # Evita duplicatas pelo IP
    for player in players:
        if player["ip"] == data["ip"]:
            player.update({"nome": data["nome"], "ping": data["ping"]})
            break
    else:
        players.append({"nome": data["nome"], "ping": data["ping"], "ip": data["ip"]})
    
    return jsonify({"success": True}), 200

# Rota para retornar os players em JSON (opcional para debug)
@app.route("/api/players", methods=["GET"])
def get_players():
    return jsonify(players)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
