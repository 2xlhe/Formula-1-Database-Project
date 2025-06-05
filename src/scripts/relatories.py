from .utils import read_cli, print_divisor
from .display import ScreenUtils
from psycopg2.extensions import cursor


def wait_for_exit():
    opt = 1
    while opt != 0:
        opt = int(input("Digite 0 para sair:"))
    ScreenUtils.clear()



def wait_for_exit(self):
    opt = 1
    while opt != 0:
        opt = int(read_cli("Digite 0 para sair:"))
    ScreenUtils.clear()


class AdminSummary:
    def __init__(self, cursor: cursor):
        self.cursor = cursor

    def Summary1(self):
        """
        Summary1 is queries for all the pilot occurrences that happened during races
        print: ocurrences_status, sum(occurence)
        """
        self.cursor.execute("SELECT * FROM vw_relatorio_status;")

        print("Relatório 1: Ocorrências por Tipo de Status em Corridas\n")
        for status, qtd in cursor.fetchall():
            print(f"{status}: {qtd} ocorrências")

        wait_for_exit()
        print_divisor

    def Summary2(self):
        """
        Summary2 is responsible to do a query looking after all airports in a 100km range from an inputed city
        print: city_name, airport_code, airport_name, airport_city, airport_distance
        """
        city = read_cli("Insira o nome de uma cidade brasileira:")
        self.cursor.execute("SELECT * FROM relatorio_aeroportos(%s);", (city,))
        relatorio = cursor.fetchall()

        print(f"Relatório 2: Aeroportos próximos da cidade {city}\n")

        for cidade, iata, aeroporto, cidade_aeroporto, distancia, tipo in relatorio:
            print(f"Cidade: {cidade}")
            print(f"Código IATA do Aeroporto: {iata}")
            print(f"Nome do Aeroporto: {aeroporto}")
            print(f"Cidade do Aeroporto: {cidade_aeroporto}")
            print(f"Distância em KM: {distancia}")
            print_divisor()

        wait_for_exit()

    def Summary3(self):
        """
        Summary3 contains multiple queries called subSummaries which will calculate the total values described below
        print: multiple
        """

        print(f"Relatório 3: Escuderias e Corridas\n")

        def _list_scuderias_total_pilots():
            # Lista todas as escuderias e quantidade de pilotos em cada uma
            self.cursor.execute("SELECT * FROM relatorio_escuderias_pilotos;")
            print("Escuderias e Quantidade de Pilotos:\n")

            for nome, qtd in self.cursor.fetchall():
                print(f"Escuderia {nome}: {qtd} pilotos registrados.")
            print_divisor()

        def _total_races():
            # Nivel 1: Qtd de corridas cadastradas no total
            self.cursor.execute("SELECT * FROM relatorio_qtd_corridas;")
            qtd_corridas = self.fetchone()[0]
            print(f"Quantidade de Corridas Cadastradas: {qtd_corridas}")
            print_divisor()

        def _total_races_per_circuit():
            # Nivel 2: Quantidade de corridas cadastradas por circuito
            self.cursor.execute("SELECT * FROM relatorio_corridas_circuito;")

            for nome, total, min, max, avg in self.cursor.fetchall():
                print(f"Circuito: {nome}")
                print(f"Total de Corridas: {total}")
                print(f"Mínimo de Voltas: {min}")
                print(f"Máximo de Voltas: {max}")
                print(f"Número médio de Voltas: {avg}")
                print_divisor

        def _laps_and_time_per_circuit():
            # Nivel 3
            self.cursor.execute("SELECT * FROM relatorio_corrida_circuito_tempo;")

            print(f"Quantidade de voltas e tempo por corrida, em cada circuito")
            for circuito, corrida, ano, laps, tempo in cursor.fetchall():
                print(f"Circuito: {circuito}")
                print(f"Corrida: {corrida}")
                print(f"Ano: {ano}")
                print(f"Voltas: {laps}")
                print(f"Tempo: {tempo}")
                print_divisor()

            wait_for_exit()

        _list_scuderias_total_pilots()
        print_divisor()

        _total_races()
        print_divisor()

        _total_races_per_circuit()
        print_divisor()

        _laps_and_time_per_circuit()
        print_divisor()


class ScuderiaSummary:
    def __init__(self, cursor: cursor, scuderia_id):
        self.cursor = cursor
        self.scuderia_id = scuderia_id

    def show_menu(self):
        while True:
            print("______Página de Relatórios da Escuderia______")
            print("Selecione o tipo de relatório:")
            print("1: Relatório de Pilotos e Vitórias")
            print("2: Relatório de Resultados por Status")
            print("3: Sair da página de relatórios")
            opt = int(input().rstrip())

            if opt == 1:
                self.tela.limpa_tela()
                self.relatorio4(self.scuderia_id)
            elif opt == 2:
                self.tela.limpa_tela()
                self.relatorio5(self.scuderia_id)
            elif opt == 3:
                self.tela.limpa_tela()
                break

    def summary4(self):
        print(f"Relatório 4: Pilotos e Vitórias")
        self.tela.pula_linha()

        self.cursor.execute("SELECT * FROM relatorio_vitorias_pilotos(%s);", (self.scuderia_id,))
        vitorias_pilotos = self.cursor.fetchall()
        for nome, qtd in vitorias_pilotos:
            print(f"Piloto {nome}: {qtd} vitórias")
        self.tela.pula_linha()

        self.wait_for_exit()

    def summary5(self):
        print(f"Relatório 5: Status e Resultados")
        self.tela.pula_linha()

        self.cursor.execute("SELECT * FROM relatorio_resultado_status(%s);", (self.scuderia_id,))
        results_status = self.cursor.fetchall()
        for status, qtd in results_status:
            print(f"Status {status}: Quantidade {qtd}")
        self.tela.pula_linha()

        self.wait_for_exit()


class PilotSummary:
    def __init__(self, cursor: cursor, driver_id):
        self.cursor = cursor
        self.driver_id = driver_id
        self.tela = ScreenUtils

    def show_menu(self):
        while True:
            print("______Página de Relatórios do Piloto______")
            print("Selecione o tipo de relatório:")
            print("1: Total de Pontos obtidos por ano")
            print("2: Quantidade de resultados por status")
            print("3: Sair da página de relatórios")
            
            opt = int(read_cli())
            if opt == 1:
                self.tela.clear()
                self.summary6()
            elif opt == 2:
                self.tela.clear()
                self.summary7()
            elif opt == 3:
                self.tela.clear()
                break

    def summary6(self):
        print(f"Relatório 6: Pontuação obtida por ano\n")

        self.cursor.execute("SELECT * FROM relatorio_pontos_por_ano(%s)n", (self.driver_id,))
        pontos = self.cursor.fetchall()
        curr_ano = None
        for ano, corrida, ptos in pontos:
            if ano != curr_ano:
                if curr_ano is not None:
                    print()
                print(f"Ano: {ano}")
                curr_ano = ano
            print(f"Corrida: {corrida}, Pontuação: {ptos}")

        self.tela.newline()
        wait_for_exit()

    def summary7(self):
        print(f"Relatório 7: Quantidade de resultados por cada Status\n")

        self.cursor.execute("SELECT * FROM relatorio_status_piloto(%s);", (self.driver_id,))
        status_res = self.cursor.fetchall()
        for status, qtd in status_res:
            print(f"Status {status}: Quantidade {qtd}")
        ScreenUtils.print_divisor()

        wait_for_exit()
