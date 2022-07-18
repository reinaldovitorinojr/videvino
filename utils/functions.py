import json
import requests
import mysql.connector
from datetime import datetime, timedelta, date, timezone

# [START variables]
token = '1bb7c94a11a1ba7a41d972fd70d5fe686e8f59e1'
host = 'dbvidevino.crw80yxmagti.us-east-1.rds.amazonaws.com'
user = 'admin'
password = 'z38dywYK6ukUE5T'
database = 'dbvidevino'
# [END variables]

def create_id_execution():
    id = int(round(time.time() * 1000))
    return id

def get_updated_at():
    now = datetime.now(timezone("America/Sao_Paulo"))
    return datetime.strftime(now, "%Y-%m-%d %H:%M:%S")

def check_page_number(url, token, params):
    numero_paginas = ''
    response = requests.request("POST", url, params=params)
    json_input = response.json()
    status_processamento = json_input['retorno']['status_processamento']
    if status_processamento == '2':
        print('Erro no processmento ou não existe dados.')
    elif status_processamento == '3':
        numero_paginas = json_input['retorno']['numero_paginas']
    return status_processamento, numero_paginas, json_input


def check_create_table(host, user, password, database):
    db_connection = mysql.connector.connect(host=host, user=user, passwd=password, database=database)
    cursor = db_connection.cursor()
    
    sql = """
    CREATE TABLE IF NOT EXISTS `dbvidevino`.`tb_vendas` (
		`id` bigint(20) NOT NULL,
		`numero` bigint(20) NULL,
		`data_pedido` date DEFAULT NULL,
		`cliente_nome` varchar(50) NULL,
		`cliente_codigo` varchar(50) NULL,
		`cliente_cpf_cnpj` varchar(18) NULL,
		`cliente_endereco` varchar(80) NULL,
		`cliente_numero` varchar(10) NULL,
		`cliente_complemento` varchar(50) NULL,
		`cliente_bairro` varchar(50) NULL,
		`cliente_cidade` varchar(50) NULL,
		`cliente_uf` varchar(50) NULL,
		`cliente_cep` varchar(10) NULL,
		`valor_frete` decimal NULL,
		`valor_desconto` decimal NULL,
		`outras_despesas` decimal NULL,
		`total_produtos` decimal NULL,
		`total_pedido` decimal NULL,
		`numero_ordem_compra` varchar(10) NULL,
		`situacao` varchar(15) NULL,
		`item_id_produto` int NOT NULL,
		`item_codigo` varchar(20) NULL,
		`item_descricao` varchar(150) NULL,
		`item_quantidade` decimal NULL,
		`item_valor_unitario` decimal NULL,
	PRIMARY KEY (`id`,`item_id_produto`)
)"""
    try:
        cursor.execute(sql)
        cursor.close()
        print('Tabela Criada com sucesso!')
    except:
        print('erro')
    db_connection.commit()
    db_connection.close()


check_create_table(host, user, password, database)