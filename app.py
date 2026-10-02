"""Fade House - cadastro de clientes e barbeiros (nome, e-mail e telefone)."""
import re
import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "fadehouse.db"

app = Flask(__name__, static_folder="static", static_url_path="")

TABELAS = {"clientes": "cliente", "barbeiros": "barbeiro"}
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def init_db():
    with sqlite3.connect(DB_PATH) as db:
        for tabela in TABELAS.values():
            db.execute(
                f"""CREATE TABLE IF NOT EXISTS {tabela} (
                    id       INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome     TEXT NOT NULL,
                    email    TEXT NOT NULL UNIQUE,
                    telefone TEXT NOT NULL
                )"""
            )


def validar(dados):
    nome = " ".join(str(dados.get("nome", "")).split())
    email = str(dados.get("email", "")).strip().lower()
    telefone = re.sub(r"\D", "", str(dados.get("telefone", "")))

    erros = {}
    if len(nome) < 3:
        erros["nome"] = "Informe o nome completo."
    if not EMAIL_RE.match(email):
        erros["email"] = "Informe um e-mail válido, como nome@exemplo.com."
    if len(telefone) not in (10, 11):
        erros["telefone"] = "Informe o telefone com DDD, como (41) 99999-9999."
    return {"nome": nome, "email": email, "telefone": telefone}, erros


@app.post("/api/<tipo>")
def cadastrar(tipo):
    tabela = TABELAS.get(tipo)
    if not tabela:
        return jsonify(erro="Tipo de cadastro inexistente."), 404

    dados, erros = validar(request.get_json(silent=True) or {})
    if erros:
        return jsonify(erros=erros), 400

    try:
        with sqlite3.connect(DB_PATH) as db:
            db.execute(
                f"INSERT INTO {tabela} (nome, email, telefone) VALUES (?, ?, ?)",
                (dados["nome"], dados["email"], dados["telefone"]),
            )
    except sqlite3.IntegrityError:
        return jsonify(erros={"email": "Este e-mail já está cadastrado."}), 409

    return jsonify(ok=True), 201


@app.get("/")
def index():
    return app.send_static_file("index.html")


init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5000)