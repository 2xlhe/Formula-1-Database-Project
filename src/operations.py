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
    def __init__(
        self, cursor: cursor, conn: connection
    ):
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

    def cadastra_escuderia(self):
        try:
            self.cursor.execute(
                "SELECT COALESCE(MAX(constructorId), 0) + 1 FROM CONSTRUCTORS"
            )
            new_id = self.cursor.fetchone()[0]
            constructorref = read_cli("Constructor Reference:")
            name = read_cli("Constructor Name:")
            nationality = read_cli("Nacionalidade:")
            url = read_cli("URL:")

            self.cursor.execute(
                "INSERT INTO CONSTRUCTORS (constructorref, name, nationality, url) VALUES (%s, %s, %s, %s)",
                (constructorref, name, nationality, url),
            )
            self.conn.commit()
            print("Escuderia cadastrada com sucesso!")
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao cadastrar escuderia: {e}")

    def cadastra_piloto():
        return
