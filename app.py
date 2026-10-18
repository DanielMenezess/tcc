import importlib

from backend.app import *  # noqa: F401,F403

backend_module = importlib.import_module("backend.app")
app = backend_module.app
DB_PATH = backend_module.DB_PATH


def init_db():
    global DB_PATH
    for name in [
        "DB_PATH",
        "agora_local",
        "horario_local",
        "FUSO_HORARIO",
        "TABELAS",
        "EMAIL_RE",
        "NOME_Barbeiro_RE",
        "ADMIN_NOME",
        "ADMIN_EMAIL",
        "ADMIN_TELEFONE",
        "ADMIN_SENHA",
        "ADMIN_SENHA_HASH",
        "validar",
        "validar_servico",
    ]:
        if name in globals() and hasattr(backend_module, name):
            setattr(backend_module, name, globals()[name])
    backend_module.DB_PATH = DB_PATH
    return backend_module.init_db()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
