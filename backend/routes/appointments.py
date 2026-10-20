import importlib
import re
import sqlite3
from datetime import date, datetime, time, timedelta

from flask import Blueprint, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash

core = importlib.import_module("backend.app")

bp = Blueprint("appointments", __name__)

@bp.get("/api/horarios-disponiveis")
def listar_horarios_disponiveis():
    if session.get("tipo") != "clientes" or not core.conta_ativa():
        return jsonify(erro="Apenas clientes podem consultar horários disponíveis."), 403

    dados = request.args
    try:
        barbeiro_id = int(dados.get("barbeiro_id", ""))
        servico_id = int(dados.get("servico_id", ""))
        data_agendamento = date.fromisoformat(dados.get("data", ""))
    except (TypeError, ValueError):
        return jsonify(erro="Escolha serviço, barbeiro e data válidos."), 400
    data_texto = dados.get("data", "")
    if data_agendamento.isoformat() != data_texto or data_agendamento < core.agora_local().date():
        return jsonify(erro="A data do agendamento não pode ser anterior a hoje."), 400

    with sqlite3.connect(core.DB_PATH) as db:
        barbeiro = db.execute("SELECT 1 FROM barbeiro WHERE id = ?", (barbeiro_id,)).fetchone()
        servico = db.execute("SELECT duracao FROM servico WHERE id = ?", (servico_id,)).fetchone()
        if not barbeiro:
            return jsonify(erro="O barbeiro selecionado não existe mais."), 404
        if not servico:
            return jsonify(erro="O serviço selecionado não existe mais."), 404
        ocupados = db.execute(
            "SELECT horario, duracao FROM agendamento "
            "WHERE barbeiro_id = ? AND data_agendamento = ? "
            "AND status IN ('pendente', 'confirmado') "
            "ORDER BY horario, id",
            (str(barbeiro_id), data_texto),
        ).fetchall()

    intervalos_ocupados = []
    for horario, duracao in ocupados:
        inicio = core.horario_local(data_texto, horario)
        fim = inicio + timedelta(minutes=duracao)
        intervalos_ocupados.append({
            "inicio": inicio.strftime("%H:%M"),
            "fim": fim.strftime("%H:%M"),
        })

    return jsonify(
        duracao=servico[0],
        horario_fechamento="20:00",
        ocupados=intervalos_ocupados,
    )

@bp.get("/api/agendamentos-pendentes")
def listar_agendamentos_pendentes():
    if session.get("tipo") != "barbeiros" or not core.conta_ativa():
        return jsonify(erro="Apenas barbeiros podem consultar agendamentos pendentes."), 403

    administrador = core.exigir_administrador()
    filtro_barbeiro = "" if administrador else "AND a.barbeiro_id = ? "
    parametros = () if administrador else (str(session["usuario_id"]),)
    with sqlite3.connect(core.DB_PATH) as db:
        db.row_factory = sqlite3.Row
        agendamentos = [dict(row) for row in db.execute(
            "SELECT a.id, a.data_agendamento AS data, a.horario, "
            "a.servico_nome AS servico, a.duracao, a.preco, c.nome AS cliente, "
            "a.barbeiro_nome AS barbeiro "
            "FROM agendamento AS a LEFT JOIN cliente AS c ON c.id = a.cliente_id "
            f"WHERE a.status = 'pendente' {filtro_barbeiro}"
            "ORDER BY a.data_agendamento, a.horario, a.id",
            parametros,
        )]
    return jsonify(agendamentos=agendamentos, administrador=administrador)

@bp.post("/api/agendamentos/<int:agendamento_id>/decisao")
def decidir_agendamento(agendamento_id):
    if session.get("tipo") != "barbeiros" or not core.conta_ativa():
        return jsonify(erro="Apenas barbeiros podem decidir agendamentos."), 403

    status = (request.get_json(silent=True) or {}).get("status")
    if status not in ("confirmado", "cancelado"):
        return jsonify(erro="Escolha aceitar ou recusar o agendamento."), 400

    administrador = core.exigir_administrador()
    filtro_barbeiro = "" if administrador else " AND barbeiro_id = ?"
    parametros = (agendamento_id,) if administrador else (
        agendamento_id,
        str(session["usuario_id"]),
    )
    with sqlite3.connect(core.DB_PATH) as db:
        db.execute("BEGIN IMMEDIATE")
        agendamento = db.execute(
            f"SELECT status FROM agendamento WHERE id = ?{filtro_barbeiro}",
            parametros,
        ).fetchone()
        if not agendamento:
            return jsonify(erro="Agendamento não encontrado."), 404
        if agendamento[0] != "pendente":
            return jsonify(erro="Este agendamento já foi decidido."), 409
        db.execute(
            "UPDATE agendamento SET status = ? WHERE id = ?",
            (status, agendamento_id),
        )

    return jsonify(ok=True, status=status)

