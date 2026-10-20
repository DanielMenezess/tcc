"""Fade House - cadastro de clientes e barbeiros (nome, e-mail e telefone)."""
import re
import sqlite3
import math
import os
import secrets
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from flask import Flask, jsonify, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "fadehouse.db"

FRONTEND_DIR = BASE_DIR / "frontend"
app = Flask(
    __name__,
    template_folder=str(FRONTEND_DIR / "templates"),
    static_folder=str(FRONTEND_DIR / "static"),
    static_url_path="",
)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)

TABELAS = {"clientes": "cliente", "barbeiros": "barbeiro"}
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
NOME_Barbeiro_RE = re.compile(r"^[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ ]*$")
ADMIN_NOME = "Daniel Gabriel"
ADMIN_EMAIL = "danielgabriel@gmail.com"
ADMIN_TELEFONE = "11111111111"
ADMIN_SENHA = "123456"
ADMIN_SENHA_HASH = generate_password_hash(ADMIN_SENHA)
FUSO_HORARIO = ZoneInfo("America/Sao_Paulo")


def agora_local():
    return datetime.now(FUSO_HORARIO)


def horario_local(data_texto, horario_texto):
    data_agendamento = date.fromisoformat(data_texto)
    hora_agendamento = time.fromisoformat(horario_texto)
    return datetime.combine(data_agendamento, hora_agendamento, tzinfo=FUSO_HORARIO)


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
        db.execute(
            """CREATE TABLE IF NOT EXISTS agendamento (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id       INTEGER NOT NULL,
                servico_id       INTEGER NOT NULL,
                servico_nome     TEXT NOT NULL,
                barbeiro_id      TEXT NOT NULL,
                barbeiro_nome    TEXT NOT NULL,
                data_agendamento TEXT NOT NULL,
                horario          TEXT NOT NULL,
                duracao          INTEGER NOT NULL,
                preco            REAL NOT NULL,
                status           TEXT NOT NULL DEFAULT 'confirmado'
            )"""
        )
        colunas_agendamento = {
            linha[1] for linha in db.execute("PRAGMA table_info(agendamento)")
        }
        if "status" not in colunas_agendamento:
            db.execute(
                "ALTER TABLE agendamento ADD COLUMN status TEXT NOT NULL DEFAULT 'confirmado'"
            )
        db.execute(
            "CREATE TABLE IF NOT EXISTS app_migracao (nome TEXT PRIMARY KEY)"
        )
        migracao_historico = "historico_agendamentos_concluidos_v1"
        if not db.execute(
            "SELECT 1 FROM app_migracao WHERE nome = ?", (migracao_historico,)
        ).fetchone():
            agora = agora_local()
            data_limite = (agora.date() - timedelta(days=1)).isoformat()
            agendamentos_antigos = db.execute(
                "SELECT id, data_agendamento, horario, duracao FROM agendamento "
                "WHERE status = 'confirmado' AND data_agendamento >= ?",
                (data_limite,),
            ).fetchall()
            for agendamento_id, data_agendamento, horario, duracao in agendamentos_antigos:
                try:
                    fim = horario_local(data_agendamento, horario) + timedelta(minutes=duracao)
                except (TypeError, ValueError):
                    continue
                if fim <= agora:
                    db.execute(
                        "UPDATE agendamento SET status = 'concluido' WHERE id = ?",
                        (agendamento_id,),
                    )
            db.execute("INSERT INTO app_migracao (nome) VALUES (?)", (migracao_historico,))
        db.execute(
            """CREATE TABLE IF NOT EXISTS solicitacao_barbeiro (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                nome       TEXT NOT NULL,
                email      TEXT NOT NULL UNIQUE,
                telefone   TEXT NOT NULL UNIQUE,
                senha_hash TEXT NOT NULL
            )"""
        )
        db.execute(
            "INSERT INTO barbeiro (nome, email, telefone, senha_hash) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(email) DO UPDATE SET nome = excluded.nome, "
            "telefone = excluded.telefone, senha_hash = excluded.senha_hash",
            (ADMIN_NOME, ADMIN_EMAIL, ADMIN_TELEFONE, ADMIN_SENHA_HASH),
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
    if any(caractere.isnumeric() for caractere in nome):
        erros["nome"] = "O nome da conta não pode conter números."
    elif tipo == "barbeiros":
        if not nome or not NOME_Barbeiro_RE.fullmatch(nome):
            erros["nome"] = "Use letras maiúsculas no início de cada nome e evite números ou símbolos."
    elif len(nome) < 3:
        erros["nome"] = "Informe o nome completo."

    if not EMAIL_RE.match(email):
        erros["email"] = "Informe um e-mail válido, como nome@exemplo.com."
    if len(telefone) not in (10, 11):
        erros["telefone"] = "Informe o telefone com DDD, como (41) 99999-9999."
    return {"nome": nome, "email": email, "telefone": telefone}, erros










def conta_ativa():
    tipo = session.get("tipo")
    tabela = TABELAS.get(tipo)
    if not tabela or not session.get("usuario_id"):
        return False

    with sqlite3.connect(DB_PATH) as db:
        conta = db.execute(
            f"SELECT email FROM {tabela} WHERE id = ?",
            (session["usuario_id"],),
        ).fetchone()
    return conta is not None


def exigir_administrador():
    if (
        session.get("tipo") != "barbeiros"
        or session.get("administrador") is not True
        or not conta_ativa()
    ):
        return False

    with sqlite3.connect(DB_PATH) as db:
        conta = db.execute(
            "SELECT email FROM barbeiro WHERE id = ?",
            (session["usuario_id"],),
        ).fetchone()
    return conta is not None and conta[0] == ADMIN_EMAIL












































@app.get("/")
def index():
    return render_template("index.html")


from .routes import account_bp, appointment_bp, service_bp

app.register_blueprint(account_bp)
app.register_blueprint(appointment_bp)
app.register_blueprint(service_bp)


init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
