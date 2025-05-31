--funcao para exibir as funcoes pedidas no dashboard da escuderia.
--Precisamos listar o nome da escuderia (a partir do id) e a quantidade
--de pilotos vinculados a ela
CREATE FUNCTION dashboard_escuderia(constructor_Id INTEGER)
RETURNS TABLE (nome_escuderia VARCHAR, qtd_pilotos INTEGER) AS $$
BEGIN 
    RETURN QUERY 
    SELECT
        C.name AS Nome_Escuderia,
        COUNT(DISTINCT Q.driverId)::INTEGER AS qtd_pilotos 
    FROM
        CONSTRUCTORS C 
    JOIN 
        QUALIFYING Q 
    USING 
        constructorId 
    WHERE 
        C.constructorId = constructor_Id
    GROUP BY C.constructorref;
END; $$ LANGUAGE plpgsql;

--funcao para exibir as funcoes pedidas no dashboard do piloto.
--Precisamos listar o nome do piloto e o nome da escuderia
CREATE FUNCTION dashboard_piloto(driver_id INTEGER)
RETURNS TABLE (nomePiloto TEXT, nomeEscuderia VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT
        D.forename || ' ' || D.surname AS nomePiloto,
        C.name AS nomeEscuderia
    FROM 
        QUALIFYING
    JOIN 
        DRIVERS D 
    USING 
        (driverId)
    JOIN
        CONSTRUCTORS C
    USING 
        (constructorId)
    WHERE
        D.driverId = driver_id
    LIMIT 1;
END; 
$$ LANGUAGE plpgsql;

--Calcula total de pilotos, escuderias e temporadas na base
CREATE FUNCTION dashboard_admin_totais()
RETURNS TABLE (totalPilotos INTEGER, totalEscuderias INTEGER, totalTemp INTEGER) AS $$ 
BEGIN
    RETURN QUERY 
    SELECT 
        (SELECT COUNT(*) FROM DRIVERS) AS totalPilotos,
        (SELECT COUNT(*) FROM RACES) AS totalCorridas,
        (SELECT COUNT(*) FROM SEASON) AS totalTemp;
END;
$$ LANGUAGE plpgsql;

--
CREATE FUNCTION dashboard_admin_corridas(ano INTEGER)
RETURNS TABLE (nomeCorrida VARCHAR, voltasTotal INTEGER, tempoTotal INTERVAL) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT 
        R.name AS nomeCorrida,
        MAX(RS.laps) AS total_voltas,
        MAX(RS.time) AS tempoTotal 
    FROM 
        RACES R 
    JOIN 
        RESULTS RS 
    USING 
        (raceId)
    WHERE 
        R.year = ano
    GROUP BY 
        R.raceId, R.name 
    ORDER BY 
        R.name;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION dashboard_admin_escuderias(ano INTEGER)
RETURNS TABLE (nomeEscuderia VARCHAR, pontosTotal DOUBLE PRECISION) AS $$
BEGIN 
    RETURN QUERY 
    SELECT 
        C.name AS nomeEscuderia,
        SUM(Re.points) AS pontosTotal
    FROM 
        CONSTRUCTORS C 
    JOIN 
        RESULTS Re
    USING
        (constructorId)
    JOIN 
        RACES R 
    ON 
        Re.raceId = R.raceId
    WHERE
        R.year = ano 
    GROUP BY 
        C.name 
    ORDER BY 
        pontosTotal DESC;
END;
$$ LANGUAGE plpgsql; 


--OBS: Não existem corridas registradas em 2025. sendo assim, adicionamos a opcao
--do usuario especificar em qual ano deseja buscar
CREATE FUNCTION dashboard_admin_pilotos(ano INTEGER)
RETURNS TABLE (nomePiloto TEXT, pontosTotal INTEGER) AS $$
BEGIN
    RETURN QUERY 
    SELECT 
        D.forename || ' ' || D.surname AS nomePiloto,
        SUM(R.points)::INTEGER AS pontosTotal 
    FROM 
        DRIVERS D 
    JOIN 
        RESULTS R 
    USING 
        (driverId)
    JOIN 
        RACES Ra 
    USING 
        (raceId)
    WHERE 
        Ra.year = ano
    GROUP BY 
        D.forename, D.surname ;
END;
$$ LANGUAGE plpgsql;
