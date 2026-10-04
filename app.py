"""Fade House - cadastro de clientes e barbeiros (nome, e-mail e telefone)."""
import re
import sqlite3
import math
import os
import secrets
from pathlib import Path

from flask import Flask, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "fadehouse.db"

app = Flask(__name__, static_folder="static", static_url_path="")
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)

TABELAS = {"clientes": "cliente", "barbeiros": "barbeiro"}
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
NOME_Barbeiro_RE = re.compile(r"^[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ ]*$")


def init_db():
    with sqlite3.connect(DB_PATH) as db:
        for tabela in TABELAS.values():
            db.execute(
                f"""CREATE TABLE IF NOT EXISTS {tabela} (
                    id       INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome     TEXT NOT NULL,
                    email    TEXT NOT NULL UNIQUE,
                    telefone TEXT NOT NULL,
                    senha_hash TEXT
                )"""
            )
            colunas = {linha[1] for linha in db.execute(f"PRAGMA table_info({tabela})")}
            if "senha_hash" not in colunas:
                db.execute(f"ALTER TABLE {tabela} ADD COLUMN senha_hash TEXT")
        db.execute(
            """CREATE TABLE IF NOT EXISTS servico (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                nome     TEXT NOT NULL UNIQUE,
                duracao  INTEGER NOT NULL,
                preco    REAL NOT NULL
            )"""
        )
        if db.execute("SELECT COUNT(*) FROM servico").fetchone()[0] == 0:
            db.executemany(
                "INSERT INTO servico (nome, duracao, preco) VALUES (?, ?, ?)",
                [
                    ("Corte", 30, 35),
                    ("Barba", 20, 25),
                    ("Corte + Barba", 50, 55),
                    ("Sobrancelha", 10, 15),
                    ("Pigmentação", 40, 45),
                ],
            )


def validar_servico(dados):
    nome = " ".join(str(dados.get("nome", "")).split())
    erros = {}

    if len(nome) < 2:
        erros["nome"] = "Informe o nome do serviço."
    elif len(nome) > 80:
        erros["nome"] = "Use no máximo 80 caracteres."

    try:
        duracao = int(dados.get("duracao", ""))
        if duracao < 5 or duracao > 480:
            raise ValueError
    except (TypeError, ValueError):
        duracao = 0
        erros["duracao"] = "Informe uma duração entre 5 e 480 minutos."

    try:
        preco = float(str(dados.get("preco", "")).replace(",", "."))
        if not math.isfinite(preco) or preco < 0 or preco > 99999.99:
            raise ValueError
    except (TypeError, ValueError):
        preco = 0
        erros["preco"] = "Informe um preço válido."

    return {"nome": nome, "duracao": duracao, "preco": preco}, erros


def validar(dados, tipo=None):
    nome = " ".join(str(dados.get("nome", "")).split())
    email = str(dados.get("email", "")).strip().lower()
    telefone = re.sub(r"\D", "", str(dados.get("telefone", "")))

    erros = {}
    if tipo == "barbeiros":
        if not nome or not NOME_Barbeiro_RE.fullmatch(nome):
            erros["nome"] = "Use letras maiúsculas no início de cada nome e evite números ou símbolos."
    elif len(nome) < 3:
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

    entrada = request.get_json(silent=True) or {}
    dados, erros = validar(entrada, tipo=tipo)
    senha = str(entrada.get("senha", ""))
    confirmar_senha = str(entrada.get("confirmar_senha", ""))
    if len(senha) < 6:
        erros["senha"] = "A senha deve ter pelo menos 6 caracteres."
    elif len(senha) > 128:
        erros["senha"] = "A senha deve ter no máximo 128 caracteres."
    if senha != confirmar_senha:
        erros["confirmar_senha"] = "As senhas não coincidem."
    if erros:
        return jsonify(erros=erros), 400

    try:
        with sqlite3.connect(DB_PATH) as db:
            db.execute("BEGIN IMMEDIATE")
            for tabela_existente in TABELAS.values():
                if db.execute(
                    f"SELECT 1 FROM {tabela_existente} WHERE lower(email) = ? LIMIT 1",
                    (dados["email"],),
                ).fetchone():
                    erros["email"] = "Este e-mail já está cadastrado."
                if db.execute(
                    f"SELECT 1 FROM {tabela_existente} WHERE telefone = ? LIMIT 1",
                    (dados["telefone"],),
                ).fetchone():
                    erros["telefone"] = "Este telefone já está cadastrado."

            if erros:
                return jsonify(erros=erros), 409

            cursor = db.execute(
                f"INSERT INTO {tabela} (nome, email, telefone, senha_hash) VALUES (?, ?, ?, ?)",
                (
                    dados["nome"],
                    dados["email"],
                    dados["telefone"],
                    generate_password_hash(senha),
                ),
            )
    except sqlite3.IntegrityError:
        return jsonify(erros={"email": "Este e-mail já está cadastrado."}), 409

    session.clear()
    session["tipo"] = tipo
    session["usuario_id"] = cursor.lastrowid
    session["nome"] = dados["nome"]
    return jsonify(ok=True), 201


