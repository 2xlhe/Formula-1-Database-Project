import os
from psycopg2.extensions import cursor, connection
from typing import Optional
from utils import read_cli, print_divisor, ScreenUtils
from .relatories import AdminSummary, ScuderiaSummary, PilotSummary
from .dashboards import AdminDashboard, ScuderiaDashboard, PilotDashboard
from .operations import Register, Search


class AdminScreen:
    def __init__(self, username: str, cursor: cursor, conn: connection):
        self.username = username
        self.cursor = cursor
        self.conn = connection
        self.race_year: Optional[int] = None

    def _introduction(self) -> None:
        print(f"Bem-vindo, {self.username}!")
        print("Tela do Administrador do Sistema")
        while True:
            try:
                self.race_year = int(read_cli("Ano para as pesquisas: "))
                break
            except ValueError:
                print("Por favor, insira um ano válido.")

    def _summ_options(self):
        while True:
            print("Menu de Opções do Administrador")
            print("Selecione uma opção.")
            print("0: Cadastrar Escuderia")
            print("1: Cadastrar Piloto")
            print("2: Sair")

            summ = AdminSummary(self.cursor)

            match int(read_cli()):
                case 1:
                    ScreenUtils.clear()
                    summ.Summary1()
                case 2:
                    ScreenUtils.clear()
                    summ.Summary2()
                case 3:
                    ScreenUtils.clear()
                    summ.Summary3()
                case 4:
                    ScreenUtils.clear()
                    break

    def display(self) -> None:
        while True:
            print("Menu de Opções do Administrador")
            print("Selecione uma opção.")
            print("1: Visualizar Dashboard")
            print("2: Cadastrar Escuderia")
            print("3: Cadastrar Piloto")
            print("4: Visualizar Relatórios")
            print("5: Sair")

            reg = Register(self.cursor, self.conn)

            match int(read_cli()):
                case 1:
                    AdminDashboard(self.cursor)
                case 2:
                    reg.scuderia()
                case 3:
                    reg.pilot()
                case 4:
                    self._summ_options()
                case 5:
                    break


class ScuderiaScreen:
    def __init__(self, username: str, user_id: str, cursor: cursor, conn: connection):
        self.cursor = cursor
        self.conn = conn
        self.username = username
        self.user_id = user_id
        self.scuderia_id = None

    def _find_scuderia_pilots(self):
        self.cursor.execute(
            "SELECT idOriginal FROM USERS WHERE login =%s AND tipo='Escuderia'",
            (self.user_id,),
        )
        self.scuderia_id = cursor.fetchone()[0]

        self.cursor.execute(
            "SELECT * FROM dashboard_escuderia(%s)", (self.scuderia_id,)
        )

        fetch = self.cursor.fetchone()
        assert fetch is not None

        return fetch

    def display(self):
        try:
            escuderia, qtd = self._find_scuderia_pilots()
            print(f"Bem vindo, {self.username}!")
            print("Tela da Escuderia")
            print(f"Escuderia: {escuderia}")
            print(f"Quantidade de Pilotos da {escuderia}: {qtd}")
        except _ as _:
            print("ERRO: Escuderia não encontrada")

        print_divisor()

        while True:
            print("Menu de Opções da Escuderia")
            print("Selecione uma opção.")
            print("1: Visualizar Dashboard")
            print("2: Pesquisar piloto")
            print("3: Cadastrar Piloto (via arquivo)")
            print("4: Visualizar Relatórios")
            print("5: Sair")
            search = Search(self.cursor, self.conn)
            reg = Register(self.cursor, self.conn)

            match int(read_cli()):
                case 1:
                    ScuderiaDashboard(self.cursor, self.scuderia_id)
                    print_divisor()
                case 2:
                    search.pilot_by_forename(self.scuderia_id)
                    print_divisor()
                case 3:
                    reg.pilot_file()
                    print_divisor()
                case 4:
                    ScuderiaSummary(self.cursor, self.scuderia_id)
                    print_divisor()
                case 5:
                    ScreenUtils.clear()
                    break


class PilotScreen:
    def __init__(self, username: str, cursor: cursor):
        self.cursor = cursor
        self.username = username
        self.driverId = None

    def _get_pilot_scuderia(self):
        self.cursor.execute(
            "SELECT idOriginal FROM USERS WHERE login =%s AND tipo='Piloto'",
            (self.username,),
        )
        self.driverId = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT * FROM dashboard_piloto(%s)", (self.driverId,))

        fetch = self.cursor.fetchone()
        assert fetch is not None

        return fetch

    def _pilot_options(self):
        while True:
            print("Menu de Opções do Piloto")
            print("Selecione uma opção.")
            print("1: Visualizar Dashboard")
            print("2: Visualizar Relatórios")
            print("3: Sair")

            match int(read_cli()):
                case 1:
                    PilotDashboard(self.driverId)
                case 2:
                    PilotSummary(self.cursor, self.driverId)
                case 3:
                    ScreenUtils.clear()
                    break

    def display(self):
        try:
            name, scuderia = self._get_pilot_scuderia()
            print(f"Bem vindo, {self.username}!")
            print("Tela do Piloto")
            print(f"Piloto: {name}")
            print(f"Sua escuderia é: {scuderia}")
        except _ as _:
            print("ERRO: Piloto não encontrado")

        self._pilot_options()