@bp.get("/api/agendamentos-a-concluir")
def listar_agendamentos_a_concluir():
    if session.get("tipo") != "barbeiros" or not core.conta_ativa():
        return jsonify(erro="Apenas barbeiros podem consultar serviços aguardando conclusão."), 403

    administrador = core.exigir_administrador()
    filtro_barbeiro = "" if administrador else "AND a.barbeiro_id = ? "
    parametros = () if administrador else (str(session["usuario_id"]),)
    with sqlite3.connect(core.DB_PATH) as db:
        db.row_factory = sqlite3.Row
        agendamentos = [dict(row) for row in db.execute(
            "SELECT a.id, a.data_agendamento AS data, a.horario, "
            "a.servico_nome AS servico, a.duracao, a.preco, c.nome AS cliente, "
            "a.barbeiro_nome AS barbeiro "
            "FROM agendamento AS a LEFT JOIN cliente AS c ON c.id = a.cliente_id "
            f"WHERE a.status = 'confirmado' {filtro_barbeiro}"
            "ORDER BY a.data_agendamento, a.horario, a.id",
            parametros,
        )]
    return jsonify(agendamentos=agendamentos, administrador=administrador)

@bp.post("/api/agendamentos/<int:agendamento_id>/concluir")
def concluir_agendamento(agendamento_id):
    if session.get("tipo") != "barbeiros" or not core.conta_ativa():
        return jsonify(erro="Apenas barbeiros podem concluir serviços."), 403

    with sqlite3.connect(core.DB_PATH) as db:
        db.execute("BEGIN IMMEDIATE")
        agendamento = db.execute(
            "SELECT status, data_agendamento, horario, duracao FROM agendamento "
            "WHERE id = ? AND barbeiro_id = ?",
            (agendamento_id, str(session["usuario_id"])),
        ).fetchone()
        if not agendamento:
            return jsonify(erro="Agendamento não encontrado."), 404
        if agendamento[0] != "confirmado":
            return jsonify(erro="Somente agendamentos confirmados podem ser concluídos."), 409

        try:
            fim = core.horario_local(agendamento[1], agendamento[2]) + timedelta(
                minutes=agendamento[3]
            )
        except (TypeError, ValueError):
            return jsonify(erro="Não foi possível validar o horário do agendamento."), 400
        if fim > core.agora_local():
            return jsonify(erro="O serviço só pode ser concluído após o horário agendado."), 409

        db.execute(
            "UPDATE agendamento SET status = 'concluido' WHERE id = ?",
            (agendamento_id,),
        )

    return jsonify(ok=True, status="concluido")

@bp.get("/api/agendamentos")
def listar_agendamentos_barbeiro():
    if session.get("tipo") != "barbeiros" or not core.conta_ativa():
        return jsonify(erro="Apenas barbeiros podem consultar agendamentos."), 403

    ids_barbeiro = [str(session["usuario_id"])]
    marcadores = ", ".join("?" for _ in ids_barbeiro)
    hoje = core.agora_local().date().isoformat()
    if request.args.get("proximo") == "1":
        with sqlite3.connect(core.DB_PATH) as db:
            proxima_data = db.execute(
                f"SELECT MIN(data_agendamento) FROM agendamento "
                f"WHERE data_agendamento >= ? AND barbeiro_id IN ({marcadores}) "
                "AND status = 'confirmado'",
                (hoje, *ids_barbeiro),
            ).fetchone()[0]
        data_texto = proxima_data or hoje
    else:
        data_texto = request.args.get("data", "")
        try:
            data_agendamento = date.fromisoformat(data_texto)
        except ValueError:
            return jsonify(erro="Escolha uma data válida."), 400
        if data_agendamento.isoformat() != data_texto:
            return jsonify(erro="Escolha uma data válida."), 400

    with sqlite3.connect(core.DB_PATH) as db:
        db.row_factory = sqlite3.Row
        agendamentos = [dict(row) for row in db.execute(
            "SELECT a.id, a.servico_nome AS servico, a.horario, a.duracao, a.preco, "
            "c.nome AS cliente FROM agendamento AS a "
            "LEFT JOIN cliente AS c ON c.id = a.cliente_id "
            f"WHERE a.data_agendamento = ? AND a.barbeiro_id IN ({marcadores}) "
            "AND a.status = 'confirmado' "
            "ORDER BY a.horario, a.id",
            (data_texto, *ids_barbeiro),
        )]
    return jsonify(data=data_texto, agendamentos=agendamentos)

