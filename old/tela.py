import os

def limpa_tela():
    os.system('clear')

def pula_linha():
    print('_' * 20)
    print('\n\n\n')

def print_menu_inicial():
    print("\n" + "=" * 60)
    print("Projeto Final de Laboratório de Bases de Dados".center(60))
    print("Sistema de Gerenciamento da FIA".center(60))
    print("=" * 60 + "\n")


def print_cabecalho(titulo, largura=60):
    print("\n" + "=" * largura)
    print(titulo.center(largura))
    print("=" * largura + "\n")