CREATE TABLE escolas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    regiao VARCHAR(100),
    ano INT NOT NULL,
    pontuacao_premio NUMERIC(10,2) NOT NULL
);
SELECT table_name FROM information_schema.tables WHERE table_schema='public';