@bp.get("/api/meu-agendamento")
def listar_proximos_agendamentos_cliente():
    if session.get("tipo") != "clientes" or not core.conta_ativa():
        return jsonify(erro="Apenas clientes podem consultar seus agendamentos."), 403

    agora = core.agora_local()
    with sqlite3.connect(core.DB_PATH) as db:
        db.row_factory = sqlite3.Row
        agendamentos = db.execute(
            "SELECT id, data_agendamento AS data, horario, servico_nome AS servico, "
            "duracao, preco, barbeiro_nome AS barbeiro, status FROM agendamento "
            "WHERE cliente_id = ? AND data_agendamento >= ? "
            "ORDER BY data_agendamento, horario, id",
            (session["usuario_id"], agora.date().isoformat()),
        ).fetchall()

    proximos_agendamentos = []
    for agendamento in agendamentos:
        inicio = core.horario_local(agendamento["data"], agendamento["horario"])
        fim = inicio + timedelta(minutes=agendamento["duracao"])
        if fim > agora:
            proximos_agendamentos.append(dict(agendamento))

    return jsonify(agendamentos=proximos_agendamentos)

@bp.post("/api/meu-agendamento/<int:agendamento_id>/cancelar")
def cancelar_agendamento_cliente(agendamento_id):
    if session.get("tipo") != "clientes" or not core.conta_ativa():
        return jsonify(erro="Apenas clientes podem cancelar seus agendamentos."), 403

    with sqlite3.connect(core.DB_PATH) as db:
        db.execute("BEGIN IMMEDIATE")
        agendamento = db.execute(
            "SELECT status, data_agendamento, horario FROM agendamento "
            "WHERE id = ? AND cliente_id = ?",
            (agendamento_id, session["usuario_id"]),
        ).fetchone()
        if not agendamento:
            return jsonify(erro="Agendamento não encontrado."), 404
        if agendamento[0] not in ("pendente", "confirmado"):
            return jsonify(erro="Este agendamento não pode mais ser cancelado."), 409
        try:
            inicio = core.horario_local(agendamento[1], agendamento[2])
        except (TypeError, ValueError):
            return jsonify(erro="Não foi possível validar o horário do agendamento."), 400
        if inicio <= core.agora_local():
            return jsonify(erro="Não é possível cancelar um serviço que já começou."), 409
        db.execute(
            "UPDATE agendamento SET status = 'cancelado' WHERE id = ?",
            (agendamento_id,),
        )

    return jsonify(ok=True, status="cancelado")

@bp.delete("/api/meu-agendamento/<int:agendamento_id>")
def excluir_agendamento_cancelado_cliente(agendamento_id):
    if session.get("tipo") != "clientes" or not core.conta_ativa():
        return jsonify(erro="Apenas clientes podem remover seus agendamentos."), 403

    with sqlite3.connect(core.DB_PATH) as db:
        db.execute("BEGIN IMMEDIATE")
        agendamento = db.execute(
            "SELECT status FROM agendamento WHERE id = ? AND cliente_id = ?",
            (agendamento_id, session["usuario_id"]),
        ).fetchone()
        if not agendamento:
            return jsonify(erro="Agendamento não encontrado."), 404
        if agendamento[0] != "cancelado":
            return jsonify(erro="Somente agendamentos cancelados podem ser removidos."), 409
        db.execute("DELETE FROM agendamento WHERE id = ?", (agendamento_id,))

    return "", 204

@bp.get("/api/historico-servicos")
def listar_historico_servicos():
    tipo = session.get("tipo")
    if tipo not in ("clientes", "barbeiros") or not core.conta_ativa():
        return jsonify(erro="Entre em uma conta para consultar o histórico de serviços."), 403

    administrador = tipo == "barbeiros" and core.exigir_administrador()
    consulta = (
        "SELECT a.id, a.data_agendamento AS data, a.horario, "
        "a.servico_nome AS servico, a.duracao, a.preco, "
        "a.barbeiro_nome AS barbeiro, c.nome AS cliente "
        "FROM agendamento AS a LEFT JOIN cliente AS c ON c.id = a.cliente_id "
        "WHERE a.status = 'concluido' "
    )
    parametros = []
    if tipo == "clientes":
        consulta += "AND a.cliente_id = ? "
        parametros.append(session["usuario_id"])
    elif not administrador:
        consulta += "AND a.barbeiro_id = ? "
        parametros.append(str(session["usuario_id"]))
    consulta += "ORDER BY a.data_agendamento DESC, a.horario DESC, a.id DESC"

    with sqlite3.connect(core.DB_PATH) as db:
        db.row_factory = sqlite3.Row
        agendamentos = [dict(row) for row in db.execute(consulta, parametros)]
    return jsonify(historico=agendamentos, administrador=administrador)

