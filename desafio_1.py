# Operações
# Depósito (D)
# Extrato (E)
# Saque (S)
# Sair (Q)

from datetime import datetime


def operacao():

    menu = """
        Informe uma operação para iniciar
        # Depósito (D)
        # Extrato (E)
        # Saque (S)
        # Sair (Q)
    """
    balance = 0
    statements = []
    WITHDRAWAL_DAY_LIMIT = 3    
    VALIDS_OPERATIONS = ["D", "E", "S", "Q"]
    operation_chosen = ""

    while operation_chosen != "Q":

        user_input = input(menu)
        operation_chosen = user_input.upper()
        
        if operation_chosen not in VALIDS_OPERATIONS:
            print(f"Operação inválida: [{operation_chosen}]. Tente novamente!")
            continue

        if operation_chosen == "D":
            user_deposit = float(input("Informe o valor para depósito: "))

            if user_deposit <= 0:
                print("Não é possível depositar valores negativos ou iguais a zero.")
                continue

            balance += user_deposit
            now = datetime.now()
            statements.append({
                'operation': operation_chosen,
                'value': user_deposit,
                'date_time': now.strftime("%d-%m-%Y %H:%M:%S")
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
            
            if withdrawal_count >= WITHDRAWAL_DAY_LIMIT:
                input(f"O limite diário de {WITHDRAWAL_DAY_LIMIT} foi atingido. Entre em contato com seu gerente.")
                continue

            if user_withdrawal > balance:
                input("O saldo não é suficiente! Verifique o seu Saldo.")
                continue
            
            else:
                balance -= user_withdrawal
                now = datetime.now()
                statements.append({
                    'operation': operation_chosen,
                    'value': user_withdrawal,
                    'date_time': now.strftime("%d-%m-%Y %H:%M:%S")
                })

        if operation_chosen == "E":
            print("Extrato da aplicação")
            val = 0
            for item in statements:
                operation = ""
                if item["operation"] == "D":
                    operation = "C"
                elif item["operation"] == "S":
                    operation = "D"

                operator = "-" if item["operation"] == "S" else "+"

                if item["operation"] == "S":
                    val -= item["value"]
                elif item["operation"] == "D":
                    val += item["value"]

                print(f"({operation})      {operator}{item["value"]}            {item["date_time"]}")
            print(f"Saldo atual: R$ {val}")
        
operacao()
