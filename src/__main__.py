from utils import read_cli
from display import *
from operations import connect_db, Login

if __name__ == "__main__":
    conn, curs = connect_db()

    ScreenUtils.welcome()
    ScreenUtils.clear()

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