@bp.post("/api/agendamentos")
def criar_agendamento():
    if session.get("tipo") != "clientes" or not core.conta_ativa():
        return jsonify(erro="Apenas clientes podem confirmar agendamentos."), 403

    dados = request.get_json(silent=True) or {}
    try:
        servico_id = int(dados.get("servico_id", ""))
    except (TypeError, ValueError):
        return jsonify(erro="Escolha um serviço válido."), 400

    barbeiro_id = str(dados.get("barbeiro_id", "")).strip()
    data_texto = str(dados.get("data", ""))
    horario = str(dados.get("horario", ""))
    try:
        data_agendamento = date.fromisoformat(data_texto)
    except ValueError:
        return jsonify(erro="Escolha uma data válida."), 400
    hoje = core.agora_local().date()
    if data_agendamento.isoformat() != data_texto or data_agendamento < hoje:
        return jsonify(erro="A data do agendamento não pode ser anterior a hoje."), 400

    if not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", horario):
        return jsonify(erro="Escolha um horário válido."), 400
    minutos_inicio = int(horario[:2]) * 60 + int(horario[3:])
    if (
        minutos_inicio < 9 * 60
        or minutos_inicio > 19 * 60 + 30
        or minutos_inicio % 30 != 0
        or horario in ("12:00", "12:30")
    ):
        return jsonify(erro="Esse horário não está disponível."), 400
    agora = core.agora_local()
    if data_agendamento == agora.date() and minutos_inicio <= agora.hour * 60 + agora.minute:
        return jsonify(erro="Esse horário já passou. Escolha outro horário."), 400

    with sqlite3.connect(core.DB_PATH) as db:
        db.execute("BEGIN IMMEDIATE")
        servico = db.execute(
            "SELECT nome, duracao, preco FROM servico WHERE id = ?",
            (servico_id,),
        ).fetchone()
        if not servico:
            return jsonify(erro="O serviço selecionado não existe mais."), 404
        if minutos_inicio + servico[1] > 20 * 60:
            return jsonify(erro="Esse serviço ultrapassa o horário de funcionamento."), 400

        if barbeiro_id.isdecimal():
            barbeiro = db.execute(
                "SELECT nome FROM barbeiro WHERE id = ?",
                (int(barbeiro_id),),
            ).fetchone()
            if not barbeiro:
                return jsonify(erro="O barbeiro selecionado não existe mais."), 404
            barbeiro_nome = barbeiro[0]
        else:
            return jsonify(erro="Escolha um barbeiro válido."), 400

        agendamentos = db.execute(
            "SELECT horario, duracao FROM agendamento "
            "WHERE barbeiro_id = ? AND data_agendamento = ? "
            "AND status IN ('pendente', 'confirmado')",
            (barbeiro_id, data_texto),
        ).fetchall()
        fim_novo = minutos_inicio + servico[1]
        for horario_existente, duracao_existente in agendamentos:
            minutos_existente = int(horario_existente[:2]) * 60 + int(horario_existente[3:])
            if minutos_inicio < minutos_existente + duracao_existente and minutos_existente < fim_novo:
                return jsonify(erro="Esse horário acabou de ser reservado. Escolha outro."), 409

        cursor = db.execute(
            "INSERT INTO agendamento "
            "(cliente_id, servico_id, servico_nome, barbeiro_id, barbeiro_nome, "
            "data_agendamento, horario, duracao, preco, status) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pendente')",
            (
                session["usuario_id"],
                servico_id,
                servico[0],
                barbeiro_id,
                barbeiro_nome,
                data_texto,
                horario,
                servico[1],
                servico[2],
            ),
        )

    return jsonify(
        ok=True,
        agendamento={
            "id": cursor.lastrowid,
            "servico": servico[0],
            "barbeiro": barbeiro_nome,
            "data": data_texto,
            "horario": horario,
            "preco": servico[2],
        },
    ), 201
