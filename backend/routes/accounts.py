import importlib
import re
import sqlite3
from datetime import date, datetime, time, timedelta

from flask import Blueprint, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash

core = importlib.import_module("backend.app")

bp = Blueprint("accounts", __name__)

@bp.post("/api/<tipo>")
def cadastrar(tipo):
    tabela = core.TABELAS.get(tipo)
    if not tabela:
        return jsonify(erro="Tipo de cadastro inexistente."), 404
    if tipo != "clientes":
        return jsonify(erro="O cadastro de barbeiros é feito pela administração."), 403

    entrada = request.get_json(silent=True) or {}
    dados, erros = core.validar(entrada, tipo=tipo)
    if dados["telefone"] == core.ADMIN_TELEFONE:
        erros["telefone"] = "Este telefone é reservado para a conta administradora."
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
        with sqlite3.connect(core.DB_PATH) as db:
            db.execute("BEGIN IMMEDIATE")
            for tabela_existente in core.TABELAS.values():
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
            if db.execute(
                "SELECT 1 FROM solicitacao_barbeiro WHERE lower(email) = ? LIMIT 1",
                (dados["email"],),
            ).fetchone():
                erros["email"] = "Este e-mail já possui uma solicitação pendente."
            if db.execute(
                "SELECT 1 FROM solicitacao_barbeiro WHERE telefone = ? LIMIT 1",
                (dados["telefone"],),
            ).fetchone():
                erros["telefone"] = "Este telefone já possui uma solicitação pendente."

            if erros:
                return jsonify(erros=erros), 409

            senha_hash = generate_password_hash(senha)
            cursor = db.execute(
                f"INSERT INTO {tabela} (nome, email, telefone, senha_hash) VALUES (?, ?, ?, ?)",
                (dados["nome"], dados["email"], dados["telefone"], senha_hash),
            )
    except sqlite3.IntegrityError:
        return jsonify(erros={"email": "Este e-mail já está cadastrado."}), 409

    session.clear()
    session["tipo"] = tipo
    session["usuario_id"] = cursor.lastrowid
    session["nome"] = dados["nome"]
    return jsonify(ok=True), 201

@bp.post("/api/login")
def login():
    dados = request.get_json(silent=True) or {}
    identificador = str(dados.get("identificador", "")).strip()
    senha = str(dados.get("senha", ""))

    usuarios = []
    if senha:
        with sqlite3.connect(core.DB_PATH) as db:
            if core.EMAIL_RE.fullmatch(identificador.lower()):
                for tipo_conta, tabela in core.TABELAS.items():
                    contas = db.execute(
                        f"SELECT id, nome, senha_hash, telefone, email FROM {tabela} "
                        "WHERE lower(email) = ?",
                        (identificador.lower(),),
                    ).fetchall()
                    usuarios.extend((tipo_conta, conta) for conta in contas)
            else:
                telefone = re.sub(r"\D", "", identificador)
                formato_telefone = re.fullmatch(r"[+\d()\s.-]+", identificador)
                if formato_telefone and len(telefone) in (10, 11):
                    for tipo_conta, tabela in core.TABELAS.items():
                        contas = db.execute(
                            f"SELECT id, nome, senha_hash, telefone, email FROM {tabela} "
                            "WHERE telefone = ?",
                            (telefone,),
                        ).fetchall()
                        usuarios.extend((tipo_conta, conta) for conta in contas)

    if len(usuarios) != 1:
        return jsonify(erro="E-mail/telefone ou senha incorretos."), 401

    tipo, usuario = usuarios[0]
    if usuario[2] and not check_password_hash(usuario[2], senha):
        return jsonify(erro="E-mail/telefone ou senha incorretos."), 401

    if not usuario[2]:
        telefone = re.sub(r"\D", "", identificador)
        if telefone == usuario[3]:
            if len(senha) < 6 or len(senha) > 128:
                return jsonify(erro="Defina uma senha com 6 a 128 caracteres."), 400
            with sqlite3.connect(core.DB_PATH) as db:
                db.execute(
                    f"UPDATE {core.TABELAS[tipo]} SET senha_hash = ? WHERE id = ?",
                    (generate_password_hash(senha), usuario[0]),
                )
        elif core.EMAIL_RE.fullmatch(identificador.lower()):
            return jsonify(erro="No primeiro acesso, use o telefone cadastrado para definir sua senha."), 401
        else:
            return jsonify(erro="E-mail/telefone ou senha incorretos."), 401

    session.clear()
    session["tipo"] = tipo
    session["usuario_id"] = usuario[0]
    session["nome"] = usuario[1]
    session["administrador"] = tipo == "barbeiros" and usuario[4] == core.ADMIN_EMAIL
    return jsonify(ok=True)

