from abc import ABC, abstractmethod
from datetime import datetime
import textwrap
import os
from pathlib import Path
import csv
caminho_da_pasta = Path ("/Volumes/PortableSSD/aulas_python/desafios/transacoes.csv")

class Cliente:
    def __init__(self, endereço):
        self.endereço = endereço
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Pessoa_Fisíca(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereço):
        super().__init__(endereço)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ({self.cpf})>"

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._agencia = "0001"
        self._numero = numero 
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor_saque):
        saldo = self._saldo
        excedeu_saldo = valor_saque > saldo

        if excedeu_saldo:
            print("\nSaque Inválido! O valor informado é maior do que seu saldo em conta.")
        
        elif valor_saque > 0:
            self._saldo -= valor_saque
            print(f"\nSaque Realizado!, \n Seu saldo atual é de: R$ {self.saldo:.2f}")  
            return True
        
        else:
            print("\nSaque Inválido! O valor informado é inválido!")
            return False

    def depositar(self, valor_deposito):
        if valor_deposito > 0:
            self._saldo += valor_deposito
            print(f"\nDepósito realizado,\n Seu saldo atual é de R$ {self.saldo:.2f}")
        else:
            print("\nDepósito Inválido! Não é possível depositar um valor negativo.")
            return False
        
        return True
        