@app.post("/api/login")
def login():
    dados = request.get_json(silent=True) or {}
    tipo = dados.get("tipo")
    tabela = TABELAS.get(tipo)
    identificador = str(dados.get("identificador", "")).strip()
    senha = str(dados.get("senha", ""))

    usuarios = []
    if tabela and senha:
        with sqlite3.connect(DB_PATH) as db:
            if EMAIL_RE.fullmatch(identificador.lower()):
                usuarios = db.execute(
                    f"SELECT id, nome, senha_hash, telefone FROM {tabela} WHERE email = ?",
                    (identificador.lower(),),
                ).fetchall()
            else:
                telefone = re.sub(r"\D", "", identificador)
                formato_telefone = re.fullmatch(r"[+\d()\s.-]+", identificador)
                if formato_telefone and len(telefone) in (10, 11):
                    usuarios = db.execute(
                        f"SELECT id, nome, senha_hash, telefone FROM {tabela} WHERE telefone = ?",
                        (telefone,),
                    ).fetchall()

    usuario = next(
        (conta for conta in usuarios if conta[2] and check_password_hash(conta[2], senha)),
        None,
    )

    if not usuario:
        telefone = re.sub(r"\D", "", identificador)
        contas_sem_senha = [conta for conta in usuarios if not conta[2]]
        if len(contas_sem_senha) == 1 and telefone == contas_sem_senha[0][3]:
            conta = contas_sem_senha[0]
            if len(senha) < 6 or len(senha) > 128:
                return jsonify(erro="Defina uma senha com 6 a 128 caracteres."), 400
            with sqlite3.connect(DB_PATH) as db:
                db.execute(
                    f"UPDATE {tabela} SET senha_hash = ? WHERE id = ?",
                    (generate_password_hash(senha), conta[0]),
                )
            usuario = conta
        elif contas_sem_senha and EMAIL_RE.fullmatch(identificador.lower()):
            return jsonify(erro="No primeiro acesso, use o telefone cadastrado para definir sua senha."), 401
        else:
            return jsonify(erro="E-mail/telefone ou senha incorretos."), 401

    session.clear()
    session["tipo"] = tipo
    session["usuario_id"] = usuario[0]
    session["nome"] = usuario[1]
    return jsonify(ok=True)


@app.get("/api/sessao")
def sessao_atual():
    if not session.get("tipo"):
        return jsonify(autenticado=False)
    return jsonify(
        autenticado=True,
        tipo=session["tipo"],
        nome=session["nome"],
    )


@app.post("/api/sair")
def sair():
    session.clear()
    return jsonify(ok=True)


@app.get("/api/barbeiros")
def listar_barbeiros():
    with sqlite3.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        barbeiros = [dict(row) for row in db.execute(
            "SELECT id, nome FROM barbeiro ORDER BY nome"
        )]
    return jsonify(barbeiros=[{"id": "fixo-joao", "nome": "João"}, *barbeiros])


@app.get("/api/servicos")
def listar_servicos():
    with sqlite3.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        servicos = [dict(row) for row in db.execute(
            "SELECT id, nome, duracao, preco FROM servico ORDER BY id"
        )]
    return jsonify(servicos=servicos)


@app.post("/api/servicos")
def criar_servico():
    if session.get("tipo") != "barbeiros":
        return jsonify(erro="Apenas barbeiros podem gerenciar serviços."), 403

    dados, erros = validar_servico(request.get_json(silent=True) or {})
    if erros:
        return jsonify(erros=erros), 400

    try:
        with sqlite3.connect(DB_PATH) as db:
            cursor = db.execute(
                "INSERT INTO servico (nome, duracao, preco) VALUES (?, ?, ?)",
                (dados["nome"], dados["duracao"], dados["preco"]),
            )
            dados["id"] = cursor.lastrowid
    except sqlite3.IntegrityError:
        return jsonify(erros={"nome": "Já existe um serviço com esse nome."}), 409

    return jsonify(servico=dados), 201


@app.delete("/api/servicos/<int:servico_id>")
def remover_servico(servico_id):
    if session.get("tipo") != "barbeiros":
        return jsonify(erro="Apenas barbeiros podem gerenciar serviços."), 403

    with sqlite3.connect(DB_PATH) as db:
        cursor = db.execute("DELETE FROM servico WHERE id = ?", (servico_id,))
    if cursor.rowcount == 0:
        return jsonify(erro="Serviço não encontrado."), 404
    return "", 204


@app.get("/")
def index():
    return app.send_static_file("index.html")


init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5000)