@bp.post("/api/contas/<tipo>")
def criar_conta_administrador(tipo):
    if not core.exigir_administrador():
        return jsonify(erro="Apenas a conta administradora pode cadastrar contas."), 403

    tabela = core.TABELAS.get(tipo)
    if not tabela:
        return jsonify(erro="Tipo de conta inválido."), 404

    entrada = request.get_json(silent=True) or {}
    dados, erros = core.validar(entrada, tipo=tipo)
    senha = str(entrada.get("senha", ""))
    if len(senha) < 6:
        erros["senha"] = "A senha deve ter pelo menos 6 caracteres."
    elif len(senha) > 128:
        erros["senha"] = "A senha deve ter no máximo 128 caracteres."
    if dados["telefone"] == core.ADMIN_TELEFONE:
        erros["telefone"] = "Este telefone é reservado para a conta administradora."
    if dados["email"] == core.ADMIN_EMAIL:
        erros["email"] = "Este e-mail é reservado para a conta administradora."
    if erros:
        return jsonify(erros=erros), 400

    try:
        with sqlite3.connect(core.DB_PATH) as db:
            db.execute("BEGIN IMMEDIATE")
            for tabela_existente in core.TABELAS.values():
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

    return jsonify(ok=True, id=cursor.lastrowid), 201

@bp.get("/api/sessao")
def sessao_atual():
    if not session.get("tipo"):
        return jsonify(autenticado=False)
    if not core.conta_ativa():
        session.clear()
        return jsonify(autenticado=False)
    dados_sessao = {
        "autenticado": True,
        "tipo": session["tipo"],
        "nome": session["nome"],
    }
    if session["tipo"] == "barbeiros":
        dados_sessao["administrador"] = session.get("administrador", False)
    return jsonify(dados_sessao)

@bp.get("/api/solicitacoes-barbeiros")
def listar_solicitacoes_barbeiros():
    if not core.exigir_administrador():
        return jsonify(erro="Apenas a conta administradora pode consultar solicitações."), 403

    with sqlite3.connect(core.DB_PATH) as db:
        db.row_factory = sqlite3.Row
        solicitacoes = [dict(row) for row in db.execute(
            "SELECT id, nome, email, telefone FROM solicitacao_barbeiro ORDER BY id"
        )]
    return jsonify(solicitacoes=solicitacoes)

@bp.post("/api/solicitacoes-barbeiros/<int:solicitacao_id>/aprovar")
def aprovar_solicitacao_barbeiro(solicitacao_id):
    if not core.exigir_administrador():
        return jsonify(erro="Apenas a conta administradora pode aprovar solicitações."), 403

    try:
        with sqlite3.connect(core.DB_PATH) as db:
            db.execute("BEGIN IMMEDIATE")
            solicitacao = db.execute(
                "SELECT nome, email, telefone, senha_hash FROM solicitacao_barbeiro WHERE id = ?",
                (solicitacao_id,),
            ).fetchone()
            if not solicitacao:
                return jsonify(erro="Solicitação não encontrada."), 404

            db.execute(
                "INSERT INTO barbeiro (nome, email, telefone, senha_hash) VALUES (?, ?, ?, ?)",
                solicitacao,
            )
            db.execute("DELETE FROM solicitacao_barbeiro WHERE id = ?", (solicitacao_id,))
    except sqlite3.IntegrityError:
        return jsonify(erro="O e-mail ou telefone já está cadastrado."), 409

    return jsonify(ok=True), 200

@bp.delete("/api/solicitacoes-barbeiros/<int:solicitacao_id>")
def recusar_solicitacao_barbeiro(solicitacao_id):
    if not core.exigir_administrador():
        return jsonify(erro="Apenas a conta administradora pode recusar solicitações."), 403

    with sqlite3.connect(core.DB_PATH) as db:
        cursor = db.execute(
            "DELETE FROM solicitacao_barbeiro WHERE id = ?",
            (solicitacao_id,),
        )
    if cursor.rowcount == 0:
        return jsonify(erro="Solicitação não encontrada."), 404
    return "", 204

@bp.get("/api/contas")
def listar_contas():
    if not core.exigir_administrador():
        return jsonify(erro="Apenas a conta administradora pode consultar contas."), 403

    with sqlite3.connect(core.DB_PATH) as db:
        db.row_factory = sqlite3.Row
        clientes = [dict(row) for row in db.execute(
            "SELECT id, nome, email, telefone FROM cliente ORDER BY nome, id"
        )]
        barbeiros = [dict(row) for row in db.execute(
            "SELECT id, nome, email, telefone FROM barbeiro ORDER BY nome, id"
        )]
    for barbeiro in barbeiros:
        barbeiro["administrador"] = barbeiro["email"] == core.ADMIN_EMAIL
    return jsonify(clientes=clientes, barbeiros=barbeiros)

@bp.delete("/api/contas/<tipo>/<int:conta_id>")
def excluir_conta(tipo, conta_id):
    if not core.exigir_administrador():
        return jsonify(erro="Apenas a conta administradora pode excluir contas."), 403

    tabela = core.TABELAS.get(tipo)
    if not tabela:
        return jsonify(erro="Tipo de conta inválido."), 404

    with sqlite3.connect(core.DB_PATH) as db:
        db.execute("BEGIN IMMEDIATE")
        conta = db.execute(
            f"SELECT email FROM {tabela} WHERE id = ?",
            (conta_id,),
        ).fetchone()
        if not conta:
            return jsonify(erro="Conta não encontrada."), 404
        if tipo == "barbeiros" and conta[0] == core.ADMIN_EMAIL:
            return jsonify(erro="A conta administradora não pode ser excluída."), 403
        db.execute(f"DELETE FROM {tabela} WHERE id = ?", (conta_id,))

    return jsonify(ok=True), 200

@bp.post("/api/sair")
def sair():
    session.clear()
    return jsonify(ok=True)
