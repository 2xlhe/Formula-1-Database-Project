from psycopg2 import sql, connect
from psycopg2.extensions import cursor, connection
import hashlib
from typing import Optional, Tuple
from utils import read_cli
from contextlib import contextmanager


@contextmanager
def connect_db():
    conn = None
    cur = None
    try:
        conn = connect(
            host="localhost",
            port="5432",
            dbname="fia",
            user="postgres",
            password="postgres",
        )
        cur = conn.cursor()
        yield conn, cur
    except Exception as e:
        raise Exception(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


class Login:
    def __init__(self, cursor: cursor, conn: connection):
        self.cursor = cursor
        self.conn = conn

    def _hash_password(self, passwd: str) -> str:
        return hashlib.sha256(passwd.encode("utf-8")).hexdigest()

    def _log_user(self, user_id: int):
        try:
            self.cursor.execute(
                sql.SQL("INSERT INTO USERS_LOG (userId) VALUES (%s)"), (user_id,)
            )
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao registrar log do usuário: {e}")

    def login(self, username: str, password: Optional[str]) -> Tuple[str, str | None]:
        try:
            self.cursor.execute(
                sql.SQL("SELECT userid, tipo, password FROM USERS WHERE login=%s"),
                (username,),
            )
            res = self.cursor.fetchone()
            if res:
                user_id, account_type, expected_password = res
                if expected_password == password:
                    print("Login realizado com sucesso!")
                    self._log_user(user_id)
                    return account_type, user_id
                else:
                    print("Senha incorreta! Tente novamente.")
            else:
                print("Usuário não registrado! Tente novamente.\n\n\n\n\n\n")
        except Exception as e:
            print(f"Erro ao realizar login: {e}")
        return None, None


class Register:
    def __init__(self, cursor: cursor, conn: connection):
        self.cursor = cursor
        self.conn = conn

    def scuderia(self):
        constructorref = read_cli("Constructor Reference:")
        name = read_cli("Constructor Name:")
        nationality = read_cli("Nacionalidade:")
        url = read_cli("URL:")

        try:
            # Garante que não haja inconsistência com as chaves primarias de constructor.
            # Mesmo com constructorId definido com SERIAL, o problema persistiu.
            self.cursor.execute(
                """
                SELECT setval(
                    pg_get_serial_sequence('constructors', 'constructorid'),
                    COALESCE((SELECT MAX(constructorid) FROM constructors), 0)
                )
            """
            )

            # Faz a inserção de um construtor a partir dos dados fornecidos pelo usuario
            self.cursor.execute(
                "INSERT INTO CONSTRUCTORS (constructorref, name, nationality, url) VALUES (%s, %s, %s, %s)",
                (constructorref, name, nationality, url),
            )

            self.conn.commit()
            print("Escuderia cadastrada com sucesso!")
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao cadastrar escuderia: {e}")

    def pilot(self):
        driverref = read_cli("Driver Reference:")
        number = int(read_cli("Driver Number:"))
        code = read_cli("Driver Code:")
        forename = read_cli("Driver Forename:")
        surname = read_cli("Driver Surname:")
        date = read_cli("Date of Birth:")
        nationality = read_cli("Nationality:")

        try:
            # Garante que não haja inconsistência com as chaves primarias de constructor.
            # Mesmo com constructorId definido com SERIAL, o problema persistiu.
            self.cursor.execute(
                """
            SELECT setval(
                pg_get_serial_sequence('drivers', 'driverid'),
                COALESCE((SELECT MAX(driverid) FROM drivers), 0)
            )
            """
            )

            # Faz a inserção de um piloto
            self.cursor.execute(
                """INSERT INTO DRIVERS (driverref, number, code, 
                forename, surname, dateOfBirth, nationality) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (driverref, number, code, forename, surname, date, nationality),
            )
            self.conn.commit()
            print("Piloto cadastrado com sucesso!")
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao cadastrar piloto: {e}")

    def pilot_file(self):
        filename = read_cli("Insira o caminho do arquivo:")
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("Arquivo não encontrado")
            return

        try:
            # Garante que não haja inconsistência com as chaves primarias de driver.
            self.cursor.execute("""
            SELECT setval(
                pg_get_serial_sequence('drivers', 'driverid'),
                COALESCE((SELECT MAX(driverid) FROM drivers), 0)
            )
            """)

            pilots_to_insert = []
            for line in lines:
                data = line.strip().split(',')

                if len(data) < 6:
                    print(f"Linha inválida ignorada: {line.strip()}")
                    continue

                driverref = data[0]
                code = data[1]
                forename = data[2]
                surname = data[3]
                dateOfBirth = data[4]
                nationality = data[5]
                number = data[6] if len(data) > 6 and data[6] != '' else None
                url = data[7] if len(data) > 7 and data[7] != '' else None

                self.cursor.execute(
                    "SELECT 1 FROM DRIVERS WHERE FORENAME=%s AND surname=%s",
                    (forename, surname)
                )
                if self.cursor.fetchone():
                    print(f"O piloto {forename} {surname} já foi registrado. Inserção abortada.")
                    continue

                pilots_to_insert.append(
                    (driverref, number, code, forename, surname, dateOfBirth, nationality, url)
                )

            if pilots_to_insert:
                self.cursor.executemany(
                    """INSERT INTO DRIVERS (driverref, number, code, forename, surname,
                    dateOfBirth, nationality, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    pilots_to_insert
                )
                self.conn.commit()
                print("Piloto(s) inseridos com sucesso.")
            else:
                print("Nenhum piloto novo para inserir.")
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao cadastrar piloto(s): {e}")


class Search:
    def __init__(self, cursor: cursor, conn: connection):
        self.cursor = cursor
        self.conn = conn

    def pilot_by_forename(self, scuderia_id: int):
        forename = read_cli("Insira o Forename do piloto:")

        try:
            self.cursor.execute(
                "SELECT * FROM consulta_piloto_forename(%s, %s)",
                (forename, scuderia_id),
            )
            results = self.cursor.fetchall()

            if results:
                print(f"{len(results)} pilotos encontrados:\n")
                for driver in results:
                    print(
                        f"Nome: {driver[0]}, Nascimento: {driver[1]}, Nacionalidade: {driver[2]}"
                    )
            else:
                print("Nenhum piloto encontrado com esse nome para a sua escuderia.")
        except Exception as e:
            print(f"Erro ao buscar piloto: {e}")
