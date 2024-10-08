## Sistema Bancário
import textwrap
from datetime import datetime, timedelta

def depositar(saldo, extrato, data_atual, numero_operações,/):
    deposito = float(input("Informe o valor que você gostaria de depositar: "))

    if deposito > 0:
        saldo += deposito
        data_atual = datetime.now("%d/%m/%Y %H:%M")
        extrato += (f"Deposito Realizado:\tR$ {deposito:.2f}     {data_atual}\n")
        numero_operações += 1
        print(f"\nDepósito realizado,\n Seu saldo atual é de R$ {saldo}")
            
    else:
                print("\nO valor do depósito não pode ser um valor negativo")

def sacar(*, saldo, valor_limites_p_saques, LIMITE_SAQUES, numero_saque, numero_operações, extrato):
    saque = float(input("Informe qual o valor que você gostaria de sacar: "))

    excedeu_saldo = saque > saldo

    excedeu_limite_diario= saque > valor_limites_p_saques

    excedeu_numero_saques= numero_saque > LIMITE_SAQUES
            
    if excedeu_saldo:
        print ("Saque Inválido! O valor informado é maior doq o seu saldo em conta.")
                
    elif excedeu_limite_diario:
        print ("Saque Inválido! O valor informado é maior doq o limte diário para saques (R$ 500,00), em sua conta.") 

    elif excedeu_numero_saques:
        print ("Saque Inválido! Você já realizou o numero máximo (3 saques) de saques por dia.")

    else:
        saldo -= saque
        numero_saque += 1
        numero_operações += 1
        data_atual = datetime.now("%d/%m/%Y %H:%M")
        extrato += (f"Saque Realizado:\t R$ {saque:.2f}       {data_atual}\n")
        print(f"\nSaque Realizado!, \n Seu saldo atual é de: R$ {saldo}")  

def exibir_extrato(extrato, saldo):
    print(f"======== Extrato ========\n\n\n", {extrato}, "\n\n\n=========================")
    print(f"\nSaldo: R$ {saldo:.2f}")

def verificar_cpf_existe(cpf, usuários):
    for usuário in usuários:
        if usuário["cpf"] == cpf:
            return True  # CPF já existe
    return False  # CPF não existe

def criar_usuário(usuários):
    cpf = input("Informe seu CPF: ")
    
    # Verifica se o CPF já existe
    if verificar_cpf_existe(cpf, usuários):
        print("\nJá existe um usuário com este CPF!!")
    else:
        nome = input("Informe o seu nome completo: ")
        data_nascimento = input("Informe sua data de nascimento [dd/mm/aaaa]: ")
        endereço = input("Informe seu endereço [logradouro, nº - bairro, cidade/sigla estado]: ")
        data_atual = datetime.now("%d/%m/%Y %H:%M")

        # Cria um dicionário com os dados do usuário
        novo_usuário = {
            "cpf": cpf,
            "nome": nome,
            "data_nascimento": data_nascimento,
            "endereço": endereço
        }

        # Adiciona o dicionário à lista de usuários
        usuários.append(novo_usuário)
        print(f"\nUsuário criado com sucesso!! às {data_atual}")

def criar_conta(cpf, usuários, contas):
    data_atual = datetime.now("%d/%m/%Y %H:%M")
    # Verifica se o CPF já existe
    if not verificar_cpf_existe(cpf, usuários):
        print("\nCPF não encontrado. Por favor, crie o usuário primeiro.")
        return

    # Agência fixa
    agencia = "0001"
    
    # Número da conta começa em 0 e incrementa de acordo com o número de contas já criadas
    numero_conta = len(contas) + 1

    # Cria um dicionário com os dados da conta
    nova_conta = {
        "agencia": agencia,
        "numero_conta": str(numero_conta).zfill(5),  # Adiciona zeros à esquerda para formar 5 dígitos
        "cpf": cpf
    }

    # Adiciona a nova conta à lista de contas
    contas.append(nova_conta)
    print(f"\nConta criada com sucesso para o CPF {cpf}!        {data_atual}")
    print(f"Agência: {agencia}, Número da Conta: {nova_conta['numero_conta']}")

# Função para listar todas as contas
def listar_contas(contas):
    data_atual = datetime.now("%d/%m/%Y %H:%M")
    if not contas:
        print("\nNenhuma conta cadastrada.")
        return
    
    print("\nListagem de Contas:")
    for conta in contas:
        print("======== Lista de Contas ========\n\n")
        print(f"\tAgência: {conta['agencia']}, \n\tNúmero da Conta: {conta['numero_conta']}, \tCPF: {conta['cpf']}")
        print("\n\n=================================")
        print(f"\t{data_atual}")

# Exemplo de uso da função

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    valor_limites_p_saque = 500 
    extrato = ""
    numero_saque = 0
    numero_operações = 0
    numero_conta = 0
    data_atual = datetime
    
    nome = ""
    data_nascimento = ""
    endereço = ""
    usuários = []
    contas = []
    menu = '''\n 
            ====== Escolha uma Operação ======
            [1] \tDepositar
            [2] \tSacar
            [3] \tExtrato
            [4] \tCriar Usuário
            [5] \tCriar Conta
            [6] \tListar Conta
            [7] \tSair
            ==================================\n
            ''' 
    while True:
        operação = int(input(menu))

        if operação in [1, 2, 3, 5]:
            cpf = input("Informe o seu CPF (somente números): ")
            if not verificar_cpf_existe(cpf, usuários):
                print("\nCPF não encontrado. Por favor, crie o usuário primeiro (opção 4).")
                continue
        
        if operação == 1 and numero_operações < 10 :
            depositar(saldo,extrato,data_atual,numero_operações)
                                    
        elif operação == 2 and numero_operações < 10:
            sacar (saldo=saldo,
            valor_limites_p_saques= valor_limites_p_saque,
            limite_saque= LIMITE_SAQUES,
            numero_operações=numero_operações,
            extrato=extrato)
                    
        elif operação == 3 and numero_operações < 10:
            exibir_extrato (
            extrato=extrato,
            saldo=saldo)
                  
        elif operação == 4 and numero_operações < 10:
            criar_usuário(usuários)
            

        elif operação == 5  and numero_operações < 10:
            cpf = input("Informe o seu CPF (somente números): ")
            criar_conta(cpf,usuários,contas)

        elif operação == 6 and numero_operações < 10:
            listar_contas(contas) 

        elif operação > 7 and numero_operações < 10:
            print("""Operação inválida!! 
            Selecione uma operação Válida.
            """) 
                                    
        elif operação == 7 and numero_operações < 10:
            break

        else:
            print("\n\n\nVocê excedeu o limite diário de operações (10 operações).")
            break
                 
print(main())
        
