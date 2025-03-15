def filtrar_transacoes(transacoes, limite):
    transacoes_filtradas = []

    for transacao in transacoes:
        if transacao < 0 and (transacao * -1) > limite:
            transacoes_filtradas.append(transacao)
        elif transacao > limite:
            transacoes_filtradas.append(transacao)
    return transacoes_filtradas


entrada = input()

entrada_transacoes, limite = entrada.split("],")
entrada_transacoes = entrada_transacoes.strip("[]").replace(" ", "") 
limite = float(limite.strip())  # Converte o limite para float

transacoes = [int(valor) for valor in entrada_transacoes.split(",")]

resultado = filtrar_transacoes(transacoes, limite)


print(f"Transações: {resultado}")