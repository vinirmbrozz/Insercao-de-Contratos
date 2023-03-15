import json
from urllib import response
import requests
import psycopg2
from requests.auth import HTTPBasicAuth
import sys
import dotenv
import os
dotenv.load_dotenv()
from validate_docbr import CPF, CNPJ
from sqlalchemy import false, true
import numpy as np


def main():
  valorEntrada = sys.argv[1:]
  cpf = CPF()
  cnpj = CNPJ()
  try:
    for entrada in valorEntrada:
      if np.isinteger(entrada) and cpf.validate(entrada):
        print('CPF: ' + str(entrada))
        pegarIdCliente = consultaClienteViaCPF(entrada.replace('.','').replace('-', ''))
        pegarIdContrato = filtrarContratoPorID(pegarIdCliente)
        for idContrato in pegarIdContrato:
          webHookInsercao(idContrato)

      elif np.isinteger(entrada) and cnpj.validate(entrada):
          print('CNPJ: ' + str(entrada))
          pegarIdCliente = consultaClienteViaCNPJ(entrada.replace('.','').replace('/','').replace('-',''))
          pegarIdContrato = filtrarContratoPorID(pegarIdCliente)
          for idContrato in pegarIdContrato:
            webHookInsercao(idContrato)
      else:
        print('Entrada por ID: ' + str(entrada))
        pegarIdContrato = filtrarContratoPorID(entrada)
        for idContrato in pegarIdContrato:
          webHookInsercao(idContrato)
  except:
    print('Entrada inválida')
def consultaClienteViaCPF(cpf):
  url = str(os.environ['URL_API']) + str(os.environ['DOMINIO']) + str(os.environ['PARAMETRO_CUSTOMERS_CPF']) + str(cpf)
  response = requests.get(url, auth = HTTPBasicAuth(str(os.environ['USER']), str(os.environ['PASS'])))
  idCliente = 0
  if response.status_code == 200:
    dados = response.json()
    for result in dados['results']:
      idCliente = result['id']
  else:
    print(response.status_code)
  return idCliente


def consultaClienteViaCNPJ(cnpj):
  url = str(os.environ['URL_API']) + str(os.environ['DOMINIO']) + str(os.environ['PARAMETRO_CUSTOMERS_CNPJ']) + str(cnpj)
  response = requests.get(url, auth = HTTPBasicAuth(str(os.environ['USER']), str(os.environ['PASS'])))
  idCliente = 0
  if response.status_code == 200:
    dados = response.json()
    for result in dados['results']:
      idCliente = result['id']
  else:
    print(response.status_code)
  return idCliente


def filtrarContratoPorID(idCliente):
  url = str(os.environ['URL_API']) + str(os.environ['DOMINIO']) + str(os.environ['PARAMETRO_SALES_CONTRACTS']) + str(idCliente)
  response = requests.get(url, auth = HTTPBasicAuth(str(os.environ['USER']), str(os.environ['PASS'])))
  if response.status_code == 200:
    json = response.json()
    retornoIds = []
    for result in json['results']:
      enterpriseId = result['enterpriseId']
      if len(str(enterpriseId)) > 3:
        continue
      else:
        idContrato = result['id']
        retornoIds.append(idContrato)
    return retornoIds
      
def webHookInsercao(idContrato):
  print(idContrato)
  url = str(os.environ['URL_WEBHOOK'])
  payload = {'salesContractId' : idContrato}
  headers = {'Content-type': 'application/json'}

  response = requests.request('POST', url, json=payload, headers=headers)

  print(response.content)

  if response.status_code == 201:
    return true
  else:
    return false

if __name__ == "__main__":
  main()