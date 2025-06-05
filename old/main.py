import hashlib
import psycopg2
from psycopg2 import sql
import getpass
import os
#deixar mais modularizado


def pula_linha():
    print('________________________________')
    print('\n\n\n')

def conecta_banco():
    connection = psycopg2.connect(host="localhost", port="5432",
                                  dbname="fia", user="postgres", password="postgres")
    cursor = connection.cursor()
    return connection, cursor

def log_user(user_id):
    conn, cursor = conecta_banco()
    cursor.execute(sql.SQL("INSERT INTO USERS_LOG (userId) VALUES (%s)"), (user_id,))
    conn.commit()
    cursor.close()
    conn.close()



def login(user_input, senha_input):
    conn, cursor = conecta_banco()

    cursor.execute(sql.SQL("SELECT userid, tipo, password FROM USERS" \
                            " WHERE login=%s"), (user_input,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()

    if resultado:
        user_id, tipo_user, senha_real = resultado

        senha_input_hash = hashlib.sha256(senha_input.encode('utf-8')).hexdigest()

        if senha_real == senha_input_hash:
            print("Login realizado com sucesso!")
            log_user(user_id)
            return tipo_user 
        else:
            print("Senha incorreta! Tente novamente.")
    
    else:
        print("Usuário não registrado! Tente novamente.\n\n\n\n\n\n")
        return None 


def cadastra_escuderia():
    cursor.execute("SELECT COALESCE(MAX(constructorId), 0) + 1 FROM CONSTRUCTORS")
    new_id = cursor.fetchone()[0]

    print("Constructor Reference:")
    constructorref = input().rstrip()
    print("Constructor Name:")
    name = input().rstrip()
    print("Nacionalidade:")
    nationality = input().rstrip()
    print("URL:")
    url = input().rstrip()

    conn, cursor = conecta_banco()
    cursor.execute("INSERT INTO CONSTRUCTORS (constructorref, name, nationality, url) VALUES (%s, %s, %s, %s)", 
                                    (constructorref, name, nationality, url))
    conn.commit()

    cursor.close()
    conn.close()
    return 0

def cadastra_piloto():
    return 0

def tela_admin(nome_usuario):
    conn, cursor = conecta_banco()

    print(f"Bem vindo, {nome_usuario}")
    print("Tela do Administrador do Sistema")
    pula_linha()
    print("Ano para as pesquisas: ")
    ano_pesquisa = int(input().rstrip())
    
    #Lista total de pilotos, escuderias e temporas
    print("__________Visão geral:__________")
    cursor.execute("SELECT * FROM dashboard_admin_totais()")
    totalP, totalE, totalT = cursor.fetchone()
    print(f"Total de pilotos registrados: {totalP}")
    print(f"Total de escuderias registradas: {totalE}")
    print(f"Total de temporadas registradas: {totalT}")
    pula_linha()

    #Lista de todas as corridas no ano, total de voltas e tempo
    print("__________Resumo das corridas:__________")
    cursor.execute("SELECT * FROM dashboard_admin_corridas(%s)",        (ano_pesquisa,))
    for nome, voltas, tempo in cursor.fetchall():
        print(f"{nome}: {voltas} voltas, tempo total: {tempo}")
    pula_linha()

    #Lista de todas as escuderias no ano e pontuacao total
    print("__________Resumo das Escuderias:__________")
    cursor.execute("SELECT * FROM dashboard_admin_escuderias(%s)", (ano_pesquisa,))
    for nome, pontos in cursor.fetchall():
        print(f"{nome}: Pontuação {pontos}")
    pula_linha()


    #Lista todos os pilotos no ano corrente e pontuacao
    print("__________Resumo dos pilotos:__________")
    cursor.execute("SELECT * FROM dashboard_admin_pilotos(%s)", (ano_pesquisa,))
    for piloto, pontuacao in cursor.fetchall():
        print(f"{piloto}: {pontuacao} pontos.")
    pula_linha()

    cursor.close()
    conn.close()

    opt = 0
    while(opt!=2):
        print("Menu de Opções do Administrador")
        print("Selecione uma opção.")
        print("0: Cadastrar Escuderia")
        print("1: Cadastrar Piloto")
        print("2: Sair")
        opt = int(input().rstrip())

        match opt:
            case 0:
                cadastra_escuderia()
            case 1:
                cadastra_piloto
            case 2:
                break
    
    


def tela_escuderia(nome_usuario):
    conn, cursor = conecta_banco()

    #Busca Id do usuario 
    cursor.execute("SELECT idOriginal FROM USERS WHERE login =%s AND tipo='Escuderia'", (nome_usuario,))
    constructorId = cursor.fetchone()[0]

    #Tendo o id, vamos chamar a funcao para listar quantos pilotos temos na escuderia
    cursor.execute("SELECT * FROM dashboard_escuderia(%s)", (constructorId,))
    dashboard_res = cursor.fetchone()

    if dashboard_res:
        escuderia, qtd = dashboard_res
        print(f"Bem vindo, {nome_usuario}!")
        print("Tela da Escuderia")
        print(f"Escuderia: {escuderia}")
        print(f"Quantidade de Pilotos da {escuderia}: {qtd}")
    
    else:
        print("ERRO: Escuderia não encontrada")

    cursor.close()
    conn.close()



def tela_piloto(nome_usuario):
    conn, cursor = conecta_banco()

    #Busca Id do usuario 
    cursor.execute("SELECT idOriginal FROM USERS WHERE login =%s AND tipo='Piloto'", (nome_usuario,))
    driverId = cursor.fetchone()[0]

    #Tendo o id, vamos chamar a funcao para listar o nome do piloto e escuderia
    cursor.execute("SELECT * FROM dashboard_piloto(%s)", (driverId,))
    dashboard_res = cursor.fetchone()

    if dashboard_res:
        nome, escuderia = dashboard_res
        print(f"Bem vindo, {nome_usuario}!")
        print("Tela do Piloto")
        print(f"Piloto: {nome}")
        print(f"Sua escuderia é: {escuderia}")
    
    else:
        print("ERRO: Piloto não encontrado")

    cursor.close()
    conn.close()

def menu():
    while True:
        exibe_mensagens()

        print("Digite seu nome de usuário:")
        login_input = input().rstrip()
        print("Digite sua senha:")
        senha_input = input().rstrip()
        tipo_usuario = login(login_input, senha_input)
        
        #Direciona para cada tela de acordo com o tipo de usuario
        if tipo_usuario is not None:
            limpa_tela()
            match tipo_usuario:
                case 'Administrador':
                    tela_admin(login_input)
                case 'Escuderia':
                    tela_escuderia(login_input)
                case 'Piloto':
                                tela_piloto(login_input)





if __name__ == "__main__":
    menu()