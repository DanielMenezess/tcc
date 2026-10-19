-- Schema do Fade House (SQLite).
-- O backend cria a conta administradora e armazena a senha usando hash.

CREATE TABLE cliente (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT NOT NULL,
    email       TEXT NOT NULL UNIQUE,
    telefone    TEXT NOT NULL,
    senha_hash  TEXT
);

CREATE TABLE barbeiro (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT NOT NULL,
    email       TEXT NOT NULL UNIQUE,
    telefone    TEXT NOT NULL,
    senha_hash  TEXT
);

CREATE TABLE servico (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    nome     TEXT NOT NULL UNIQUE,
    duracao  INT NOT NULL,
    preco    REAL NOT NULL
);

CREATE TABLE agendamento (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id        INTEGER NOT NULL,
    servico_id        INTEGER NOT NULL,
    servico_nome      TEXT NOT NULL,
    barbeiro_id       TEXT NOT NULL,
    barbeiro_nome     TEXT NOT NULL,
    data_agendamento  TEXT NOT NULL,
    horario           TEXT NOT NULL,
    duracao           INT NOT NULL,
    preco             REAL NOT NULL,
    status            TEXT NOT NULL DEFAULT 'confirmado'
);

CREATE TABLE solicitacao_barbeiro (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT NOT NULL,
    email       TEXT NOT NULL UNIQUE,
    telefone    TEXT NOT NULL UNIQUE,
    senha_hash  TEXT NOT NULL
);

CREATE TABLE app_migracao (
    nome TEXT PRIMARY KEY
);

CREATE INDEX idx_agendamento_barbeiro_data_status
    ON agendamento (barbeiro_id, data_agendamento, status);

CREATE INDEX idx_agendamento_cliente_data
    ON agendamento (cliente_id, data_agendamento);

CREATE INDEX idx_agendamento_status_data_horario
    ON agendamento (status, data_agendamento, horario);