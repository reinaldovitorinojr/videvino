import json
import requests
import time
from datetime import datetime, timedelta, date, timezone
import mysql.connector

# [START variables]
token = '1bb7c94a11a1ba7a41d972fd70d5fe686e8f59e1'
url = "https://api.tiny.com.br/api2/contatos.pesquisa.php"


print('==================================')

# [END variables]

def create_id_execution():
    id = int(round(time.time() * 1000))
    return id

def get_updated_at():
    now = datetime.now(timezone("America/Sao_Paulo"))
    return datetime.strftime(now, "%Y-%m-%d %H:%M:%S")

def check_page_number(url, token):
    params = {
        "token" : token,
        "formato" : 'json',
        "situacao" : 'Ativo',
        "dataMinimaAtualizacao" : '04/01/2022 23:59:59'
    }

    response = requests.request("POST", url, params=params)
    json_input = response.json()
    
    status_processamento = json_input['retorno']['status_processamento']
    if status_processamento == '2':
        print('Erro no processmento ou não existe dados.')
    elif status_processamento == '3':
        print('Iniciando a Carga')
        qtd = len(json_input['retorno']['contatos'])
        itens = json_input['retorno']['contatos']
        for i in range(0,qtd):
            cpf_cnpj = itens[i]['contato']['cpf_cnpj']
            if cpf_cnpj != None and cpf_cnpj != '' and cpf_cnpj != 'None':
                id_cliente = int(cpf_cnpj.replace('.','').replace('-','').replace('/',''))
            else:
                id_cliente = -1
            codigo = itens[i]['contato']['id']            
            nome = itens[i]['contato']['nome'] 
            if nome != None and nome != '' and nome != 'None':
                nome = (itens[i]['contato']['nome']).title()
            tipo_pessoa = itens[i]['contato']['tipo_pessoa']
            endereco = itens[i]['contato']['endereco']
            if endereco != None and endereco != '' and endereco != 'None':
                endereco = (itens[i]['contato']['endereco']).title()
            numero = itens[i]['contato']['numero']
            complemento = itens[i]['contato']['complemento']
            if complemento != None and complemento != '' and complemento != 'None':
                complemento = (itens[i]['contato']['complemento']).title()
            bairro = itens[i]['contato']['bairro']
            if bairro != None and bairro != '' and bairro != 'None':
                bairro = (itens[i]['contato']['bairro']).title()
            cep = itens[i]['contato']['cep']
            if cep != None and cep != '' and cep != 'None':
                cep = (itens[i]['contato']['cep']).title()
            cidade = itens[i]['contato']['cidade']
            if cidade != None and cidade != '' and cidade != 'None':
                cidade = (itens[i]['contato']['cidade']).title()
            uf = itens[i]['contato']['uf']
            if uf != None and uf != '' and uf != 'None':
                uf = (itens[i]['contato']['uf']).title()
            situacao = itens[i]['contato']['situacao']
            data_criacao = itens[i]['contato']['data_criacao']
            data_criacao = data_criacao[6:10] +'-'+ data_criacao[3:5] +'-'+ data_criacao[:2]+' '+ data_criacao[11:]
            #print(id_cliente, codigo, nome, tipo_pessoa, cpf_cnpj, endereco, numero, complemento, bairro, cep, cidade, uf, situacao, data_criacao)
            ## INSERT
            #"""
            db_connection = mysql.connector.connect(host="dbvidevino.crw80yxmagti.us-east-1.rds.amazonaws.com", user="admin", passwd="z38dywYK6ukUE5T", database="dbvidevino")
            cursor = db_connection.cursor()
            sql = "INSERT INTO `dbvidevino`.`tb_cliente` (id_cliente, codigo, nome, tipo_pessoa, cpf_cnpj, endereco, numero, complemento, bairro, cep, cidade, uf, situacao, data_criacao, dt_insert) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, sysdate())"
            values = (id_cliente, codigo, nome, tipo_pessoa, cpf_cnpj, endereco, numero, complemento, bairro, cep, cidade, uf, situacao, data_criacao)
            try:
                cursor.execute(sql, values)
                cursor.close()
                db_connection.commit()
                print(f'Contato inserido com sucesso! {id_cliente}')
            except Exception as e:
                if str(e).find("Duplicate") != -1:
                    print(f'id_cliente já existe {id_cliente}')
            db_connection.close()
            #"""
    
check_page_number(url, token)
