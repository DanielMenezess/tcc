import app as app_module


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
