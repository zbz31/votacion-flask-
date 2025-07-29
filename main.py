from flask import Flask, request, jsonify
import json, os
from datetime import datetime

app = Flask(__name__)

# 🔧 Crear la carpeta /data si no existe
os.makedirs("/data", exist_ok=True)

DB_FILE = "/data/votes.json"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({"total": 0, "count": 0, "visits": 0}, f)

def read_votes():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def write_votes(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

@app.route("/vote", methods=["POST"])
def vote():
    data = request.get_json()
    stars = data.get("stars")
    if not isinstance(stars, int) or not (1 <= stars <= 5):
        return jsonify({"error": "Voto inválido"}), 400
    votes = read_votes()
    votes["total"] += stars
    votes["count"] += 1
    write_votes(votes)
    return jsonify({"message": "Voto registrado"}), 200

@app.route("/average")
def average():
    votes = read_votes()
    if votes["count"] == 0:
        return jsonify({"average": 0, "totalVotes": 0})
    avg = votes["total"] / votes["count"]
    return jsonify({"average": round(avg, 2), "totalVotes": votes["count"]})

@app.route("/ping")
def ping():
    return "pong", 200

@app.route("/wake")
def wake():
    return jsonify({"message": "Servidor activo", "time": datetime.now().isoformat()})

@app.route("/")
def home():
    votes = read_votes()
    votes["visits"] = votes.get("visits", 0) + 1
    write_votes(votes)
    return f"Servidor activo - visitas: {votes['visits']}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
