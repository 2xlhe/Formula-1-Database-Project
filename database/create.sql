--Cria a tabela dos usuarios
CREATE TABLE USERS (
    userId SERIAL PRIMARY KEY,
    login VARCHAR(60) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    tipo VARCHAR(20) NOT NULL 
        CHECK (tipo IN ('Administrador', 'Escuderia', 'Piloto')),
    idOriginal INTEGER NOT NULL
);

--Insere o administrador
INSERT INTO USERS VALUES (0, 'admin', encode(digest('admin', 'sha256'), 'hex'), 'Administrador', 1);

--Insere os pilotos
INSERT INTO USERS (login, password, tipo, idOriginal)
SELECT
    CONCAT(driverref, ' d') AS login,
    encode(digest(driverref, 'sha256'), 'hex') AS password,
    'Piloto',
    driverId
FROM 
    DRIVERS;

--Insere as escuderias
INSERT INTO USERS (login, password, tipo, idOriginal)
SELECT 
    CONCAT(constructorref, ' c') AS login,
    encode(digest(constructorref, 'sha256'), 'hex') AS password,
    'Escuderia',
    constructorId
FROM 
    CONSTRUCTORS;


--Cria tabela de log de usuario
CREATE TABLE USERS_LOG (
    logId SERIAL PRIMARY KEY,
    userId INTEGER NOT NULL,
    diaHora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY userId REFERENCES USERS(userId)

) ;
