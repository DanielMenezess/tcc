import app as app_module


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
        json={"tipo": "clientes", "email": "MARIA@TESTE.COM", "senha": "senha-segura-123"},
    )

    assert resposta.status_code == 200
    assert cliente.get("/api/sessao").json == {
        "autenticado": True,
        "tipo": "clientes",
        "nome": "Maria da Silva",
    }


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
        json={"tipo": "clientes", "email": "maria@teste.com", "senha": "senha-errada"},
    )

    assert resposta.status_code == 401
    assert resposta.json["erro"] == "E-mail ou senha incorretos."


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
    assert resposta_cadastro.status_code == 201

    with app_module.sqlite3.connect(app_module.DB_PATH) as db:
        senha_hash = db.execute("SELECT senha_hash FROM barbeiro").fetchone()[0]
    assert senha_hash != "senha-segura-123"

    cliente.post("/api/sair")
    resposta_login = cliente.post(
        "/api/login",
        json={"tipo": "barbeiros", "email": "joao@teste.com", "senha": "senha-segura-123"},
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
            "email": "maria@teste.com",
            "telefone": "(41) 99999-9999",
            "senha": "abc123",
        },
    )

    assert resposta.status_code == 200
    assert cliente.get("/api/sessao").json["nome"] == "Maria da Silva"
    cliente.post("/api/sair")
    resposta_login = cliente.post(
        "/api/login",
        json={"tipo": "clientes", "email": "maria@teste.com", "senha": "abc123"},
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
