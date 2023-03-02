import json
from urllib import response
import requests
import psycopg2
from requests.auth import HTTPBasicAuth
import sys
import dotenv
import os
dotenv.load_dotenv()

from sqlalchemy import false, true

def main():
  cpf = ['355.187.741-68']
  for CPF in cpf:
    pegarIdCliente = consultaClienteAPI(CPF.replace('.','').replace('-', ''))
    pegarIdContrato = filtrarContratoPorID(pegarIdCliente)
    for idContrato in pegarIdContrato:
      webHookInsercao(idContrato)

def consultaClienteAPI(cpf):
  url = 'https://api.sienge.com.br/' + str(os.environ['DOMINIO_WPA']) +'/public/api/v1/customers?cpf=' + str(cpf)
  response = requests.get(url, auth = HTTPBasicAuth(str(os.environ['USER_WPA']), str(os.environ['PASS_WPA'])))
  idCliente = 0
  if response.status_code == 200:
    dados = response.json()
    for result in dados['results']:
      idCliente = result['id']
  else:
    print(response.status_code)
  return idCliente



def filtrarContratoPorID(idCliente):
  url = 'https://api.sienge.com.br/' + str(os.environ['DOMINIO_WPA']) + '/public/api/v1/sales-contracts?customerId=' + str(idCliente)
  response = requests.get(url, auth = HTTPBasicAuth(str(os.environ['USER_WPA']), str(os.environ['PASS_WPA'])))
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
  url = str(os.environ['URL_WEBHOOK'])
  payload = {'salesContractId' : idContrato}
  headers = {'Content-type': 'application/json'}

  response = requests.request('POST', url, json=payload, headers=headers)

  if response.status_code == 201:
    return true
  else:
    return false

if __name__ == "__main__":
  main()