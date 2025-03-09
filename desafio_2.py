# Operações
# Depósito (D)
# Extrato (E)
# Saque (S)
# Sair (Q)

from datetime import datetime
from pytz import timezone


def app():

    menu = """
        Informe uma operação para iniciar
        # Depósito (D)
        # Extrato (E)
        # Saque (S)
        # Transferência (T)
        # Sair (Q)
    """

    balance = 0
    statements = []
    TRANSACTIONS_DAY_LIMIT = 10    
    VALIDS_OPERATIONS = ["D", "E", "S", "T", "Q"]
    operation_chosen = ""

    while operation_chosen != "Q":

        user_input = input(menu)
        operation_chosen = user_input.upper()
        
        if operation_chosen not in VALIDS_OPERATIONS:
            print(f"Operação inválida: [{operation_chosen}]. Tente novamente!")
            continue

        today = datetime.now(timezone('America/Sao_Paulo')).date()
        daily_operations = [item for item in statements if item['date_time'].date() == today]

        if len(daily_operations) >= TRANSACTIONS_DAY_LIMIT and operation_chosen != "E":
            print("Você atingiu o limite de operações diárias.")
            continue

        if operation_chosen == "D":
            user_deposit = float(input("Informe o valor para depósito: "))

            if user_deposit <= 0:
                print("Não é possível depositar valores negativos ou iguais a zero.")
                continue

            balance += user_deposit
            now = datetime.now(timezone('America/Sao_Paulo'))
            statements.append({
                'operation': operation_chosen,
                'value': user_deposit,
                'date_time': now
            })

        if operation_chosen == "S":
            user_withdrawal = float(input("Informe o valor para saque: "))

            if user_withdrawal > 500:
                input("Cada saque não poderá ultrapassar o valor de R$ 500,00")
                continue

            withdrawal_count = 0
            for item in statements:
                if item["operation"] == "S":
                    withdrawal_count += 1            

            if user_withdrawal > balance:
                input("O saldo não é suficiente! Verifique o seu Saldo.")
                continue
            
            else:
                balance -= user_withdrawal
                now = datetime.now(timezone('America/Sao_Paulo'))
                statements.append({
                    'operation': operation_chosen,
                    'value': user_withdrawal,
                    'date_time': now
                })

        if operation_chosen == "E":
            print(
            """
            *********************************************************
            Operação\t\tData/Hora\t\tValor       
            *********************************************************
            """
            )
            for item in statements:
                operation = item["operation"]
                if item["operation"] == "D":
                    operation = "C"
                elif item["operation"] == "S":
                    operation = "D"

                operator = "-" if item["operation"] in ("S", "T") else "+"

                date_time = item["date_time"].strftime("%d/%m/%Y %H:%M:%S")
                print(f"""\t\t({operation})\t\t{date_time}\t{operator}{item["value"]}""")
            print(
            f"""
            *********************************************************
            
            Saldo atual: R$ {balance}"""
            )

        if operation_chosen == "T":
            transfer_amount = float(input("Informe o valor para transferência: "))
            target_account = input("Informe a conta de destino: ")

            if transfer_amount <= 0:
                print("Não é possível transferir valores negativos ou iguais a zero.")
                continue

            if transfer_amount > balance:
                print("O saldo não é suficiente! Verifique o seu Saldo.")
                continue

            balance -= transfer_amount
            now = datetime.now(timezone('America/Sao_Paulo'))
            statements.append({
                'operation': operation_chosen,
                'value': transfer_amount,
                'date_time': now,
                'target_account': target_account
            })
            print(f"Transferência de R$ {transfer_amount} para a conta {target_account} realizada com sucesso.")

app()
