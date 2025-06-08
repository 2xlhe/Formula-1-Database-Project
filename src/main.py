from utils import read_cli
from display import *
from operations import connect_db, Login
import yaml
import argparse


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", type=str, required=True, help="Path to YAML file with DB config"
    )
    args, _ = parser.parse_known_args()
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)
    return config


config = parser()


if __name__ == "__main__":
    db = connect_db(config)

    ScreenUtils.welcome()
    ScreenUtils.clear()

    curs, conn = db

    # User Login
    login = Login(cursor=curs, conn=conn)

    while True:
        username = read_cli("Digite seu usuário: ")
        password = read_cli("Digite sua senha: ")
        info = login.login(username, password)
        if info is not None:
            account_type, user_id = info
            break
        else:
            print("Usuário ou senha incorretos. Tente novamente.\n")

    ScreenUtils.clear()

    if account_type == "Administrador":
        AdminScreen(username, curs).display()
    elif account_type == "Escuderia":
        ScuderiaScreen(username, user_id, curs).display()
    elif account_type == "Piloto":
        PilotScreen(username, curs).display()
    else:
        print("Tipo de conta desconhecido.")
