# Formula 1 database CLI manager

This project retrieves a Formula 1 dataset (http://ergast.com/mrd/).

# How to run
1. Copy the repository into the local machine

2. Create a postgres instance

3. Load the database (./database) into postgres

4. Create a config.yaml with the following parameters form your postgres instance:

```
host: localhost
port: 5432
dbname: postgres
user: postgres
password: yourpassword
```

5. Go to the root folder and run:
```
uv sync
```

6. Run the cli program
```
uv run src/scripts/main.py --config config.yaml
```