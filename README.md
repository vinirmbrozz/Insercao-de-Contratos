# Inserção de Contrato

## Descrição do Projeto

<p align="center">Este código é um script Python que realiza uma integração com a API do sistema Sienge. O objetivo do script é consultar um cliente por CPF/CNPJ na API do Sienge, filtrar os contratos deste cliente e enviar uma mensagem de webhook para uma URL específica para cada contrato encontrado.</p>

## 🎲 API's consumidas no Projeto

- GET /customers -> Busca por CPF
- GET /customers -> Busca por CNPJ
- GET /sales-contracts -> Busca de contrato através do ID do Cliente
- POST /whcontractcancela -> Insere um contrato

## 🛠 Tecnologias

As seguintes ferramentas foram usadas na construção do projeto:

- Python
- API REST

## ➕ Sobre 

<p align="left">O objetivo da criação desse script foi para automatizar uma busca manual, que ocupava tempo. Ele funciona consultando pelo CPF/CNPJ do cliente via API para trazer o ID do mesmo ou diretamente pelo Id do cliente caso ja o tenha. Com o ID do cliente em mãos, conseguimos encontrar todos os contratos de vendas atrelados a ele e subí-los através do webhook para uma fila no banco de dados. O programa recebe os valores de entrada (CPF/CNPJ/ID) via linha de comando e insere todos numa lista. Com um laço de repetição, o script percorre a lista toda garantindo que a entrada seja um número inteiro e valida o CPF e o CNPJ.</p>

