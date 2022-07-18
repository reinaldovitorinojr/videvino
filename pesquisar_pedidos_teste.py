import json
import requests
import time
import sys
import mysql.connector
from datetime import datetime, timedelta, date, timezone

# [START variables]
url = "https://api.tiny.com.br/api2/pedidos.pesquisa.php"
# [END variables]

def check_page_number(data_inicio, data_fim, url, token, id_seq_loja):
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++')
    print(f'+  - Loja: {id_seq_loja}')
    print(f'+  - Data Inicio: {str(data_inicio)}  Data Fim: {str(data_fim)}')
    params = {
        "token" : token,
        "formato" : 'json',
        "dataInicial": data_inicio,
        "dataFinal": data_fim
    }

    response = requests.request("POST", url, params=params)
    json_input = response.json()
    status_processamento = json_input['retorno']['status_processamento']
    if status_processamento == '2':
        print('+  - Erro no processmento ou não existe dados.')
    elif status_processamento == '3':
        print('+  - Iniciando a Carga')
        list_pedidos = json_input['retorno']['pedidos']
        for i in range(0,len(list_pedidos)):
            id_seq_loja = id_seq_loja
            id_pedido = list_pedidos[i]['pedido']['id']
            data_pedido = list_pedidos[i]['pedido']['data_pedido']
            data_pedido = data_pedido[6:10] +'-'+ data_pedido[3:5] +'-'+ data_pedido[:2]+' '+ data_pedido[11:]
            ## INSERT
            #"""
            db_connection = mysql.connector.connect(host="dbvidevino.crw80yxmagti.us-east-1.rds.amazonaws.com", user="admin", passwd="z38dywYK6ukUE5T", database="dbvidevino")
            cursor = db_connection.cursor()
            sql = "INSERT INTO tb_pedido (id_seq_loja, id_pedido, data_pedido, dt_insert) VALUES (%s, %s, %s, sysdate())"
            values = (id_seq_loja, id_pedido, data_pedido)
            try:
                cursor.execute(sql, values)
                cursor.close()
                db_connection.commit()
                print(f'+    -- Pedido inserido com sucesso! Pedido: {id_pedido} data: {data_pedido}')
            except Exception as e:
                if str(e).find("Duplicate") != -1:
                    print(f'+    -- Pedido já existe {id_pedido} data: {data_pedido}')
            db_connection.close()
            #"""

if __name__ == "__main__":
    token = ''
    for loja in range(1,4):
        if loja == 1:
            token = ''
            id_seq_loja = 1
        elif loja == 2:
            token = '1bb7c94a11a1ba7a41d972fd70d5fe686e8f59e1'
            id_seq_loja = 2
        elif loja == 3:
            token = ''
            id_seq_loja = 3    
        #data_inicio = date.today().strftime("%d/%m/%Y")
        #data_fim = data_inicio
        data_inicio = '07/06/2022'
        data_fim = '07/06/2022'
        if token != '':
            check_page_number(data_inicio, data_fim, url, token, id_seq_loja)