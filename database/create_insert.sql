--Cria a tabela dos usuarios
CREATE TABLE IF NOT EXISTS USERS (
    userId SERIAL PRIMARY KEY,
    login VARCHAR(60) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    tipo VARCHAR(20) NOT NULL 
        CHECK (tipo IN ('Administrador', 'Escuderia', 'Piloto')),
    idOriginal INTEGER NOT NULL
);

CREATE EXTENSION IF NOT EXISTS pgcrypto;

--Insere o administrador na base (apenas se não existir)
INSERT INTO USERS (userId, login, password, tipo, idOriginal)
SELECT 0, 'admin', encode(digest('admin', 'sha256'), 'hex'), 'Administrador', 1
WHERE NOT EXISTS (SELECT 1 FROM USERS WHERE login = 'admin');

--Insere os pilotos da tabela DRIVERS (apenas os que não existem)
INSERT INTO USERS (login, password, tipo, idOriginal)
SELECT
    CONCAT(driverref, ' d') AS login,
    encode(digest(driverref, 'sha256'), 'hex') AS password,
    'Piloto',
    driverId
FROM 
    DRIVERS
WHERE CONCAT(driverref, ' d') NOT IN (SELECT login FROM USERS);

--Insere as escuderias da tabela CONSTRUCTORS (apenas as que não existem)
INSERT INTO USERS (login, password, tipo, idOriginal)
SELECT 
    CONCAT(constructorref, ' c') AS login,
    encode(digest(constructorref, 'sha256'), 'hex') AS password,
    'Escuderia',
    constructorId
FROM 
    CONSTRUCTORS
WHERE CONCAT(constructorref, ' c') NOT IN (SELECT login FROM USERS);


--Cria tabela de Log de Usuários
CREATE TABLE IF NOT EXISTS USERS_LOG (
    logId SERIAL PRIMARY KEY,
    userId INTEGER NOT NULL,
    diaHora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (userId) REFERENCES USERS(userId)
);
