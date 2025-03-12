from datetime import datetime
from pytz import timezone

"""
    O objetivo deste desafio é refatorar o código do desafio anterior para que as funcionalidades fiquem separadas em funções.
    """

# Aqui é a representação do banco de dados
# Estas variáveis possuem o escopo global e são 
# acessadas em quase todas as funções diretamente
database = {}
contas_abertas = set(())
extratos = {}

def listar_clientes() -> None:
    for item in database.values():
        nome = item["nome"]
        cpf = item["cpf"]
        numero_conta = "-"
        agencia = "-"
        saldo = 0
        quantidade_transacoes = 0

        print(
            """
            *************************************************************************************************************
            CLIENTES DO PYTHON BANK
            NOME\t\tCPF\t\tCONTA\t\tAGÊNCIA\t\tSALDO\t\tTRANS. REALIZADAS       
            *************************************************************************************************************""")

        if len(item["conta_corrente"]) > 0:
            for conta_corrente in item["conta_corrente"].values():
                numero_conta = conta_corrente["numero_conta"]
                agencia = conta_corrente["agencia"]
                saldo = conta_corrente["saldo"]
                quantidade_transacoes = len(extratos[cpf][numero_conta]) if cpf in extratos and numero_conta in extratos[cpf] else 0
                
                print(
            f"""
            {nome}\t\t{cpf}\t\t{numero_conta}\t\t{agencia}\t\t{saldo}\t\t{quantidade_transacoes}
            """
                )
        else:
            print("Nenhuma conta encontrada!")

def sacar(*, cliente: str, numero_conta: int, valor: float) -> bool:

    if valor <= 0:
        print("Não é possível sacar valores negativos ou iguais a zero.")
        return False

    if valor > 500:
        input("Cada saque não poderá ultrapassar o valor de R$ 500,00")
        return False
    
    saldo_conta = database[cliente]["conta_corrente"][numero_conta]["saldo"]
    if valor > saldo_conta:
        input("O saldo não é suficiente! Verifique o seu Saldo.")
        return False
    
    saldo_conta -= valor
    database[cliente]["conta_corrente"][numero_conta]["saldo"] = saldo_conta
    atualizar_extrato(cliente, numero_conta, "S", valor)
    return True

def depositar(cliente:str, numero_conta:int, valor:float) -> bool:
    if valor <= 0:
        print("Não é possível depositar valores negativos ou iguais a zero.")
        ValueError("Valor inválido")
        return False
    
    if cliente not in database.keys():
        print("Cliente não encontrado")
        return False
    
    if numero_conta not in database[cliente]["conta_corrente"]:
        print("Conta não encontrada")
        return False
    
    saldo_corrente = float(database[cliente]["conta_corrente"][numero_conta]["saldo"])
    saldo_atualizado = saldo_corrente + valor
    database[cliente]["conta_corrente"][numero_conta]["saldo"] = saldo_atualizado
    atualizar_extrato(cliente, numero_conta, "D", valor)

    return True

