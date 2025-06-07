--funcao para exibir as funcoes pedidas na pagina da escuderia.
--Precisamos listar o nome da escuderia (a partir do id) e a quantidade
--de pilotos vinculados a ela
CREATE FUNCTION info_escuderia(constructor_id INTEGER)
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
    ON 
        C.constructorid = Q.constructorid
    WHERE 
        C.constructorid = constructor_id
    GROUP BY C.name;
END; $$ LANGUAGE plpgsql;

--funcao para exibir as funcoes pedidas na pagina do piloto.
--Precisamos listar o nome do piloto e o nome da escuderia
CREATE FUNCTION info_piloto(driver_id INTEGER)
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

--Funcao para consultar piloto via forename.
CREATE OR REPLACE FUNCTION consulta_piloto_forename(forename VARCHAR, escuderia_id INTEGER)
RETURNS TABLE (nome_completo VARCHAR, data_nascimento DATE, nacionalidade VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        d.forename || ' ' || d.surname AS nome_completo,
        d.dateOfBirth AS data_nascimento,
        d.nationality AS nacionalidade
    FROM 
        drivers d
    JOIN 
        results r 
    ON 
        d.driverid = r.driverid
    WHERE 
        d.forename ILIKE forename_input
        AND c.constructorid = escuderia_id;
END;
$$ LANGUAGE plpgsql;

--Funcao responsavel por exibir os dados de Dashboard da Escuderia
CREATE OR REPLACE FUNCTION dashboard_escuderia(constructor_id INTEGER) 
RETURNS TABLE (
    totalVitorias INTEGER,
    totalPilotos INTEGER,
    primeiroAno INTEGER,
    ultimoAno INTEGER
) AS $$
BEGIN
    RETURN QUERY 
    SELECT 
        COUNT(*) FILTER (WHERE R.position=1)::INTEGER AS totalVitorias,
        COUNT(DISTINCT R.driverId)::INTEGER AS totalPilotos,
        MIN(RAC.year)::INTEGER AS primeiroAno,
        MAX(RAC.year)::INTEGER AS ultimoAno 
    FROM 
        RESULTS R 
    JOIN 
        RACES RAC 
    ON 
        R.raceId = RAC.raceId
    WHERE 
        R.constructorId = constructor_id;
END;
$$ LANGUAGE plpgsql;

--Funcao responsavel por exibir os dados de Dashboard do Piloto (primeiro e ultimo ano)
CREATE OR REPLACE FUNCTION dashboard_piloto_ano(driver_id INTEGER)
RETURNS TABLE (
    primeiroAno INTEGER,
    ultimoAno INTEGER
) AS $$
BEGIN 
    RETURN QUERY
    SELECT 
        MIN(RAC.year)::INTEGER AS primeiroAno,
        MAX(RAC.year)::INTEGER AS ultimoAno 
    FROM 
        RESULTS R 
    JOIN
        RACES RAC 
    USING 
        (raceId)
    WHERE 
        R.driverId = driver_id; 
END;
$$ LANGUAGE plpgsql;

--ARRUMAR ISSO AQUI. D
DROP FUNCTION IF EXISTS dashboard_piloto_vitorias(INTEGER); 
CREATE OR REPLACE FUNCTION dashboard_piloto_vitorias(driver_id INTEGER)
RETURNS TABLE (
    ano INTEGER,
    nomeCircuito VARCHAR,
    pontos DOUBLE PRECISION,
    qtdVitorias INTEGER,
    qtdCorridas INTEGER
) AS $$
BEGIN 
    RETURN QUERY
    SELECT
        RA.year AS ano,
        C.name AS nomeCircuito,
        SUM(R.points) AS pontos,
        COUNT(*) FILTER (WHERE R.position=1)::INTEGER AS qtdVitorias,
        COUNT(*)::INTEGER AS qtdCorridas
    FROM
        RESULTS R 
    JOIN
        RACES RA 
    USING 
        (raceId)
    JOIN 
        CIRCUITS C 
    ON 
        C.circuitId = RA.circuitId
    WHERE 
        R.driverId = driver_id
    GROUP BY 
        RA.year, C.name
    ORDER BY 
        RA.year, C.name;
END;
$$ LANGUAGE plpgsql;


--Relatorio 2
CREATE EXTENSION IF NOT EXISTS cube;
CREATE EXTENSION IF NOT EXISTS earthdistance;

DROP FUNCTION IF EXISTS relatorio_aeroportos(TEXT);
CREATE FUNCTION relatorio_aeroportos(cidade TEXT)
RETURNS TABLE (
    nomeCidade VARCHAR,
    codigoIata VARCHAR,
    nomeAeroporto VARCHAR,
    cidadeAeroporto VARCHAR,
    distancia NUMERIC,
    tipoAeroporto VARCHAR
) AS $$ 
BEGIN 
    RETURN QUERY 
    SELECT 
        C.name AS nomeCidade,
        A.iataCode AS codigoIata, 
        A.name AS nomeAeroporto,
        A.city AS cidadeAeroporto,
        ROUND((earth_distance(
            ll_to_earth(C.lat, C.long),
            ll_to_earth(A.latdeg, A.longdeg)
        ) / 1000)::NUMERIC, 2) AS distancia,
        A.type AS tipoAeroporto
    FROM 
        GEOCITIES15K C
    JOIN
        AIRPORTS A 
    ON 
        A.isoCountry = 'BR'
        AND A.type IN ('medium_airport', 'large_airport')
    WHERE 
        C.name ILIKE cidade
        AND earth_distance(
            ll_to_earth(C.lat, C.long),
            ll_to_earth(A.latdeg, A.longdeg)) <= 100000;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS relatorio_vitorias_pilotos(INTEGER);
CREATE OR REPLACE FUNCTION relatorio_vitorias_pilotos(constructor_id INTEGER)
RETURNS TABLE (
    driver TEXT,
    qtdVitorias INTEGER
) AS $$ 
BEGIN 
    RETURN QUERY
    SELECT
        D.forename || ' ' || D.surname AS driver,
        COUNT(*) FILTER (WHERE R.position=1)::INTEGER AS qtdVitorias
    FROM 
        RESULTS R 
    JOIN
        DRIVERS D 
    ON 
        D.driverId = R.driverId
    WHERE
        R.constructorId = constructor_id
    GROUP BY 
        D.forename, D.surname
    ORDER BY qtdVitorias DESC, driver;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS relatorio_resultado_status(INTEGER);
CREATE OR REPLACE FUNCTION relatorio_resultado_status(constructor_id INTEGER)
RETURNS TABLE (
    status VARCHAR,
    qtd INTEGER
) AS $$ 
BEGIN
    RETURN QUERY
    SELECT
        S.status,
        COUNT(*)::INTEGER AS qtd
    FROM
        RESULTS R 
    JOIN
        STATUS S 
    ON 
        S.statusId = R.statusId
    WHERE
        R.constructorId = constructor_id
    GROUP BY 
        S.status
    ORDER BY 
        qtd DESC;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS relatorio_pontos_por_ano(INTEGER);
CREATE OR REPLACE FUNCTION relatorio_pontos_por_ano(driver_id INTEGER)
RETURNS TABLE (
    ano INTEGER,
    corrida VARCHAR,
    pontos FLOAT
) AS $$ 
BEGIN
    RETURN QUERY
    SELECT
        R.year,
        R.name AS corrida,
        RS.points
    FROM 
        RACES R 
    JOIN
        RESULTS RS 
    ON 
        R.raceId = RS.raceId
    WHERE
        RS.driverId = driver_id
    ORDER BY 
        R.year, R.name;
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS relatorio_status_piloto(INTEGER);
CREATE FUNCTION relatorio_status_piloto(driver_id INTEGER)
RETURNS TABLE (
    status VARCHAR,
    qtd INTEGER
) AS $$ 
BEGIN
    RETURN QUERY
    SELECT
        S.status,
        COUNT(*)::INTEGER AS qtd
    FROM
        RESULTS R 
    JOIN
        STATUS S 
    ON 
        S.statusId = R.statusId
    WHERE 
        R.driverId = driver_id 
    GROUP BY 
        S.status
    ORDER BY 
        qtd DESC;
END;
$$ LANGUAGE plpgsql;
