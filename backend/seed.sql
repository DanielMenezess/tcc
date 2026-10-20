INSERT INTO servico (nome, duracao, preco) VALUES
    ('Corte', 30, 35),
    ('Barba', 20, 25),
    ('Corte + Barba', 50, 55),
    ('Sobrancelha', 10, 15),
    ('Pigmentação', 40, 45)
ON CONFLICT (nome) DO NOTHING;