def atualizar_extrato(cliente, conta, /, operacao, valor):
    if cliente not in extratos:
        extratos[cliente] = {}
    
    if conta not in extratos[cliente]:
        extratos[cliente][conta] = []
    
    extratos[cliente][conta].append({
        "operacao": operacao,
        "valor": valor,
        "data_hora": datetime.now(timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M:%S')
    })

def extrato(cliente, *, conta) -> bool | str:

    if (cliente not in extratos) or (conta not in extratos[cliente]):
        print("Nenhum extrato disponível para este cliente")
        return False
    
    print(
    """
    *********************************************************
    Operação\t\tData/Hora\t\tValor       
    *********************************************************
    """
    )
    for item in extratos[cliente][conta]:
        operacao = item["operacao"]
        if item["operacao"] == "D":
            operacao = "C"
        elif item["operacao"] == "S":
            operacao = "D"

        operator = "-" if item["operacao"] in ("S", "T") else "+"

        data_hora = datetime.strptime(item["data_hora"], "%Y-%m-%d %H:%M:%S")
        data_hora = data_hora.strftime("%d/%m/%Y %H:%M:%S")
        print(f"""\t\t({operacao})\t\t{data_hora}\t{operator}{item["valor"]}""")
    print(
    f"""
    *********************************************************
    
    Saldo atual: R$ {database[cliente]["conta_corrente"][conta]["saldo"]}"""
    )

def adicionar_cliente(*, nome, cpf, data_nascimento, endereco) -> str:
    cpf = str(cpf).replace(".","").replace("-","")
    criado_em = datetime.now(timezone('America/Sao_Paulo'))
    atualizado_em = datetime.now(timezone('America/Sao_Paulo'))

    if cpf in database:
        database[cpf]["nome"] = nome
        database[cpf]["cpf"] = cpf
        database[cpf]["data_nascimento"] = data_nascimento
        database[cpf]["endereco"] = endereco
        database[cpf]["atualizado_em"] = atualizado_em.strftime('%Y-%m-%d %H:%M:%S')
        return "updated"
    else:
        database[cpf] = {
            "nome": nome,
            "cpf": cpf,
            "data_nascimento": data_nascimento,
            "endereco": endereco,
            "criado_em": criado_em.strftime('%Y-%m-%d %H:%M:%S'),
            "atualizado_em": atualizado_em.strftime('%Y-%m-%d %H:%M:%S')
        }
        return "created"

def abrir_conta_corrente(*, nome, cpf, data_nascimento, endereco) -> bool:

    adicionar_cliente(
        nome=nome, 
        cpf=cpf, 
        data_nascimento=data_nascimento, 
        endereco=endereco)
    
    
    numero_conta = len(contas_abertas) + 1
    contas_abertas.add(numero_conta)

    conta_corrente = {
        "numero_conta": numero_conta,
        "agencia": "0001",
        "saldo": 0
    }

    if "conta_corrente" not in database[cpf]:
        database[cpf]["conta_corrente"] = {}

    database[cpf]["conta_corrente"][numero_conta] = conta_corrente

    return True

def atingiu_limite_diario(*, cpf, conta) -> bool:
    LIMITE_TRANSACOES_DIARIAS = 10    
    hoje = datetime.now(timezone('America/Sao_Paulo')).date()
    operacoes_diarias = [item for item in extratos[cpf][conta] if item['data_hora'].date() == hoje]

    if len(operacoes_diarias) >= LIMITE_TRANSACOES_DIARIAS:
        return True
    return False

def main():

    menu = """
        Informe uma operação para iniciar
        # Depósito (D)
        # Extrato (E)
        # Saque (S)
        # Nova Conta (N)
        # Listar Clientes (LC)
        # Sair (Q)
    """

    VALIDS_OPERATIONS = ["D", "E", "S", "N", "LC", "T", "Q"]
    operacao_selecionada = ""

    while operacao_selecionada != "Q":

        user_input = input(menu)
        operacao_selecionada = user_input.upper()

        if operacao_selecionada not in VALIDS_OPERATIONS:
            print(f"Operação inválida: [{operacao_selecionada}]. Tente novamente!")
            continue

        if operacao_selecionada == "N":
            nome = input("Informe o nome do cliente: ")
            cpf = input("Informe o CPF do cliente: ")
            data_nascimento = input("Informe a data de nascimento do cliente: ")
            endereco = input("Informe o endereço do cliente: ")

            abrir_conta_corrente(nome=nome, 
                cpf=cpf, 
                data_nascimento=data_nascimento, 
                endereco=endereco)
            
        if operacao_selecionada == "E":
            cpf_cliente = str(input("Informe o cpf do titular da conta: "))
            numero_conta_destino = int(input("Informe o número da conta: "))
            extrato(cpf_cliente, conta=numero_conta_destino)

        if operacao_selecionada == "D":
            cpf_cliente = str(input("Informe o cpf do titular da conta que vai receber o depósito: "))
            numero_conta_destino = int(input("Informe o número da conta que receberá o depósito: "))
            valor = float(input("Informe o valor para depósito: "))            
            depositar(cpf_cliente, numero_conta_destino, valor)

        if operacao_selecionada == "S":
            cpf_cliente = str(input("Informe o cpf do titular da conta que vai realizar o saque: "))
            numero_conta_destino = int(input("Informe o número da conta: "))
            valor = float(input("Informe o valor para saque: "))            

            if atingiu_limite_diario(cpf=cpf_cliente, conta=numero_conta_destino):
                print("Você atingiu o limite de operações diárias.")
                continue

            sacar(cliente=cpf_cliente, numero_conta=numero_conta_destino, valor=valor)
            
        if operacao_selecionada == "LC":
            listar_clientes()


main()