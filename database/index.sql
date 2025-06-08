--Indices usados para agilizar o relatorio 4
DROP INDEX indice_results_constructor;
CREATE INDEX indice_results_constructor ON RESULTS(constructorId);

DROP INDEX indice_drivers_names;
CREATE INDEX indice_drivers_names ON DRIVERS(forename, surname);

--Indices usados para agilizar o relatorio 6
DROP INDEX IF EXISTS indice_race_year;
CREATE INDEX indice_race_year ON races(raceid, year);

DROP INDEX IF EXISTS indice_results_driver;
CREATE INDEX IF NOT EXISTS indice_results_driver ON results(driverid);
