from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap

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
            if super().sacar(valor_saque):  # Verifica se o saque foi bem-sucedido
                saque = Saque(valor_saque)  # Cria uma nova transação de saque
                self.historico.adicionar_transacao(saque)  # Adiciona a transação ao histórico
        
        return False
    
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
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
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

# Agora você pode usar o método exibir_extrato para mostrar as transações
def exibir_extrato(clientes):
    cpf = input("Informe o seu CPF (somente números): ")
    cliente = verificar_cpf_existe(cpf, clientes)

    if not cliente:
        print("\nCPF não encontrado. Por favor, crie o usuário primeiro (opção 1).")
        return

    conta = recuperar_conta_cliente(cliente)
    if conta:
        conta.historico.exibir_extrato()

# Exemplo de como chamar o método mostrar_extrato
# mostrar_extrato(clientes)

def verificar_cpf_existe(cpf, clientes):
    
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    
    if clientes_filtrados:
        return clientes_filtrados[0]  # Retorna o primeiro cliente encontrado
    
    return None

def main():
    clientes = []
    contas = []
    menu = '''\n 
                ====== Escolha uma Operação ======
                [1] \tCriar Usuário
                [2] \tCriar Conta
                [3] \tDepositar
                [4] \tSacar
                [5] \tExtrato
                [6] \tListar Conta
                [7] \tSair
                ==================================\n
                ''' 

    while True:
        operação = int(input(menu))
        
        if  operação == 1:
            criar_cliente(clientes)
        
        elif operação == 2:
            numero_conta = len(contas) + 1 
            criar_conta(clientes, numero_conta, contas)
        
        elif operação == 3:
            depositar(clientes)
        
        elif operação == 4:
            sacar(clientes)
        
        elif operação == 5:
            exibir_extrato(clientes)
        
        elif operação == 6:
            listar_contas(contas) 
        
        elif operação == 7:
            break

        else: 
            print("""Operação inválida!! 
            Selecione uma operação Válida.
            """) 


print(main())
