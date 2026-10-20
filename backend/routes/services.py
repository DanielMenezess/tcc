import importlib
import re
import sqlite3
from datetime import date, datetime, time, timedelta

from flask import Blueprint, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash

core = importlib.import_module("backend.app")

bp = Blueprint("services", __name__)

@bp.get("/api/barbeiros")
def listar_barbeiros():
    with sqlite3.connect(core.DB_PATH) as db:
        db.row_factory = sqlite3.Row
        barbeiros = [dict(row) for row in db.execute(
            "SELECT id, nome FROM barbeiro ORDER BY nome"
        )]
    return jsonify(barbeiros=barbeiros)

@bp.get("/api/servicos")
def listar_servicos():
    with sqlite3.connect(core.DB_PATH) as db:
        db.row_factory = sqlite3.Row
        servicos = [dict(row) for row in db.execute(
            "SELECT id, nome, duracao, preco FROM servico ORDER BY id"
        )]
    return jsonify(servicos=servicos)

@bp.post("/api/servicos")
def criar_servico():
    if session.get("tipo") != "barbeiros" or not core.conta_ativa():
        return jsonify(erro="Apenas barbeiros podem gerenciar serviços."), 403

    dados, erros = core.validar_servico(request.get_json(silent=True) or {})
    if erros:
        return jsonify(erros=erros), 400

    try:
        with sqlite3.connect(core.DB_PATH) as db:
            cursor = db.execute(
                "INSERT INTO servico (nome, duracao, preco) VALUES (?, ?, ?)",
                (dados["nome"], dados["duracao"], dados["preco"]),
            )
            dados["id"] = cursor.lastrowid
    except sqlite3.IntegrityError:
        return jsonify(erros={"nome": "Já existe um serviço com esse nome."}), 409

    return jsonify(servico=dados), 201

@bp.delete("/api/servicos/<int:servico_id>")
def remover_servico(servico_id):
    if session.get("tipo") != "barbeiros" or not core.conta_ativa():
        return jsonify(erro="Apenas barbeiros podem gerenciar serviços."), 403

    with sqlite3.connect(core.DB_PATH) as db:
        cursor = db.execute("DELETE FROM servico WHERE id = ?", (servico_id,))
    if cursor.rowcount == 0:
        return jsonify(erro="Serviço não encontrado."), 404
    return "", 204
