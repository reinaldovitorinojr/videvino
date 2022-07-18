import json
import requests
import time
import mysql.connector
from datetime import datetime, timedelta, date, timezone
from utils.functions import check_page_number

# [START variables]
token = '1bb7c94a11a1ba7a41d972fd70d5fe686e8f59e1'
url = "https://api.tiny.com.br/api2/produtos.pesquisa.php"
params = {
    "token" : token,
    "formato" : 'json',
    "pesquisa":'',
    "pagina": 1
}
# [END variables]

        
def loaded_page(url, token, params):
    page_number = check_page_number(url, token, params)
    status_processamento = page_number[0]
    numero_paginas = page_number[1] +1
    json_input = page_number[2]
    for j in range(1,numero_paginas):
        print('+++++++++++++++++++++++++++++')
        print(f'+  Paginas: {j}/{numero_paginas-1}')
        if j <= 1:
            qtd = len(json_input['retorno']['produtos'])
            itens = json_input['retorno']['produtos']
            loaded_table(qtd, itens, json_input)
        else:
            params = {
                "token" : token,
                "formato" : 'json',
                "pesquisa":'',
                "pagina": j
            }
            page_number = check_page_number(url, token, params)
            json_input = page_number[2]
            qtd = len(json_input['retorno']['produtos'])
            itens = json_input['retorno']['produtos']
            loaded_table(qtd, itens, json_input)

def loaded_table (qtd, itens, json_input):
    for i in range(0,qtd):
        codigo = itens[i]['produto']['id']
        id = itens[i]['produto']['codigo']
        if id != None and id != '' and id != 'None':
            id_produto = int(itens[i]['produto']['codigo'])
        else:
            id_produto = int(itens[i]['produto']['id'])
        nome = itens[i]['produto']['nome']
        preco = itens[i]['produto']['preco']
        preco_promocional = itens[i]['produto']['preco_promocional']
        unidade = itens[i]['produto']['unidade']
        gtin = itens[i]['produto']['gtin']
        tipo_variacao = itens[i]['produto']['tipoVariacao']
        localizacao = itens[i]['produto']['localizacao']
        preco_custo = itens[i]['produto']['preco_custo']
        preco_custo_medio = itens[i]['produto']['preco_custo_medio']
        situacao = itens[i]['produto']['situacao']
        ## INSERT
        #"""
        db_connection = mysql.connector.connect(host="dbvidevino.crw80yxmagti.us-east-1.rds.amazonaws.com", user="admin", passwd="z38dywYK6ukUE5T", database="dbvidevino")
        cursor = db_connection.cursor()
        sql = "INSERT INTO `dbvidevino`.`tb_produto` (id_produto, codigo, nome, preco, preco_promocional, unidade, gtin, tipo_variacao, localizacao, preco_custo, preco_custo_medio, situacao, dt_insert) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, sysdate())"
        values = (id_produto, codigo, nome, preco, preco_promocional, unidade, gtin, tipo_variacao, localizacao, preco_custo, preco_custo_medio, situacao)
        try:
            cursor.execute(sql, values)
            cursor.close()
            db_connection.commit()
            print(f'+    -- Produto inserido com sucesso! {id_produto}')
        except Exception as e:
            if str(e).find("Duplicate") != -1:
                print(f'+    -- id_produto já existe {id_produto}')
        db_connection.close()
        #"""


loaded_page(url, token, params)
