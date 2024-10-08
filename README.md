## Descrição do Código:

Este código implementa um sistema bancário simples que permite ao usuário realizar 5 operações principais: depositar, sacar e ver o extrato da conta. Essas operações só podem ser realizadas se o cpf informado já estiver vinculado a um usuário e uma conta.  Ele opera com a moeda base em Reais (R$) e estabelece regras claras para as transações de saque, limitando a quantidade diária que pode ser sacada, bem como o número máximo de saques permitidos por dia.

## Funcionalidades:
# Depósito:
O usuário pode adicionar fundos à sua conta. O valor do depósito é somado ao saldo atual, e a transação é registrada no extrato bancário.

# Saque:
O saque possui duas restrições principais para segurança e controle financeiro:

Limite diário de saque: o usuário pode sacar no máximo R$ 500,00 por dia.
Limite de saques por dia: o usuário pode realizar no máximo 3 saques por dia.
Se o usuário tentar exceder qualquer um desses limites, o saque será negado. Cada saque aprovado é subtraído do saldo e registrado no extrato bancário.
# Ver Extrato:
O usuário pode visualizar um histórico de todas as transações (depósitos e saques) realizadas. O extrato exibe todas as operações e o saldo final da conta. Além de informar a data e os horários de cada operação.

# Criar Usuário:
O usuário pode criar seu usuário adicionando suas informações pessoais (cpf, nome, data de nascimento, endereço).

# Criar uma conta 
O usuário pode criar sua conta vinculada a um cpf já existente.

# Regras:
O sistema não permite que as operações depositar, sacar, ver extrato sejam realizadas sem já possuir um cpf cadastrado a um usuário e uma conta vinculada a esse cpf.
O sistema bloqueia qualquer tentativa de saque se o saldo disponível for insuficiente.
O saque diário máximo de R$ 500,00 e o limite de até 3 saques por dia garantem um controle rigoroso sobre as retiradas de dinheiro.
O limite maximo de operações (saque, deposito) é de 10 operações. Caso o usário tentar realizar mais que essa quantidade será informado que execedeu o número de operações.
