import app as app_module


def testar_login_de_cliente_cadastrado(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()
    cliente = app_module.app.test_client()
    cliente.post(
        "/api/clientes",
        json={"nome": "Maria da Silva", "email": "maria@teste.com", "telefone": "41999999999"},
    )
    cliente.post("/api/sair")

    resposta = cliente.post(
        "/api/login",
        json={"email": "MARIA@TESTE.COM", "telefone": "(41) 99999-9999"},
    )

    assert resposta.status_code == 200
    assert cliente.get("/api/sessao").json == {
        "autenticado": True,
        "tipo": "clientes",
        "nome": "Maria da Silva",
    }


def testar_login_rejeita_dados_incorretos(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "fadehouse.db")
    app_module.init_db()

    resposta = app_module.app.test_client().post(
        "/api/login",
        json={"email": "inexistente@teste.com", "telefone": "41999999999"},
    )

    assert resposta.status_code == 401
    assert resposta.json["erro"] == "E-mail ou telefone incorretos."


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
