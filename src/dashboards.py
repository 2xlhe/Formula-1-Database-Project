from psycopg2.extensions import cursor
from utils import ScreenUtils


class AdminDashboard:
    def __init__(self, cursor: cursor):
        self.cursor = cursor

        self._ask_input()
        self._overview()
        self._race_summary()
        self._scuderia_summary()
        self._pilots_summary()

    def _ask_input(self) -> int:
        print("Ano para as pesquisas: ")
        return int(input().rstrip())

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


class ScuderiaDashboard:
    def __init__(self, cursor: cursor, constructorId: int):
        self.cursor = cursor
        self.constructorId = constructorId

        self._show_dashboard()

    def _show_dashboard(self):
        self.cursor.execute(
            "SELECT * FROM dashboard_escuderia(%s);", (self.constructorId,)
        )
        res = self.cursor.fetchone()

        print("__________Resumo da Escuderia:__________")
        if res:
            totalvit, totalpil, primeiroano, ultimoano = res
            print(f"Total de Vitórias da Escuderia: {totalvit}")
            print(f"Total de Pilotos que já correram pela Escuderia: {totalvit}")
            print(f"Primeiro ano da Escuderia: {primeiroano}")
            print(f"Último ano da Escuderia: {ultimoano}")
        else:
            print("Nenhuma informação encontrada para a escuderia informada.")


class PilotDashboard:
    def __init__(self, cursor: cursor, driverId: int):
        self.cursor = cursor
        self.driverId = driverId

        self._dashboard_piloto()

    def _dashboard_piloto(self):
        self.cursor.execute("SELECT * FROM dashboard_piloto_ano(%s);", (self.driverId,))
        primeiro, ultimo = cursor.fetchone()
        print(f"Primeiro Ano do Piloto: {primeiro}")
        print(f"Último Ano do Piloto: {ultimo}")
        
        for linha in cursor.fetchall():
            ano, circuito, pontos, vitorias, corridas = linha 
            print(f"Ano: {ano}")
            print(f"Circuito: {circuito}")
            print(f"Pontos: {pontos}")
            print(f"Vitorias: {vitorias}")
            print(f"Quantidade de Corridas: {corridas}")
            ScreenUtils.print_divisor()