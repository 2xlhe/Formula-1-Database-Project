import tela 
import conection 

#Função que define a tela quando o usuário faz login como piloto
def tela_piloto(nome_usuario):
    conn, cursor = conection.conecta_banco()

    #Busca Id do usuario 
    cursor.execute("SELECT idOriginal FROM USERS WHERE login =%s AND tipo='Piloto'", (nome_usuario,))
    driverId = cursor.fetchone()[0]

    #Tendo o id, vamos chamar a funcao para listar o nome do piloto e escuderia
    cursor.execute("SELECT * FROM info_piloto(%s)", (driverId,))
    info_res = cursor.fetchone()

    tela.print_cabecalho("Tela do Piloto")
    if info_res:
        nome, escuderia = info_res
        print(f"Bem vindo, {nome_usuario}!")
        print(f"Piloto: {nome}")
        print(f"Sua escuderia é: {escuderia}")
    
    else:
        print("ERRO: Piloto não encontrado")


    cursor.close()
    conn.close()

def dashboard_piloto(driverId):
    conn, cursor = conection.conecta_banco()

    cursor.execute("SELECT * FROM dashboard_piloto_ano(%s);", (driverId,))
    primeiro, ultimo = cursor.fetchone() 
    print(f"Primeiro Ano do Piloto: {primeiro}")
    print(f"Último Ano do Piloto: {ultimo}")
    tela.pula_linha()

    cursor.execute("SELECT * FROM dashboard_piloto_vitorias(%s);", (driverId,))
    for linha in cursor.fetchall():
        ano, circuito, pontos, vitorias, corridas = linha 
        print(f"Ano: {ano}")
        print(f"Circuito: {circuito}")
        print(f"Pontos: {pontos}")
        print(f"Vitorias: {vitorias}")
        print(f"Quantidade de Corridas: {corridas}")
        tela.pula_linha()
    

    cursor.close()
    conn.close()

def relatorios_piloto(driverId):
    while(True):
        print("______Página de Relatórios do Piloto______")
        print("Selecione o tipo de relatório:")
        print("1: Total de Pontos obtidos por ano")
        print("2: Quantidade de resultados por status")
        print("3: Sair da página de relatórios")
        opt = int(input().rstrip())

        match opt:
            case 1:
                tela.limpa_tela()
                relatorio6(driverId)
            case 2:
                tela.limpa_tela()
                relatorio7(driverId)
            case 3:
                tela.limpa_tela()
                break

def relatorio6(driverId):
    conn, cursor = conection.conecta_banco()

    print(f"Relatório 6: Pontuação obtida por ano")
    tela.pula_linha()

    cursor.execute("SELECT * FROM relatorio_pontos_por_ano(%s);", (driverId,))
    pontos = cursor.fetchall() 
    curr_ano = None
    for ano, corrida, ptos in pontos:
        if ano != curr_ano:
            if curr_ano is not None:
                print()
            print(f"Ano: {ano}")
            curr_ano = ano 
        print(f"Corrida: {corrida}, Pontuação: {ptos}")
        
    
    cursor.close()
    conn.close()
    
    opt=1
    while(opt!=0):
        opt = int(input("Digite 0 para sair:"))
    tela.limpa_tela()

def relatorio7(driverId):
    conn, cursor = conection.conecta_banco()

    print(f"Relatório 7: Quantidade de resultados por cada Status")
    tela.pula_linha()

    cursor.execute("SELECT * FROM relatorio_status_piloto(%s);", (driverId,))
    status_res = cursor.fetchall()
    for status, qtd in status_res:
        print(f"Status {status}: Quantidade {qtd}")
    tela.pula_linha()
        
    cursor.close()
    conn.close()
    
    opt=1
    while(opt!=0):
        opt = int(input("Digite 0 para sair:"))
    tela.limpa_tela()