import tela 
import conection

#Função que define a tela quando o usuário faz login como escuderia
def tela_escuderia(nome_usuario):
    conn, cursor = conection.conecta_banco()

    #Busca Id do usuario 
    cursor.execute("SELECT idOriginal FROM USERS WHERE login =%s AND tipo='Escuderia'", (nome_usuario,))
    constructorId = cursor.fetchone()[0]

    #Tendo o id, vamos chamar a funcao para listar quantos pilotos temos na escuderia
    cursor.execute("SELECT * FROM info_escuderia(%s)", (constructorId,))
    info_res = cursor.fetchone()


    tela.print_cabecalho("Tela da Escuderia")
    if info_res:
        escuderia, qtd = info_res
        print(f"Bem vindo, {nome_usuario}!")
        print(f"Escuderia: {escuderia}")
        print(f"Quantidade de Pilotos da {escuderia}: {qtd}")
        tela.pula_linha()
    
    else:
        print("ERRO: Escuderia não encontrada")

    #Menu da Escuderia    
    while(True):
        print("Menu de Opções da Escuderia")
        print("Selecione uma opção.")
        print("1: Visualizar Dashboard")
        print("2: Pesquisar piloto")
        print("3: Cadastrar Piloto (via arquivo)")
        print("4: Visualizar Relatórios")
        print("5: Sair")
        opt = int(input().rstrip())

        match opt:
            case 1:
                dashboard_escuderia(constructorId)
            case 2:
                pesquisa_piloto(constructorId)
                tela.pula_linha()
            case 3:
                cadastra_piloto_arquivo(constructorId)
                tela.pula_linha()
            case 4:
                relatorios_escuderia(constructorId)
            case 5:
                tela.limpa_tela()
                break

    cursor.close()
    conn.close()

def dashboard_escuderia(constructorId):
    conn, cursor = conection.conecta_banco()
    cursor.execute("SELECT * FROM dashboard_escuderia(%s);", (constructorId,))
    res = cursor.fetchone()

    if res:
        totalvit, totalpil, primeiroano, ultimoano = res
        print(f"Total de Vitórias da Escuderia: {totalvit}")
        print(f"Total de Pilotos que já correram pela Escuderia: {totalvit}")
        print(f"Primeiro ano da Escuderia: {primeiroano}")
        print(f"Último ano da Escuderia: {ultimoano}")
        tela.pula_linha()
    
    cursor.close()
    conn.close()

#Funcao para pesquisar piloto via constructorId na página da escuderia
def pesquisa_piloto(constructorId):
    print('Insira o Forename do piloto:')
    forename = input().rstrip()

    conn, cursor = conection.conecta_banco()
    #Pesquisa para verificar se o piloto existe na escuderia cadastrada
    cursor.execute("SELECT * FROM consulta_piloto_forename(%s,%s)", (forename, constructorId))
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()

    
    if results:
        print(f"{len(results)} pilotos encontrados:\n")
        for driver in results:
            print(f"Nome: {driver[0]}, Nascimento: {driver[1]}, Nacionalidade: {driver[2]}")
    else:
        print("Nenhum piloto encontrado com esse nome para a sua escuderia.")


#Funcao para cadastrar piloto via arquivo usado como input. Página da escuderia
def cadastra_piloto_arquivo(constructorId):
    filename = input("Insira o caminho do arquivo:").rstrip()
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    
    except FileNotFoundError:
        print(f"Arquivo não encontrado")

    conn, cursor = conection.conecta_banco()

    for line in lines:
        data = line.strip().split(',')
    
        driverref = data[0]
        code = data[1]
        forename = data[2]
        surname = data[3]
        dateOfBirth = data[4]
        nationality = data[5]
        number = None 
        url = None 

        if len(data) > 6:
            number = data[6]
        if len(data) > 7:
            url = data[7]

        cursor.execute("SELECT 1 FROM DRIVERS WHERE FORENAME=%s AND surname =%s", (forename, surname))
        if cursor.fetchone():
            print(f"O piloto {forename} {surname} já foi registrado. Inserção abortada.")
            continue 
            
        cursor.execute("""INSERT INTO DRIVERS (driverref, number, code, forename, surname,
                        dateOfBirth, nationality, url) VALUES
                       (%s, %s, %s, %s, %s, %s, %s, %s)""", (driverref, number, code, forename,
                                                            surname, dateOfBirth, nationality, url))
    conn.commit()
    cursor.close()
    conn.close()
    print("Piloto(s) inseridos com sucesso.")
    
def relatorios_escuderia(constructorId):
    while(True):
        print("______Página de Relatórios da Escuderia______")
        print("Selecione o tipo de relatório:")
        print("1: Relatório de Pilotos e Vitórias")
        print("2: Relatório de Resultados por Status")
        print("3: Sair da página de relatórios")
        opt = int(input().rstrip())

        match opt:
            case 1:
                tela.limpa_tela()
                relatorio4(constructorId)
            case 2:
                tela.limpa_tela()
                relatorio5(constructorId)
            case 3:
                tela.limpa_tela()
                break
        
def relatorio4(constructorId):
    conn, cursor = conection.conecta_banco()

    print(f"Relatório 4: Pilotos e Vitórias")
    tela.pula_linha()

    cursor.execute("SELECT * FROM relatorio_vitorias_pilotos(%s);", (constructorId,))
    vitorias_pilotos = cursor.fetchall() 
    for nome, qtd in vitorias_pilotos:
        print(f"Piloto {nome}: {qtd} vitórias")
    tela.pula_linha()
    
    cursor.close()
    conn.close()
    
    opt=1
    while(opt!=0):
        opt = int(input("Digite 0 para sair:"))
    tela.limpa_tela()

def relatorio5(constructorId):
    conn, cursor = conection.conecta_banco()

    print(f"Relatório 5: Status e Resultados")
    tela.pula_linha()

    cursor.execute("SELECT * FROM relatorio_resultado_status(%s);", (constructorId,))
    results_status = cursor.fetchall() 
    for status, qtd in results_status:
        print(f"Status {status}: Quantidade {qtd}")
    tela.pula_linha()
    
    cursor.close()
    conn.close()
    
    opt=1
    while(opt!=0):
        opt = int(input("Digite 0 para sair:"))
    tela.limpa_tela()