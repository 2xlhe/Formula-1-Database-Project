import hashlib
import psycopg2
from psycopg2 import sql
import getpass
import os
import tela
import conection

#Função que define a tela quando o usuário faz login como admin
def tela_admin(nome_usuario):
    tela.print_cabecalho("Tela do Administrador")
    print(f"Bem vindo, {nome_usuario}!")
    
    while(True):
        print("Menu de Opções do Administrador")
        print("Selecione uma opção.")
        print("1: Visualizar Dashboard")
        print("2: Cadastrar Escuderia")
        print("3: Cadastrar Piloto")
        print("4: Visualizar Relatórios")
        print("5: Sair")
        opt = int(input().rstrip())
        tela.limpa_tela()

        match opt:
            case 1:
                dashboard_admin()
            case 2:
                cadastra_escuderia()
            case 3:
                cadastra_piloto()
            case 4:
                relatorios_admin()
            case 5:
                break

def dashboard_admin():
    conn, cursor = conection.conecta_banco()

    tela.pula_linha()
    print("Ano para as pesquisas: ")
    ano_pesquisa = int(input().rstrip())
    
    #Lista total de pilotos, escuderias e temporas
    print("__________Visão geral:__________")
    cursor.execute("SELECT * FROM dashboard_admin_totais()")
    totalP, totalE, totalT = cursor.fetchone()
    print(f"Total de pilotos registrados: {totalP}")
    print(f"Total de escuderias registradas: {totalE}")
    print(f"Total de temporadas registradas: {totalT}")
    tela.pula_linha()

    #Lista de todas as corridas no ano, total de voltas e tempo
    print("__________Resumo das corridas:__________")
    cursor.execute("SELECT * FROM dashboard_admin_corridas(%s)", (ano_pesquisa,))
    for nome, voltas, tempo in cursor.fetchall():
        print(f"{nome}: {voltas} voltas, tempo total: {tempo}")
    tela.pula_linha()

    #Lista de todas as escuderias no ano e pontuacao total
    print("__________Resumo das Escuderias:__________")
    cursor.execute("SELECT * FROM dashboard_admin_escuderias(%s)", (ano_pesquisa,))
    for nome, pontos in cursor.fetchall():
        print(f"{nome}: Pontuação {pontos}")
    tela.pula_linha()


    #Lista todos os pilotos no ano corrente e pontuacao
    print("__________Resumo dos pilotos:__________")
    cursor.execute("SELECT * FROM dashboard_admin_pilotos(%s)", (ano_pesquisa,))
    for piloto, pontuacao in cursor.fetchall():
        print(f"{piloto}: {pontuacao} pontos.")
    tela.pula_linha()

    cursor.close()
    conn.close()

def cadastra_escuderia():
    constructorref = input("Constructor Reference:").rstrip()
    name = input("Constructor Name:").rstrip()
    nationality = input("Nacionalidade:").rstrip()
    url = input("URL:").rstrip()

    conn, cursor = conection.conecta_banco()

    #Garante que não haja inconsistência com as chaves primarias de constructor.
    #Mesmo com constructorId definido com SERIAL, o problema persistiu.
    cursor.execute("""
        SELECT setval(
            pg_get_serial_sequence('constructors', 'constructorid'),
            COALESCE((SELECT MAX(constructorid) FROM constructors), 0)
        )
    """)

    #Faz a inserção de um construtor a partir dos dados fornecidos pelo usuario
    cursor.execute("INSERT INTO CONSTRUCTORS (constructorref, name, nationality, url) VALUES (%s, %s, %s, %s)", 
                                    (constructorref, name, nationality, url))
    conn.commit()

    cursor.close()
    conn.close()


