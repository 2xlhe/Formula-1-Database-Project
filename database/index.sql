DROP INDEX indice_results_constructor;
CREATE INDEX indice_results_constructor ON RESULTS(constructorId);

DROP INDEX indice_drivers_names;
CREATE INDEX indice_drivers_names ON DRIVERS(forename, surname);

