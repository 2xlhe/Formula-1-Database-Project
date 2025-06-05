--Visão do relatório 1
CREATE VIEW vw_relatorio_status AS 
SELECT 
    S.status AS Tipo_Status, 
    COUNT(*) AS Total_Ocorrencias
FROM 
    RESULTS R 
JOIN 
    STATUS S 
ON 
    R.statusId = S.statusId 
GROUP BY 
    S.status 
ORDER BY 
    Total_Ocorrencias DESC;

--VIEWS USADAS PARA O RELATORIO 3
DROP VIEW IF EXISTS relatorio_escuderias_pilotos;
CREATE VIEW relatorio_escuderias_pilotos AS 
SELECT 
    C.name AS Nome_Escuderia,
    COUNT(DISTINCT R.driverId) AS Quantidade_Pilotos
FROM
    CONSTRUCTORS C 
LEFT JOIN
    RESULTS R 
ON
    C.constructorId = R.constructorId 
GROUP BY 
    C.constructorId, C.name
ORDER BY 
    Quantidade_Pilotos DESC;

DROP VIEW IF EXISTS relatorio_qtd_corridas;
CREATE VIEW relatorio_qtd_corridas AS 
SELECT 
    COUNT(*) as TotalCorridas
FROM RACES;

DROP VIEW IF EXISTS relatorio_corridas_circuito;
CREATE VIEW relatorio_corridas_circuito AS 
SELECT 
    C.name AS nomeCircuito,
    COUNT(R.raceId) AS totalCorridas,
    MIN(RES.laps) AS minVoltas,
    MAX(RES.laps) AS maxVoltas,
    ROUND(AVG(RES.laps)::NUMERIC,2) AS mediaVoltas
FROM 
    CIRCUITS C 
JOIN 
    RACES R 
ON 
    C.circuitId = R.circuitId
JOIN
    RESULTS RES 
ON 
    RES.raceId = R.raceId 
GROUP BY 
    C.name
ORDER BY 
    totalCorridas DESC;

DROP VIEW IF EXISTS relatorio_corrida_circuito_tempo;
CREATE VIEW relatorio_corrida_circuito_tempo AS 
SELECT 
    C.name AS Circuito,
    R.name as Corrida,
    R.year,
    RES.laps,
    COALESCE(SUM(RES.milliseconds), 0) AS tempoTotal
FROM 
    RACES R 
JOIN 
    CIRCUITS C 
ON 
    C.circuitId = R.raceId 
JOIN 
    RESULTS RES 
ON 
    R.raceId = RES.raceId 
GROUP BY 
    C.name, R.name, R.year, RES.laps 
ORDER BY 
    C.name, R.year;