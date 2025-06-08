from typing import Optional
import os

# TODO Add limpa_tela and pula_linhas in the printing stuff
class ScreenUtils:
    def clear():
        os.system("clear")

    def pula_linha():
        print("________________________________")
        print("\n\n\n")
    
    def print_divisor():
        print("\n" + "-" * 20 + "\n")

    @staticmethod
    def welcome():
        print("___*** Projeto Final de Laboratório de Bases de Dados ***___\n\n")
        print("____________Sistema de Gerenciamento da Formula1____________\n\n")
        print("Login")
        print("--------------")


def print_divisor():
    print("\n" + "-" * 20 + "\n")


def read_cli(msg: Optional[str]) -> str:
    return input(msg).rstrip()
