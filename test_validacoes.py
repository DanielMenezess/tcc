from datetime import date, timedelta

import app as app_module


def entrar_administrador(cliente):
    return cliente.post(
        "/api/login",
        json={
            "tipo": "barbeiros",
            "identificador": "danielgabriel@gmail.com",
            "senha": "123456",
        },
    )


def testar_migracao_mantem_agendamentos_antigos_confirmados(tmp_path, monkeypatch):
    caminho_db = tmp_path / "fadehouse.db"
    monkeypatch.setattr(app_module, "DB_PATH", caminho_db)
    with app_module.sqlite3.connect(caminho_db) as db:
        db.execute(
            "CREATE TABLE agendamento ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, cliente_id INTEGER NOT NULL, "
            "servico_id INTEGER NOT NULL, servico_nome TEXT NOT NULL, "
            "barbeiro_id TEXT NOT NULL, barbeiro_nome TEXT NOT NULL, "
            "data_agendamento TEXT NOT NULL, horario TEXT NOT NULL, "
            "duracao INTEGER NOT NULL, preco REAL NOT NULL)"
        )
        db.execute(
            "INSERT INTO agendamento "
            "(cliente_id, servico_id, servico_nome, barbeiro_id, barbeiro_nome, "
            "data_agendamento, horario, duracao, preco) "
            "VALUES (1, 1, 'Corte', '1', 'Daniel Gabriel', '2026-10-06', '09:00', 30, 35)"
        )
        db.execute(
            "INSERT INTO agendamento "
            "(cliente_id, servico_id, servico_nome, barbeiro_id, barbeiro_nome, "
            "data_agendamento, horario, duracao, preco) "
            "VALUES (2, 2, 'Barba', '1', 'Daniel Gabriel', ?, '09:00', 20, 25)",
            ((date.today() - timedelta(days=1)).isoformat(),),
        )

    app_module.init_db()

    with app_module.sqlite3.connect(caminho_db) as db:
        assert db.execute("SELECT status FROM agendamento WHERE id = 1").fetchone() == (
            "confirmado",
        )
        assert db.execute("SELECT status FROM agendamento WHERE id = 2").fetchone() == (
            "concluido",
        )
        db.execute(
            "INSERT INTO agendamento "
            "(cliente_id, servico_id, servico_nome, barbeiro_id, barbeiro_nome, "
            "data_agendamento, horario, duracao, preco, status) "
            "VALUES (3, 3, 'Corte + Barba', '1', 'Daniel Gabriel', ?, '09:00', 50, 55, 'confirmado')",
            ((date.today() - timedelta(days=1)).isoformat(),),
        )

    app_module.init_db()

    with app_module.sqlite3.connect(caminho_db) as db:
        assert db.execute("SELECT status FROM agendamento WHERE id = 3").fetchone() == (
            "confirmado",
        )


