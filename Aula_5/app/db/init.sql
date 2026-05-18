DROP TABLE IF EXISTS alunos;

CREATE TABLE alunos (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    curso TEXT NOT NULL,
    matricula INTEGER NOT NULL
);
