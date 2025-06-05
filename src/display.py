import os
from psycopg2.extensions import cursor
from typing import Optional
from utils import read_cli


# TODO Add limpa_tela and pula_linhas in the printing stuff
class ScreenUtils:
    def clear():
        os.system("clear")

    def pula_linha():
        print("________________________________")
        print("\n\n\n")

    @staticmethod
    def welcome():
        print("___*** Projeto Final de Laboratório de Bases de Dados ***___\n\n")
        print("____________Sistema de Gerenciamento da Formula1____________\n\n")
        print("Login")
        print("--------------")


class AdminScreen:
    def __init__(self, username: str, cursor: cursor):
        self.username = username
        self.cursor = cursor
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

    def _overview(self) -> None:
        self.cursor.execute("SELECT * FROM dashboard_admin_totais()")
        totalP, totalE, totalT = self.cursor.fetchone()
        print("\n__________Visão geral:__________")
        print(f"Total de pilotos registrados: {totalP}")
        print(f"Total de escuderias registradas: {totalE}")
        print(f"Total de temporadas registradas: {totalT}\n")

    def _race_summary(self) -> None:
        print("__________Resumo das corridas:__________")
        self.cursor.execute(
            "SELECT * FROM dashboard_admin_corridas(%s)", (self.race_year,)
        )
        rows = self.cursor.fetchall()
        if not rows:
            print("Nenhuma corrida encontrada para o ano informado.")
        for nome, voltas, tempo in rows:
            print(f"{nome}: {voltas} voltas, tempo total: {tempo}")

    def _scuderia_summary(self) -> None:
        print("__________Resumo das Escuderias:__________")
        self.cursor.execute(
            "SELECT * FROM dashboard_admin_escuderias(%s)", (self.race_year,)
        )
        rows = self.cursor.fetchall()
        if not rows:
            print("Nenhuma escuderia encontrada para o ano informado.")
        for nome, pontos in rows:
            print(f"{nome}: Pontuação {pontos}")

    def _pilots_summary(self) -> None:
        print("__________Resumo dos pilotos:__________")
        self.cursor.execute(
            "SELECT * FROM dashboard_admin_pilotos(%s)", (self.race_year,)
        )
        rows = self.cursor.fetchall()
        if not rows:
            print("Nenhum piloto encontrado para o ano informado.")
        for piloto, pontuacao in rows:
            print(f"{piloto}: {pontuacao} pontos.")

    def _admin_options(self):
        while opt != 2:
            print("Menu de Opções do Administrador")
            print("Selecione uma opção.")
            print("0: Cadastrar Escuderia")
            print("1: Cadastrar Piloto")
            print("2: Sair")
            opt = int(read_cli())

            match opt:
                case 0:
                    ...
                case 1:
                    ...
                case 2:
                    break

    def display(self) -> None:
        self._introduction()
        self._overview()
        self._race_summary()
        self._scuderia_summary()
        self._pilots_summary()
        self._admin_options()


class ScuderiaScreen:
    def __init__(self, username: str, user_id: str, cursor: cursor):
        self.cursor = cursor
        self.username = username
        self.user_id = user_id

    def _find_scuderia_pilots(self):
        self.cursor.execute(
            "SELECT idOriginal FROM USERS WHERE login =%s AND tipo='Escuderia'",
            (self.user_id,),
        )
        self.cursor.execute(
            "SELECT * FROM dashboard_escuderia(%s)", (self.cursor.fetchone()[0],)
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


class PilotScreen:
    def __init__(self, username: str, cursor: cursor):
        self.cursor = cursor
        self.username = username

    def _get_pilot_scuderia(self):
        self.cursor.execute(
            "SELECT idOriginal FROM USERS WHERE login =%s AND tipo='Piloto'",
            (self.username,),
        )
        driverId = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT * FROM dashboard_piloto(%s)", (driverId,))

        fetch = self.cursor.fetchone()
        assert fetch is not None

        return fetch

    def display(self):
        try:
            name, scuderia = self._get_pilot_scuderia()
            print(f"Bem vindo, {self.username}!")
            print("Tela do Piloto")
            print(f"Piloto: {name}")
            print(f"Sua escuderia é: {scuderia}")
        except _ as _:
            print("ERRO: Piloto não encontrado")
