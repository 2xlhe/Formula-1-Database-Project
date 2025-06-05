import hashlib
import psycopg2
from psycopg2 import sql
import getpass
import os
import tela
import conection
import admin
import constructor
import driver

#Registra o login do usuario na tabela de logs
def log_user(user_id):
    conn, cursor = conection.conecta_banco()
    cursor.execute(sql.SQL("INSERT INTO USERS_LOG (userId) VALUES (%s)"), (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

#Faz o login do usuario a partir dos inputs fornecidos
def login(user_input, senha_input):
    conn, cursor = conection.conecta_banco()

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

def menu():
    while True:
        tela.print_menu_inicial()

        #Realiza login do usuario
        login_input = input("Digite seu nome de usuário:").rstrip()
        senha_input = getpass.getpass("Digite sua senha:")
        tipo_usuario = login(login_input, senha_input)
        
        #Direciona para cada tela de acordo com o tipo de usuario
        if tipo_usuario is not None:
            tela.limpa_tela()
            match tipo_usuario:
                case 'Administrador':
                    admin.tela_admin(login_input)
                case 'Escuderia':
                    constructor.tela_escuderia(login_input)
                case 'Piloto':
                    driver.tela_piloto(login_input)

if __name__ == "__main__":
    menu()