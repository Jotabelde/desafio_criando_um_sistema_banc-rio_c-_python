# 💼 Sistema Bancário em Python

Este é um projeto de terminal que simula um sistema bancário simples, com suporte a **clientes**, **contas** e **transações**, como **saques** e **depósitos**. O sistema também realiza o **registro e persistência de dados** em um arquivo `.csv`.

---

## 🧩 Funcionalidades

- ✅ Cadastro de cliente (Pessoa Física)
- ✅ Criação de conta corrente
- ✅ Depósito com validação de valor
- ✅ Saque com limite de valor e quantidade diária
- ✅ Emissão de extrato com histórico de transações
- ✅ Listagem de contas cadastradas
- ✅ Salvamento automático de todas as transações em arquivo `.csv`
- ✅ Carregamento de dados históricos ao iniciar o programa

---

## 🗃️ Estrutura de Classes

- `Cliente` (classe base)
- `Pessoa_Fisíca` (herda de `Cliente`)
- `Conta` (classe base)
- `Conta_Corrente` (herda de `Conta`)
- `Transacao` (classe abstrata)
  - `Saque`
  - `Deposito`
- `Historico` (registra todas as transações da conta)

---

## 💾 Persistência de Dados

- As transações são salvas no arquivo `transacoes.csv` no caminho


- Ao iniciar o programa, os dados do CSV são carregados automaticamente e recriam as instâncias de clientes, contas e seus históricos.

---

## 🏁 Execução

1. Verifique se o caminho do arquivo CSV (`caminho_da_pasta`) está correto no início do script.
2. Execute o programa com:

 ```bash
 python seu_arquivo.py



