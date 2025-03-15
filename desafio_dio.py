''' 
Para ler e escrever dados em Python, utilizamos as seguintes funções: 
- input: lê UMA linha com dado(s) de Entrada do usuário;
- print: imprime um texto de Saída (Output), pulando linha.  
'''

def calcular_saldo(transacoes):
    saldo = 0 
    for t in transacoes:
        saldo += t

    return f'Saldo: R$ {saldo:.2f}'
    

entrada_usuario = input()

entrada_usuario = entrada_usuario.strip("[]").replace(" ", "")
transacoes = [float(valor) for valor in entrada_usuario.split(",")]



resultado = calcular_saldo(transacoes)

print(resultado)