class Conta_Corrente(Conta):
    def __init__(self, numero, cliente, valor_limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._valor_limite = valor_limite
        self._limite_saques = limite_saques

    def sacar(self, valor_saque):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        excedeu_limite = valor_saque > self._valor_limite
        excedeu_saques = numero_saques >= self._limite_saques  # Alterado para verificar se atingiu o limite

        if excedeu_limite:
            print("Saque Inválido! O valor informado é maior do que o limite diário para saques (R$ 500,00), em sua conta.")
        
        elif excedeu_saques:
            print("Saque Inválido! Você já realizou o número máximo (3 saques) de saques por dia.")
        
        else:
            if super().sacar(valor_saque): 
                saque = Saque(valor_saque)
                self.historico.adicionar_transacao(saque)
                return True  # <-- isso estava faltando

        
        return False
    
    def __repr__(self):
        return f"<{self.__class__.__name__}: ('{self.agencia}'' , '{self.numero}', '{self.cliente.nome}')>"

    def __str__(self):
        return f"""\ 
                Agência:    {self.agencia}
                C/C:        {self.numero}
                Titular:    {self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime('%d/%m/%Y %H:%M'),
            }
        )

    def exibir_extrato(self):
        print("\n=== Extrato da Conta ===")
        for transacao in self._transacoes:
            print(f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}")

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self):
        pass
    
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor_deposito):
        self._valor_deposito = valor_deposito

    @property
    def valor(self):
        return self._valor_deposito
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)

        if resultado is None:
            return

        conta = resultado  # resultado retornado da função decorada

        ultima_transacao = conta.historico.transacoes[-1]
        tipo = ultima_transacao["tipo"]
        valor = ultima_transacao["valor"]
        data = ultima_transacao["data"]
        nome = conta.cliente.nome
        cpf = conta.cliente.cpf
        agencia = conta.agencia
        numero = conta.numero

        with open(caminho_da_pasta, "a", newline="") as arquivo:
            arquivo.write(f"{nome},{cpf},{agencia},{numero},{tipo},{valor},{data}\n")

        return resultado
    return envelope

def criar_cliente(clientes):
    cpf = input("Informe o seu CPF (somente números): ")
    cliente = verificar_cpf_existe(cpf, clientes)
    
    if cliente:
        print("\nJá existe um cliente com esse CPF!!")
        return
    
    nome = input("Informe o seu nome completo: ")
    data_nascimento = input("Informe sua data de nascimento [dd/mm/aaaa]: ")
    endereço = input("Informe seu endereço [logradouro, nº - bairro, cidade/sigla estado]: ")
    
    cliente = Pessoa_Fisíca(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereço=endereço)
    clientes.append(cliente)
    print(f"\nUsuário criado com sucesso!! às {datetime.now().strftime('%d/%m/%Y %H:%M')}")

def criar_conta(clientes, numero_conta, contas):
    cpf = input("Informe o seu CPF (somente números): ")
    cliente = verificar_cpf_existe(cpf, clientes)
    
    if not cliente:
        print("\nCPF não encontrado. Por favor, crie o usuário primeiro (opção 1).")
        return
    
    conta = Conta_Corrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta) 
    print(f"\nConta criada com sucesso!! às {datetime.now().strftime('%d/%m/%Y %H:%M')}")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100, "\n")
        print(textwrap.dedent(str(conta)))
        print("=" * 100, "\n")

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta!")
        return None  

    return cliente.contas[0]

@log_transacao
def depositar(clientes):
    cpf = input("Informe o seu CPF (somente números): ")
    cliente = verificar_cpf_existe(cpf, clientes)

    if not cliente:
        print("\nCPF não encontrado. Por favor, crie o usuário primeiro (opção 1).")
        return
    
    valor_deposito = float(input("Informe o valor que você gostaria de depositar: "))
    transacao = Deposito(valor_deposito)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

    # Acesso ao saldo da conta
    print(f"\nDepósito realizado, às {datetime.now().strftime('%d/%m/%Y %H:%M')}\nSeu saldo atual é de R$ {conta.saldo:.2f}")

@log_transacao
def sacar(clientes):
    cpf = input("Informe o seu CPF (somente números): ")
    cliente = verificar_cpf_existe(cpf, clientes)

    if not cliente:
        print("\nCPF não encontrado. Por favor, crie o usuário primeiro (opção 1).")
        return
    
    valor_saque = float(input("Informe o valor que você gostaria de sacar: "))
    transacao = Saque(valor_saque)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

    # Acesso ao saldo da conta
    print(f"\nSaque realizado, às {datetime.now().strftime('%d/%m/%Y %H:%M')}\nSeu saldo atual é de R$ {conta.saldo:.2f}")


def exibir_extrato(clientes):
    cpf = input("Informe o seu CPF (somente números): ")
    cliente = verificar_cpf_existe(cpf, clientes)

    if not cliente:
        print("\nCPF não encontrado. Por favor, crie o usuário primeiro (opção 1).")
        return

    conta = recuperar_conta_cliente(cliente)
    if conta:
        conta.historico.exibir_extrato()

def verificar_cpf_existe(cpf, clientes):
    
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    
    if clientes_filtrados:
        return clientes_filtrados[0]  # Retorna o primeiro cliente encontrado
    
    return None

def carregar_dados(caminho, clientes, contas):
    if not caminho.exists():
        return  # Arquivo ainda não existe, começa vazio

    clientes_dict = {}
    contas_dict = {}

    with open(caminho, newline='') as arquivo:
        leitor = csv.reader(arquivo)
        for linha in leitor:
            nome, cpf, agencia, numero, tipo, valor, data_str = linha

            # Criar cliente se não existir
            if cpf not in clientes_dict:
                cliente = Pessoa_Fisíca(nome=nome, cpf=cpf, data_nascimento="01/01/1970", endereço="Desconhecido")
                clientes_dict[cpf] = cliente
                clientes.append(cliente)
            else:
                cliente = clientes_dict[cpf]

            # Criar conta se não existir
            if numero not in contas_dict:
                conta = Conta_Corrente.nova_conta(numero=numero, cliente=cliente)
                contas_dict[numero] = conta
                contas.append(conta)
                cliente.adicionar_conta(conta)
            else:
                conta = contas_dict[numero]

            # Criar transação e adicionar ao histórico
            valor = float(valor)
            if tipo == "Deposito":
                transacao = Deposito(valor)
            elif tipo == "Saque":
                transacao = Saque(valor)
            else:
                continue  # Tipo desconhecido, ignora

            # Adiciona transação ao histórico (ajustar data se quiser usar a original)
            conta.historico.adicionar_transacao(transacao)

def main():
    clientes = []
    contas = []
    carregar_dados(caminho_da_pasta, clientes, contas)
    menu = '''\n
    ====== Escolha uma Operação ======
    [1] Criar Usuário
    [2] Criar Conta
    [3] Depositar
    [4] Sacar
    [5] Extrato
    [6] Listar Contas
    [7] Sair
    ==================================\n
    '''

    while True:
        try:
            opcao = int(input(menu))
        except ValueError:
            print("Entrada inválida. Digite um número de 1 a 7.")
            continue
        
        if opcao == 1:
            criar_cliente(clientes)
        elif opcao == 2:
            numero_conta = len(contas) + 1 
            criar_conta(clientes, numero_conta, contas)
        elif opcao == 3:
            depositar(clientes)
        elif opcao == 4:
            sacar(clientes)
        elif opcao == 5:
            exibir_extrato(clientes)
        elif opcao == 6:
            listar_contas(contas)
        elif opcao == 7:
            print("\nEncerrando o sistema. Obrigado por utilizar nossos serviços.")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Execução direta
if __name__ == "__main__":
    main()