def testar_login_de_cliente_cadastrado(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()
    cliente = app_module.app.test_client()
    cliente.post(
        "/api/clientes",
        json={
            "nome": "Maria da Silva",
            "email": "maria@teste.com",
            "telefone": "41999999999",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    )
    cliente.post("/api/sair")

    resposta = cliente.post(
        "/api/login",
        json={"tipo": "clientes", "identificador": "MARIA@TESTE.COM", "senha": "senha-segura-123"},
    )

    assert resposta.status_code == 200
    assert cliente.get("/api/sessao").json == {
        "autenticado": True,
        "tipo": "clientes",
        "nome": "Maria da Silva",
    }


def testar_administrador_e_criado_novamente_com_o_banco(tmp_path, monkeypatch):
    caminho_db = tmp_path / "fadehouse.db"
    monkeypatch.setattr(app_module, "DB_PATH", caminho_db)
    app_module.init_db()

    administrador = app_module.app.test_client()
    assert entrar_administrador(administrador).status_code == 200
    assert administrador.get("/api/sessao").json == {
        "autenticado": True,
        "tipo": "barbeiros",
        "nome": "Daniel Gabriel",
        "administrador": True,
    }

    with app_module.sqlite3.connect(caminho_db) as db:
        conta = db.execute(
            "SELECT nome, email, telefone FROM barbeiro WHERE email = ?",
            ("danielgabriel@gmail.com",),
        ).fetchone()
    assert conta == ("Daniel Gabriel", "danielgabriel@gmail.com", "11111111111")

    caminho_db.unlink()
    app_module.init_db()
    administrador_apos_recriacao = app_module.app.test_client()
    resposta = administrador_apos_recriacao.post(
        "/api/login",
        json={
            "tipo": "barbeiros",
            "identificador": "(11) 11111-1111",
            "senha": "123456",
        },
    )
    assert resposta.status_code == 200
    assert administrador_apos_recriacao.get("/api/sessao").json["administrador"] is True


def testar_telefone_administrador_nao_pode_ser_usado_por_outra_conta(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()
    cliente = app_module.app.test_client()

    for tipo, email in (
        ("clientes", "cliente@teste.com"),
        ("barbeiros", "barbeiro@teste.com"),
    ):
        resposta = cliente.post(
            f"/api/{tipo}",
            json={
                "nome": "Maria da Silva" if tipo == "clientes" else "João da Silva",
                "email": email,
                "telefone": "(11) 11111-1111",
                "senha": "senha-segura-123",
                "confirmar_senha": "senha-segura-123",
            },
        )
        assert resposta.status_code == 400
        assert "telefone" in resposta.json["erros"]


def testar_solicitacao_barbeiro_exige_aprovacao_administrativa(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()
    barbeiro = app_module.app.test_client()

    resposta = barbeiro.post(
        "/api/barbeiros",
        json={
            "nome": "João da Silva",
            "email": "joao@teste.com",
            "telefone": "41911111111",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    )
    assert resposta.status_code == 202
    assert barbeiro.post(
        "/api/login",
        json={"tipo": "barbeiros", "identificador": "joao@teste.com", "senha": "senha-segura-123"},
    ).status_code == 401
    assert barbeiro.get("/api/solicitacoes-barbeiros").status_code == 403
    assert barbeiro.post("/api/solicitacoes-barbeiros/1/aprovar").status_code == 403

    administrador = app_module.app.test_client()
    assert entrar_administrador(administrador).status_code == 200
    solicitacao = administrador.get("/api/solicitacoes-barbeiros").json["solicitacoes"][0]
    assert administrador.delete(
        f"/api/solicitacoes-barbeiros/{solicitacao['id']}"
    ).status_code == 204
    assert barbeiro.post(
        "/api/login",
        json={"tipo": "barbeiros", "identificador": "joao@teste.com", "senha": "senha-segura-123"},
    ).status_code == 401


def testar_administrador_lista_contas_separadas_sem_hashes(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()
    cliente = app_module.app.test_client()
    barbeiro = app_module.app.test_client()

    cliente.post(
        "/api/clientes",
        json={
            "nome": "Maria da Silva",
            "email": "maria@teste.com",
            "telefone": "41911111111",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    )
    assert barbeiro.post(
        "/api/barbeiros",
        json={
            "nome": "João da Silva",
            "email": "joao@teste.com",
            "telefone": "41922222222",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    ).status_code == 202

    administrador = app_module.app.test_client()
    assert entrar_administrador(administrador).status_code == 200
    solicitacao = administrador.get("/api/solicitacoes-barbeiros").json["solicitacoes"][0]
    assert administrador.post(
        f"/api/solicitacoes-barbeiros/{solicitacao['id']}/aprovar"
    ).status_code == 200

    assert cliente.get("/api/contas").status_code == 403
    contas = administrador.get("/api/contas")
    assert contas.status_code == 200
    assert [conta["email"] for conta in contas.json["clientes"]] == ["maria@teste.com"]
    assert {conta["email"] for conta in contas.json["barbeiros"]} == {
        app_module.ADMIN_EMAIL,
        "joao@teste.com",
    }
    assert all(
        "senha_hash" not in conta
        for grupo in (contas.json["clientes"], contas.json["barbeiros"])
        for conta in grupo
    )


def testar_administrador_exclui_contas_e_revoga_sessoes(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()
    cliente = app_module.app.test_client()
    barbeiro = app_module.app.test_client()
    administrador = app_module.app.test_client()

    cliente.post(
        "/api/clientes",
        json={
            "nome": "Maria da Silva",
            "email": "maria@teste.com",
            "telefone": "41911111111",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    )
    barbeiro.post(
        "/api/barbeiros",
        json={
            "nome": "João da Silva",
            "email": "joao@teste.com",
            "telefone": "41922222222",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    )
    assert entrar_administrador(administrador).status_code == 200
    solicitacao = administrador.get("/api/solicitacoes-barbeiros").json["solicitacoes"][0]
    assert administrador.post(
        f"/api/solicitacoes-barbeiros/{solicitacao['id']}/aprovar"
    ).status_code == 200
    assert barbeiro.post(
        "/api/login",
        json={"tipo": "barbeiros", "identificador": "joao@teste.com", "senha": "senha-segura-123"},
    ).status_code == 200

    contas = administrador.get("/api/contas").json
    id_cliente = contas["clientes"][0]["id"]
    conta_barbeiro = next(conta for conta in contas["barbeiros"] if conta["email"] == "joao@teste.com")
    id_admin = next(conta["id"] for conta in contas["barbeiros"] if conta["administrador"])

    assert cliente.delete(f"/api/contas/clientes/{id_cliente}").status_code == 403
    assert administrador.delete(f"/api/contas/barbeiros/{id_admin}").status_code == 403
    assert administrador.delete(f"/api/contas/clientes/{id_cliente}").status_code == 200
    assert administrador.delete(f"/api/contas/barbeiros/{conta_barbeiro['id']}").status_code == 200
    assert cliente.get("/api/sessao").json == {"autenticado": False}
    assert barbeiro.get("/api/sessao").json == {"autenticado": False}


def testar_login_rejeita_senha_incorreta(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()
    cliente = app_module.app.test_client()
    cliente.post(
        "/api/clientes",
        json={
            "nome": "Maria da Silva",
            "email": "maria@teste.com",
            "telefone": "41999999999",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    )
    cliente.post("/api/sair")

    resposta = cliente.post(
        "/api/login",
        json={"tipo": "clientes", "identificador": "maria@teste.com", "senha": "senha-errada"},
    )

    assert resposta.status_code == 401
    assert resposta.json["erro"] == "E-mail/telefone ou senha incorretos."


def testar_login_de_cliente_com_telefone(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()
    cliente = app_module.app.test_client()
    cliente.post(
        "/api/clientes",
        json={
            "nome": "Maria da Silva",
            "email": "maria@teste.com",
            "telefone": "41999999999",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    )
    cliente.post("/api/sair")

    resposta = cliente.post(
        "/api/login",
        json={"tipo": "clientes", "identificador": "(41) 99999-9999", "senha": "senha-segura-123"},
    )

    assert resposta.status_code == 200
    assert cliente.get("/api/sessao").json["nome"] == "Maria da Silva"


def testar_email_e_telefone_nao_podem_ser_reutilizados_entre_perfis(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()
    cliente = app_module.app.test_client()

    def cadastrar(perfil, nome, email, telefone):
        return cliente.post(
            f"/api/{perfil}",
            json={
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "senha": "senha-segura-123",
                "confirmar_senha": "senha-segura-123",
            },
        )

    assert cadastrar("clientes", "Maria da Silva", "cliente@teste.com", "41911111111").status_code == 201
    assert cadastrar("barbeiros", "João da Silva", "barbeiro@teste.com", "41922222222").status_code == 202

    email_de_cliente = cadastrar("barbeiros", "Pedro da Silva", "cliente@teste.com", "41933333333")
    assert email_de_cliente.status_code == 409
    assert "email" in email_de_cliente.json["erros"]

    telefone_de_cliente = cadastrar("barbeiros", "Pedro da Silva", "pedro@teste.com", "41911111111")
    assert telefone_de_cliente.status_code == 409
    assert "telefone" in telefone_de_cliente.json["erros"]

    email_de_barbeiro = cadastrar("clientes", "Ana da Silva", "barbeiro@teste.com", "41944444444")
    assert email_de_barbeiro.status_code == 409
    assert "email" in email_de_barbeiro.json["erros"]

    telefone_de_barbeiro = cadastrar("clientes", "Ana da Silva", "ana@teste.com", "41922222222")
    assert telefone_de_barbeiro.status_code == 409
    assert "telefone" in telefone_de_barbeiro.json["erros"]


def testar_cliente_confirma_agendamento(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()
    cliente = app_module.app.test_client()
    cliente.post(
        "/api/clientes",
        json={
            "nome": "Maria da Silva",
            "email": "maria@teste.com",
            "telefone": "41999999999",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    )
    with app_module.sqlite3.connect(app_module.DB_PATH) as db:
        barbeiro_id = db.execute(
            "SELECT id FROM barbeiro WHERE email = ?", (app_module.ADMIN_EMAIL,)
        ).fetchone()[0]

    data_primeiro = (date.today() + timedelta(days=1)).isoformat()
    resposta = cliente.post(
        "/api/agendamentos",
        json={
            "servico_id": 1,
            "barbeiro_id": str(barbeiro_id),
            "data": data_primeiro,
            "horario": "09:00",
        },
    )

    assert resposta.status_code == 201
    assert resposta.json["agendamento"]["servico"] == "Corte"
    assert resposta.json["agendamento"]["barbeiro"] == "Daniel Gabriel"
    data_segundo = (date.today() + timedelta(days=2)).isoformat()
    assert cliente.post(
        "/api/agendamentos",
        json={
            "servico_id": 2,
            "barbeiro_id": str(barbeiro_id),
            "data": data_segundo,
            "horario": "10:00",
        },
    ).status_code == 201
    agendamentos = cliente.get("/api/meu-agendamento").json["agendamentos"]
    assert agendamentos == [
        {
            "id": 1,
            "data": data_primeiro,
            "horario": "09:00",
            "servico": "Corte",
            "duracao": 30,
            "preco": 35.0,
            "barbeiro": "Daniel Gabriel",
            "status": "pendente",
        },
        {
            "id": 2,
            "data": data_segundo,
            "horario": "10:00",
            "servico": "Barba",
            "duracao": 20,
            "preco": 25.0,
            "barbeiro": "Daniel Gabriel",
            "status": "pendente",
        },
    ]
    assert app_module.app.test_client().get("/api/meu-agendamento").status_code == 403
    assert cliente.get("/api/agendamentos-pendentes").status_code == 403
    barbeiro = app_module.app.test_client()
    assert barbeiro.post(
        "/api/login",
        json={
            "tipo": "barbeiros",
            "identificador": app_module.ADMIN_EMAIL,
            "senha": app_module.ADMIN_SENHA,
        },
    ).status_code == 200
    pendentes = barbeiro.get("/api/agendamentos-pendentes")
    assert pendentes.status_code == 200
    assert [item["id"] for item in pendentes.json["agendamentos"]] == [1, 2]
    decisao = barbeiro.post("/api/agendamentos/1/decisao", json={"status": "confirmado"})
    assert decisao.status_code == 200
    assert [
        item["id"] for item in barbeiro.get("/api/agendamentos-pendentes").json["agendamentos"]
    ] == [2]
    aguardando_conclusao = barbeiro.get("/api/agendamentos-a-concluir")
    assert aguardando_conclusao.status_code == 200
    assert [item["id"] for item in aguardando_conclusao.json["agendamentos"]] == [1]
    assert barbeiro.post("/api/agendamentos/1/concluir").status_code == 409
    agendamentos = cliente.get("/api/meu-agendamento").json["agendamentos"]
    assert [item["status"] for item in agendamentos] == ["confirmado", "pendente"]
    assert cliente.delete("/api/meu-agendamento/1").status_code == 409
    assert barbeiro.post(
        "/api/agendamentos/1/decisao", json={"status": "cancelado"}
    ).status_code == 409
    with app_module.sqlite3.connect(app_module.DB_PATH) as db:
        assert db.execute("SELECT COUNT(*) FROM agendamento").fetchone()[0] == 2


def testar_agendamento_do_mesmo_dia_usa_fuso_de_brasilia(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    agora = app_module.datetime(2026, 10, 5, 16, 57, tzinfo=app_module.FUSO_HORARIO)
    monkeypatch.setattr(app_module, "agora_local", lambda: agora)
    app_module.init_db()
    cliente = app_module.app.test_client()
    assert cliente.post(
        "/api/clientes",
        json={
            "nome": "Maria da Silva",
            "email": "maria@teste.com",
            "telefone": "41999999999",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    ).status_code == 201

    with app_module.sqlite3.connect(app_module.DB_PATH) as db:
        barbeiro_id = db.execute(
            "SELECT id FROM barbeiro WHERE email = ?", (app_module.ADMIN_EMAIL,)
        ).fetchone()[0]

    dados = {
        "servico_id": 1,
        "barbeiro_id": str(barbeiro_id),
        "data": "2026-10-05",
        "horario": "16:30",
    }
    horario_passado = cliente.post("/api/agendamentos", json=dados)
    assert horario_passado.status_code == 400
    assert "já passou" in horario_passado.json["erro"]

    dados["horario"] = "17:00"
    assert cliente.post("/api/agendamentos", json=dados).status_code == 201


def testar_conclusao_do_servico_move_agendamento_para_historico(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()
    cliente = app_module.app.test_client()
    solicitante = app_module.app.test_client()
    barbeiro = app_module.app.test_client()
    administrador = app_module.app.test_client()

    assert cliente.post(
        "/api/clientes",
        json={
            "nome": "Maria da Silva",
            "email": "maria@teste.com",
            "telefone": "41911111111",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    ).status_code == 201
    assert solicitante.post(
        "/api/barbeiros",
        json={
            "nome": "João da Silva",
            "email": "joao@teste.com",
            "telefone": "41922222222",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    ).status_code == 202
    assert entrar_administrador(administrador).status_code == 200
    solicitacao = administrador.get("/api/solicitacoes-barbeiros").json["solicitacoes"][0]
    assert administrador.post(
        f"/api/solicitacoes-barbeiros/{solicitacao['id']}/aprovar"
    ).status_code == 200
    assert barbeiro.post(
        "/api/login",
        json={"tipo": "barbeiros", "identificador": "joao@teste.com", "senha": "senha-segura-123"},
    ).status_code == 200

    ontem = (date.today() - timedelta(days=1)).isoformat()
    with app_module.sqlite3.connect(app_module.DB_PATH) as db:
        id_cliente = db.execute(
            "SELECT id FROM cliente WHERE email = ?", ("maria@teste.com",)
        ).fetchone()[0]
        id_barbeiro = db.execute(
            "SELECT id FROM barbeiro WHERE email = ?", ("joao@teste.com",)
        ).fetchone()[0]
        db.execute(
            "INSERT INTO agendamento "
            "(cliente_id, servico_id, servico_nome, barbeiro_id, barbeiro_nome, "
            "data_agendamento, horario, duracao, preco, status) "
            "VALUES (?, 1, 'Corte', ?, 'João da Silva', ?, '09:00', 30, 35, 'pendente')",
            (id_cliente, str(id_barbeiro), ontem),
        )

    assert barbeiro.post("/api/agendamentos/1/concluir").status_code == 409
    fila_admin = administrador.get("/api/agendamentos-pendentes")
    assert fila_admin.status_code == 200
    assert fila_admin.json["administrador"] is True
    assert [item["id"] for item in fila_admin.json["agendamentos"]] == [1]
    assert fila_admin.json["agendamentos"][0]["barbeiro"] == "João da Silva"
    assert administrador.post(
        "/api/agendamentos/1/decisao", json={"status": "confirmado"}
    ).status_code == 200
    assert barbeiro.get("/api/agendamentos-a-concluir").json["agendamentos"][0]["id"] == 1
    assert [item["id"] for item in barbeiro.get(
        "/api/agendamentos-a-concluir"
    ).json["agendamentos"]] == [1]
    fila_admin_conclusao = administrador.get("/api/agendamentos-a-concluir")
    assert fila_admin_conclusao.json["administrador"] is True
    assert fila_admin_conclusao.json["agendamentos"][0]["barbeiro"] == "João da Silva"
    assert barbeiro.get("/api/historico-servicos").json["historico"] == []
    assert administrador.get("/api/historico-servicos").json["historico"] == []

    conclusao = barbeiro.post("/api/agendamentos/1/concluir")
    assert conclusao.status_code == 200
    assert conclusao.json["status"] == "concluido"
    assert barbeiro.get("/api/agendamentos-a-concluir").json["agendamentos"] == []
    assert barbeiro.get("/api/historico-servicos").json["historico"][0]["servico"] == "Corte"
    historico_admin = administrador.get("/api/historico-servicos").json["historico"]
    assert [(item["barbeiro"], item["servico"]) for item in historico_admin] == [
        ("João da Silva", "Corte")
    ]
    assert barbeiro.post("/api/agendamentos/1/concluir").status_code == 409


def testar_recusa_cancela_agendamento_e_libera_o_horario(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()
    cliente = app_module.app.test_client()
    cliente.post(
        "/api/clientes",
        json={
            "nome": "Maria da Silva",
            "email": "maria@teste.com",
            "telefone": "41999999999",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    )
    dia = (date.today() + timedelta(days=1)).isoformat()
    with app_module.sqlite3.connect(app_module.DB_PATH) as db:
        barbeiro_id = db.execute(
            "SELECT id FROM barbeiro WHERE email = ?", (app_module.ADMIN_EMAIL,)
        ).fetchone()[0]

    dados = {"servico_id": 1, "barbeiro_id": str(barbeiro_id), "data": dia, "horario": "09:00"}
    assert cliente.post("/api/agendamentos", json=dados).status_code == 201
    barbeiro = app_module.app.test_client()
    assert barbeiro.post(
        "/api/login",
        json={
            "tipo": "barbeiros",
            "identificador": app_module.ADMIN_EMAIL,
            "senha": app_module.ADMIN_SENHA,
        },
    ).status_code == 200
    assert barbeiro.post(
        "/api/agendamentos/1/decisao", json={"status": "cancelado"}
    ).status_code == 200
    assert cliente.get("/api/meu-agendamento").json["agendamentos"][0]["status"] == "cancelado"

    outra_cliente = app_module.app.test_client()
    assert outra_cliente.post(
        "/api/clientes",
        json={
            "nome": "Ana da Silva",
            "email": "ana@teste.com",
            "telefone": "41988888888",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    ).status_code == 201
    assert outra_cliente.delete("/api/meu-agendamento/1").status_code == 404
    assert cliente.delete("/api/meu-agendamento/1").status_code == 204
    assert cliente.get("/api/meu-agendamento").json["agendamentos"] == []
    assert cliente.post("/api/agendamentos", json=dados).status_code == 201


def testar_barbeiro_consulta_apenas_sua_agenda_na_data_escolhida(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()
    barbeiro = app_module.app.test_client()
    outro_barbeiro = app_module.app.test_client()
    cliente = app_module.app.test_client()

    resposta_solicitacao = barbeiro.post(
        "/api/barbeiros",
        json={
            "nome": "João da Silva",
            "email": "joao@teste.com",
            "telefone": "41911111111",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    )
    resposta_outra_solicitacao = outro_barbeiro.post(
        "/api/barbeiros",
        json={
            "nome": "Carlos Souza",
            "email": "carlos@teste.com",
            "telefone": "41922222222",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    )
    assert resposta_solicitacao.status_code == 202
    assert resposta_outra_solicitacao.status_code == 202
    administrador = app_module.app.test_client()
    assert entrar_administrador(administrador).status_code == 200
    solicitacoes = administrador.get("/api/solicitacoes-barbeiros").json["solicitacoes"]
    for solicitacao in solicitacoes:
        assert administrador.post(
            f"/api/solicitacoes-barbeiros/{solicitacao['id']}/aprovar"
        ).status_code == 200
    assert barbeiro.post(
        "/api/login",
        json={"tipo": "barbeiros", "identificador": "joao@teste.com", "senha": "senha-segura-123"},
    ).status_code == 200
    assert outro_barbeiro.post(
        "/api/login",
        json={"tipo": "barbeiros", "identificador": "carlos@teste.com", "senha": "senha-segura-123"},
    ).status_code == 200
    cliente.post(
        "/api/clientes",
        json={
            "nome": "Maria da Silva",
            "email": "maria@teste.com",
            "telefone": "41933333333",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    )

    hoje = date.today().isoformat()
    amanha = (date.today() + timedelta(days=1)).isoformat()
    with app_module.sqlite3.connect(app_module.DB_PATH) as db:
        id_barbeiro = db.execute(
            "SELECT id FROM barbeiro WHERE email = ?", ("joao@teste.com",)
        ).fetchone()[0]
        id_outro_barbeiro = db.execute(
            "SELECT id FROM barbeiro WHERE email = ?", ("carlos@teste.com",)
        ).fetchone()[0]
        db.executemany(
            "INSERT INTO agendamento "
            "(cliente_id, servico_id, servico_nome, barbeiro_id, barbeiro_nome, "
            "data_agendamento, horario, duracao, preco) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (1, 1, "Corte", str(id_barbeiro), "João da Silva", hoje, "09:00", 30, 35),
                (1, 2, "Barba", str(id_barbeiro), "João da Silva", amanha, "10:00", 20, 25),
                (1, 3, "Corte + Barba", str(id_outro_barbeiro), "Carlos Souza", hoje, "11:00", 50, 55),
            ],
        )

    resposta = barbeiro.get(f"/api/agendamentos?data={hoje}")

    assert resposta.status_code == 200
    assert resposta.json["agendamentos"] == [
        {
            "id": 1,
            "servico": "Corte",
            "horario": "09:00",
            "duracao": 30,
            "preco": 35.0,
            "cliente": "Maria da Silva",
        }
    ]
    assert cliente.get(f"/api/agendamentos?data={hoje}").status_code == 403


def testar_agenda_inicia_na_proxima_data_com_agendamentos(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()
    administrador = app_module.app.test_client()
    assert entrar_administrador(administrador).status_code == 200

    proximo_dia = (date.today() + timedelta(days=1)).isoformat()
    outro_dia = (date.today() + timedelta(days=2)).isoformat()
    with app_module.sqlite3.connect(app_module.DB_PATH) as db:
        id_admin = db.execute(
            "SELECT id FROM barbeiro WHERE email = ?", (app_module.ADMIN_EMAIL,)
        ).fetchone()[0]
        db.executemany(
            "INSERT INTO agendamento "
            "(cliente_id, servico_id, servico_nome, barbeiro_id, barbeiro_nome, "
            "data_agendamento, horario, duracao, preco) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (1, 1, "Corte", str(id_admin), "Daniel Gabriel", proximo_dia, "09:00", 30, 35),
                (1, 2, "Barba", str(id_admin), "Daniel Gabriel", outro_dia, "10:00", 20, 25),
            ],
        )

    resposta = administrador.get("/api/agendamentos?proximo=1")

    assert resposta.status_code == 200
    assert resposta.json["data"] == proximo_dia
    assert [item["servico"] for item in resposta.json["agendamentos"]] == ["Corte"]


def testar_historico_mostra_servicos_passados_apenas_do_barbeiro_ou_de_todos_para_admin(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()
    barbeiro = app_module.app.test_client()
    outro_barbeiro = app_module.app.test_client()
    cliente = app_module.app.test_client()

    barbeiro.post(
        "/api/barbeiros",
        json={
            "nome": "João da Silva",
            "email": "joao@teste.com",
            "telefone": "41911111111",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    )
    outro_barbeiro.post(
        "/api/barbeiros",
        json={
            "nome": "Carlos Souza",
            "email": "carlos@teste.com",
            "telefone": "41922222222",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    )
    administrador = app_module.app.test_client()
    assert entrar_administrador(administrador).status_code == 200
    solicitacoes = administrador.get("/api/solicitacoes-barbeiros").json["solicitacoes"]
    for solicitacao in solicitacoes:
        assert administrador.post(
            f"/api/solicitacoes-barbeiros/{solicitacao['id']}/aprovar"
        ).status_code == 200

    for sessao, email in ((barbeiro, "joao@teste.com"), (outro_barbeiro, "carlos@teste.com")):
        assert sessao.post(
            "/api/login",
            json={"tipo": "barbeiros", "identificador": email, "senha": "senha-segura-123"},
        ).status_code == 200

    cliente.post(
        "/api/clientes",
        json={
            "nome": "Maria da Silva",
            "email": "maria@teste.com",
            "telefone": "41933333333",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    )
    ontem = (date.today() - timedelta(days=1)).isoformat()
    amanha = (date.today() + timedelta(days=1)).isoformat()
    with app_module.sqlite3.connect(app_module.DB_PATH) as db:
        id_cliente = db.execute(
            "SELECT id FROM cliente WHERE email = ?", ("maria@teste.com",)
        ).fetchone()[0]
        id_barbeiro = db.execute(
            "SELECT id FROM barbeiro WHERE email = ?", ("joao@teste.com",)
        ).fetchone()[0]
        id_outro_barbeiro = db.execute(
            "SELECT id FROM barbeiro WHERE email = ?", ("carlos@teste.com",)
        ).fetchone()[0]
        id_admin = db.execute(
            "SELECT id FROM barbeiro WHERE email = ?", (app_module.ADMIN_EMAIL,)
        ).fetchone()[0]
        db.executemany(
            "INSERT INTO agendamento "
            "(cliente_id, servico_id, servico_nome, barbeiro_id, barbeiro_nome, "
            "data_agendamento, horario, duracao, preco, status) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (id_cliente, 1, "Corte", str(id_barbeiro), "João da Silva", ontem, "09:00", 30, 35, "concluido"),
                (id_cliente, 2, "Barba", str(id_barbeiro), "João da Silva", amanha, "10:00", 20, 25, "confirmado"),
                (id_cliente, 3, "Corte + Barba", str(id_outro_barbeiro), "Carlos Souza", ontem, "11:00", 50, 55, "concluido"),
                (id_cliente, 4, "Sobrancelha", str(id_admin), "Daniel Gabriel", ontem, "12:00", 10, 15, "concluido"),
            ],
        )

    historico_barbeiro = barbeiro.get("/api/historico-servicos")
    assert historico_barbeiro.status_code == 200
    assert [item["servico"] for item in historico_barbeiro.json["historico"]] == ["Corte"]
    assert cliente.get("/api/historico-servicos").status_code == 403

    historico_admin = administrador.get("/api/historico-servicos")
    assert historico_admin.status_code == 200
    assert historico_admin.json["administrador"] is True
    assert {item["barbeiro"] for item in historico_admin.json["historico"]} == {
        "João da Silva",
        "Carlos Souza",
        "Daniel Gabriel",
    }
    assert all(item["data"] == ontem for item in historico_admin.json["historico"])


def testar_agendamento_rejeita_horario_sobreposto(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()
    cliente = app_module.app.test_client()
    cliente.post(
        "/api/clientes",
        json={
            "nome": "Maria da Silva",
            "email": "maria@teste.com",
            "telefone": "41999999999",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    )
    with app_module.sqlite3.connect(app_module.DB_PATH) as db:
        barbeiro_id = db.execute(
            "SELECT id FROM barbeiro WHERE email = ?", (app_module.ADMIN_EMAIL,)
        ).fetchone()[0]
    dados = {
        "servico_id": 3,
        "barbeiro_id": str(barbeiro_id),
        "data": (date.today() + timedelta(days=1)).isoformat(),
        "horario": "09:00",
    }
    assert cliente.post("/api/agendamentos", json=dados).status_code == 201

    dados["servico_id"] = 1
    dados["horario"] = "09:30"
    resposta = cliente.post("/api/agendamentos", json=dados)

    assert resposta.status_code == 409
    assert "reservado" in resposta.json["erro"]


def testar_barbeiro_fixo_joao_nao_e_listado_ou_aceito(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()
    cliente = app_module.app.test_client()

    barbeiros = cliente.get("/api/barbeiros").json["barbeiros"]
    assert all(barbeiro["id"] != "fixo-joao" for barbeiro in barbeiros)

    cliente.post(
        "/api/clientes",
        json={
            "nome": "Maria da Silva",
            "email": "maria@teste.com",
            "telefone": "41999999999",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    )
    resposta = cliente.post(
        "/api/agendamentos",
        json={
            "servico_id": 1,
            "barbeiro_id": "fixo-joao",
            "data": (date.today() + timedelta(days=1)).isoformat(),
            "horario": "09:00",
        },
    )
    assert resposta.status_code == 400
    assert "barbeiro" in resposta.json["erro"]


def testar_agendamento_exige_sessao_de_cliente(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()

    resposta = app_module.app.test_client().post("/api/agendamentos", json={})

    assert resposta.status_code == 403


def testar_senha_e_armazenada_com_hash_e_login_de_barbeiro(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()
    cliente = app_module.app.test_client()
    resposta_cadastro = cliente.post(
        "/api/barbeiros",
        json={
            "nome": "João da Silva",
            "email": "joao@teste.com",
            "telefone": "41999999999",
            "senha": "senha-segura-123",
            "confirmar_senha": "senha-segura-123",
        },
    )
    assert resposta_cadastro.status_code == 202

    administrador = app_module.app.test_client()
    assert entrar_administrador(administrador).status_code == 200
    solicitacao = next(
        item for item in administrador.get("/api/solicitacoes-barbeiros").json["solicitacoes"]
        if item["email"] == "joao@teste.com"
    )
    assert administrador.post(
        f"/api/solicitacoes-barbeiros/{solicitacao['id']}/aprovar"
    ).status_code == 200

    with app_module.sqlite3.connect(app_module.DB_PATH) as db:
        senha_hash = db.execute(
            "SELECT senha_hash FROM barbeiro WHERE email = ?", ("joao@teste.com",)
        ).fetchone()[0]
    assert senha_hash != "senha-segura-123"

    cliente.post("/api/sair")
    resposta_login = cliente.post(
        "/api/login",
        json={"tipo": "barbeiros", "identificador": "joao@teste.com", "senha": "senha-segura-123"},
    )
    assert resposta_login.status_code == 200
    assert cliente.get("/api/sessao").json["tipo"] == "barbeiros"


def testar_cadastro_exige_senha(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()

    resposta = app_module.app.test_client().post(
        "/api/clientes",
        json={
            "nome": "Maria da Silva",
            "email": "maria@teste.com",
            "telefone": "41999999999",
            "senha": "12345",
            "confirmar_senha": "12345",
        },
    )

    assert resposta.status_code == 400
    assert "senha" in resposta.json["erros"]


def testar_cadastro_aceita_seis_caracteres_e_rejeita_confirmacao_diferente(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()
    cliente = app_module.app.test_client()

    resposta_senha_curta_valida = cliente.post(
        "/api/clientes",
        json={
            "nome": "Maria da Silva",
            "email": "maria@teste.com",
            "telefone": "41999999999",
            "senha": "abc123",
            "confirmar_senha": "abc123",
        },
    )
    assert resposta_senha_curta_valida.status_code == 201

    cliente.post("/api/sair")
    resposta_senha_diferente = cliente.post(
        "/api/clientes",
        json={
            "nome": "Ana da Silva",
            "email": "ana@teste.com",
            "telefone": "41988888888",
            "senha": "abc123",
            "confirmar_senha": "abc124",
        },
    )
    assert resposta_senha_diferente.status_code == 400
    assert "confirmar_senha" in resposta_senha_diferente.json["erros"]


def testar_init_db_migra_tabelas_antigas_sem_apagar_contas(tmp_path, monkeypatch):
    caminho_db = tmp_path / "fadehouse.db"
    monkeypatch.setattr(app_module, "DB_PATH", caminho_db)
    with app_module.sqlite3.connect(caminho_db) as db:
        for tabela in ("cliente", "barbeiro"):
            db.execute(
                f"CREATE TABLE {tabela} ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "nome TEXT NOT NULL, email TEXT NOT NULL UNIQUE, telefone TEXT NOT NULL)"
            )
        db.execute(
            "INSERT INTO cliente (nome, email, telefone) VALUES (?, ?, ?)",
            ("Maria da Silva", "maria@teste.com", "41999999999"),
        )

    app_module.init_db()

    with app_module.sqlite3.connect(caminho_db) as db:
        cliente = db.execute("SELECT nome, senha_hash FROM cliente").fetchone()
    assert cliente == ("Maria da Silva", None)


def testar_conta_antiga_define_senha_no_primeiro_acesso(tmp_path, monkeypatch):
    caminho_db = tmp_path / "fadehouse.db"
    monkeypatch.setattr(app_module, "DB_PATH", caminho_db)
    with app_module.sqlite3.connect(caminho_db) as db:
        for tabela in ("cliente", "barbeiro"):
            db.execute(
                f"CREATE TABLE {tabela} ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "nome TEXT NOT NULL, email TEXT NOT NULL UNIQUE, telefone TEXT NOT NULL)"
            )
        db.execute(
            "INSERT INTO cliente (nome, email, telefone) VALUES (?, ?, ?)",
            ("Maria da Silva", "maria@teste.com", "41999999999"),
        )
    app_module.init_db()
    cliente = app_module.app.test_client()

    resposta = cliente.post(
        "/api/login",
        json={
            "tipo": "clientes",
            "identificador": "(41) 99999-9999",
            "senha": "abc123",
        },
    )

    assert resposta.status_code == 200
    assert cliente.get("/api/sessao").json["nome"] == "Maria da Silva"
    cliente.post("/api/sair")
    resposta_login = cliente.post(
        "/api/login",
        json={"tipo": "clientes", "identificador": "maria@teste.com", "senha": "abc123"},
    )
    assert resposta_login.status_code == 200


def testar_nome_de_barbeiro_valido():
    dados = {
        "nome": "João da Silva",
        "email": "joao@teste.com",
        "telefone": "41999999999",
    }

    resultado, erros = app_module.validar(dados, tipo="barbeiros")

    assert erros == {}
    assert resultado["nome"] == "João da Silva"


def testar_nome_de_conta_nao_aceita_numeros_em_nenhum_perfil(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()
    cliente = app_module.app.test_client()

    for tipo, nome, email in (
        ("clientes", "Maria 2 Silva", "maria@teste.com"),
        ("barbeiros", "João 2 Silva", "joao@teste.com"),
    ):
        resposta = cliente.post(
            f"/api/{tipo}",
            json={
                "nome": nome,
                "email": email,
                "telefone": "41999999999" if tipo == "clientes" else "41988888888",
                "senha": "senha-segura-123",
                "confirmar_senha": "senha-segura-123",
            },
        )
        assert resposta.status_code == 400
        assert resposta.json["erros"]["nome"] == "O nome da conta não pode conter números."


def testar_nome_de_barbeiro_rejeita_minusculo_e_caracteres_invalidos():
    casos_invalidos = [
        "joão da Silva",
        "Joao1 da Silva",
        "João/da Silva",
        "João@Silva",
    ]

    for nome in casos_invalidos:
        dados = {
            "nome": nome,
            "email": "teste@teste.com",
            "telefone": "41999999999",
        }

        _, erros = app_module.validar(dados, tipo="barbeiros")

        assert "nome" in erros
