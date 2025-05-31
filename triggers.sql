--Atualiza USERS sempre que um piloto é atualizado (update, insert ou delete)
CREATE OR REPLACE FUNCTION atualiza_users_pilotos() RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'UPDATE') THEN
        UPDATE USERS SET 
            login = NEW.driverref || ' d',
            password = encode(digest(NEW.driverref, 'sha256'), 'hex')
        WHERE
            tipo = 'Piloto'
        AND
            idOriginal = NEW.driverId;
    
    ELSIF (TG_OP = 'INSERT') THEN 
        INSERT INTO USERS (login, password, tipo, idOriginal)
        VALUES (NEW.driverref || ' d', encode(digest(NEW.driverref, 'sha256'), 'hex'), 'Piloto', NEW.driverId);
    
    ELSIF (TG_OP = 'DELETE') THEN
        DELETE FROM USERS 
        WHERE
            tipo = 'Piloto'
        AND
            idOriginal = OLD.driverId;

    END IF;
    RETURN NULL;
END; 
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_atualiza_users_pilotos
AFTER UPDATE OR INSERT OR DELETE ON DRIVERS
FOR EACH ROW EXECUTE FUNCTION atualiza_users_pilotos();


--Atualiza USERS sempre que constructors é atualizada
CREATE OR REPLACE FUNCTION atualiza_users_escuderias() RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'UPDATE') THEN
        UPDATE USERS SET 
            login = NEW.constructorref || ' d',
            password = encode(digest(NEW.constructorref, 'sha256'), 'hex')
        WHERE
            tipo = 'Escuderia'
        AND
            idOriginal = NEW.constructorId;
    
    ELSIF (TG_OP = 'INSERT') THEN 
        INSERT INTO USERS (login, password, tipo, idOriginal)
        VALUES (NEW.constructorref || ' c', encode(digest(NEW.driverref, 'sha256'), 'hex'), 'Escuderia', NEW.constructorId);
    
    ELSIF (TG_OP = 'DELETE') THEN
        DELETE FROM USERS 
        WHERE
            tipo = 'Escuderia'
        AND
            idOriginal = OLD.constructorId;

    END IF;
    RETURN NULL;
END; 
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_atualiza_users_escuderias
AFTER UPDATE OR INSERT OR DELETE ON CONSTRUCTORS
FOR EACH ROW EXECUTE FUNCTION atualiza_users_escuderias();