#Cadastra piloto na base
def cadastra_piloto():
    driverref = input('Driver Reference:').rstrip()
    number = int(input('Driver Number:').rstrip())
    code = input('Driver Code:').rstrip()
    forename = input('Driver Forename:').rstrip()
    surname = input('Driver Surname:').rstrip()
    date = input('Date of Birth:').rstrip()
    nationality = input('Nationality:').rstrip()
    conn, cursor = conection.conecta_banco()

    #Garante que não haja inconsistência com as chaves primarias de constructor.
    #Mesmo com constructorId definido com SERIAL, o problema persistiu.
    cursor.execute("""
        SELECT setval(
            pg_get_serial_sequence('drivers', 'driverid'),
            COALESCE((SELECT MAX(driverid) FROM drivers), 0)
        )
    """)

    #Faz a inserção de um piloto
    cursor.execute("""INSERT INTO DRIVERS (driverref, number, code, 
                   forename, surname, dateOfBirth, nationality) VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
                                    (driverref, number, code, forename, surname, date, nationality))
    conn.commit()

    cursor.close()
    conn.close()
    

def relatorios_admin():
    while(True):
        print("______Página de Relatórios do Administrador______")
        print("Selecione o tipo de relatório:")
        print("1: Relatório de Status")
        print("2: Relatório de Cidade/Aeroporto")
        print("3: Relatório de Escuderias e Corridas")
        print("4: Sair da página de relatórios")
        opt = int(input().rstrip())

        match opt:
            case 1:
                tela.limpa_tela()
                relatorio1()
            case 2:
                tela.limpa_tela()
                relatorio2()
            case 3:
                tela.limpa_tela()
                relatorio3()
            case 4:
                tela.limpa_tela()
                break


def relatorio1():
    conn, cursor = conection.conecta_banco()
    cursor.execute("SELECT * FROM vw_relatorio_status;")
    relatorio = cursor.fetchall()

    print("Relatório 1: Ocorrências por Tipo de Status em Corridas")
    for status, qtd in relatorio:
        print(f"{status}: {qtd} ocorrências")
    
    cursor.close()
    conn.close()
    
    opt=1
    while(opt!=0):
        opt = int(input("Digite 0 para sair:"))
    tela.limpa_tela()

def relatorio2():
    conn, cursor = conection.conecta_banco()

    cidade = input("Insira o nome de uma cidade brasileira:").rstrip()
    cursor.execute("SELECT * FROM relatorio_aeroportos(%s);", (cidade,))
    relatorio = cursor.fetchall()

    print(f"Relatório 2: Aeroportos próximos da cidade {cidade}")
    tela.pula_linha()

    for cidade, iata, aeroporto, cidade_aeroporto, distancia, tipo in relatorio:
        print(f"Cidade: {cidade}")
        print(f"Código IATA do Aeroporto: {iata}")
        print(f"Nome do Aeroporto: {aeroporto}")
        print(f"Cidade do Aeroporto: {cidade_aeroporto}")
        print(f"Distância em KM: {distancia}")
        tela.pula_linha()
    
    cursor.close()
    conn.close()
    
    opt=1
    while(opt!=0):
        opt = int(input("Digite 0 para sair:"))
    tela.limpa_tela()


def relatorio3():
    conn, cursor = conection.conecta_banco()

    print(f"Relatório 3: Escuderias e Corridas")
    tela.pula_linha()

    #Lista todas as escuderias e quantidade de pilotos em cada uma
    cursor.execute("SELECT * FROM relatorio_escuderias_pilotos;")
    relatorio_pilotos = cursor.fetchall()
    print("Escuderias e Quantidade de Pilotos:")
    for nome, qtd in relatorio_pilotos:
        print(f"Escuderia {nome}: {qtd} pilotos registrados.")
    tela.pula_linha()

    #nivel 1: Qtd de corridas cadastradas no total
    cursor.execute("SELECT * FROM relatorio_qtd_corridas;")
    qtd_corridas = cursor.fetchone()[0]
    print(f"Quantidade de Corridas Cadastradas: {qtd_corridas}")
    tela.pula_linha()

    #Nivel 2: Quantidade de corridas cadastradas por circuito
    cursor.execute("SELECT * FROM relatorio_corridas_circuito;")
    corridas_circuito = cursor.fetchall()
    for nome, total, min, max, avg in corridas_circuito:
        print(f"Circuito: {nome}")
        print(f"Total de Corridas: {total}")
        print(f"Mínimo de Voltas: {min}")
        print(f"Máximo de Voltas: {max}")
        print(f"Número médio de Voltas: {avg}")
        tela.pula_linha()
    
    #Nivel 3 
    cursor.execute("SELECT * FROM relatorio_corrida_circuito_tempo;")
    corridas_tempo = cursor.fetchall()

    print(f"Quantidade de voltas e tempo por corrida, em cada circuito")
    for circuito, corrida, ano, laps, tempo in corridas_tempo:
        print(f"Circuito: {circuito}")
        print(f"Corrida: {corrida}")
        print(f"Ano: {ano}")
        print(f"Voltas: {laps}")
        print(f"Tempo: {tempo}")
        tela.pula_linha()

    cursor.close()
    conn.close()
    
    opt=1
    while(opt!=0):
        opt = int(input("Digite 0 para sair:"))
    tela.limpa_tela()