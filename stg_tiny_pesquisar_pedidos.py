import json
import requests
import mysql.connector
from datetime import datetime, timedelta, date, timezone
#import time

# [START variables]
url = "https://api.tiny.com.br/api2/pedidos.pesquisa.php"
db_connection = mysql.connector.connect(
    host="dbvidevino.crw80yxmagti.us-east-1.rds.amazonaws.com", 
    user="admin", 
    passwd="z38dywYK6ukUE5T", 
    database="dbvidevino")
data_inicio = date.today().strftime("%d/%m/%Y")
data_fim = data_inicio
## Reprocessamento
#data_inicio = '01/07/2022'
#data_fim = '06/07/2022'
# [END variables]

def check_order(db_connection, dt_order_start, dt_order_end):
    cursor = db_connection.cursor()
    cursor.execute(f"""select distinct id_order from `dbvidevino`.`stg_tiny_pesquisar_pedidos` where dt_order between '{dt_order_start}' and '{dt_order_end}'""")
    result = cursor.fetchall()
    list_order = []
    for row in result:
        list_order.append(row[0])
    #print(list_order)
    return list_order

def inserted_order(db_connection, id_seq_store, id_order, dt_order):    
    cursor = db_connection.cursor()
    sql = "INSERT INTO stg_tiny_pesquisar_pedidos (id_seq_store, id_order, dt_order, dt_inserted) VALUES (%s, %s, %s, sysdate())"
    values = (id_seq_store, id_order, dt_order)
    try:
        cursor.execute(sql, values)
        cursor.close()
        db_connection.commit()
        print(f'+    -- Pedido inserido com sucesso! Pedido: {id_order} data: {dt_order}')
    except Exception as e:
        if str(e).find("Duplicate") != -1:
            print(f'+    -- Pedido já existe {id_order} data: {dt_order}')
    

def check_page_number(db_connection, data_inicio, data_fim, url, token, id_seq_store):
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++')
    print(f'+  - Loja: {id_seq_store}')
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
        ## Recuperando pedidos já carregado
        dt_order_start = datetime.strptime(data_inicio, '%d/%m/%Y').date().strftime("%Y-%m-%d")
        dt_order_end = datetime.strptime(data_fim, '%d/%m/%Y').date().strftime("%Y-%m-%d")
        list_order = check_order(db_connection, dt_order_start, dt_order_end)
        ##
        print('+  - Iniciando a Carga')
        list_pedidos = json_input['retorno']['pedidos']
        for i in range(0,len(list_pedidos)):
            id_seq_store = id_seq_store
            id_order = list_pedidos[i]['pedido']['id']
            dt_order = list_pedidos[i]['pedido']['data_pedido']
            dt_order = dt_order[6:10] +'-'+ dt_order[3:5] +'-'+ dt_order[:2]+' '+ dt_order[11:]
            ## INSERT
            if len(list_order) <= 0:
                inserted_order(db_connection, id_seq_store, id_order, dt_order)
            else:
                if int(id_order) in list_order:
                    print(f'+    -- Pedido já existe {id_order} data: {dt_order}')
                else:
                    inserted_order(db_connection, id_seq_store, id_order, dt_order)
    db_connection.close()

if __name__ == "__main__":
    token = ''
    for loja in range(1,4):
        if loja == 1:
            token = ''
            id_seq_store = 1
        elif loja == 2:
            token = '1bb7c94a11a1ba7a41d972fd70d5fe686e8f59e1'
            id_seq_store = 2
        elif loja == 3:
            token = ''
            id_seq_store = 3
        if token != '':
            check_page_number(db_connection, data_inicio, data_fim, url, token, id_seq_store)
    
    
    