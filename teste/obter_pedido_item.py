import json
import requests
#import time
#import sys
import mysql.connector
from datetime import datetime, timedelta, date, timezone

# [START variables]
url = "https://api.tiny.com.br/api2/pedido.obter.php"
# [END variables]

def check_page_number(url, token, id_seq_loja):
    db_connection = mysql.connector.connect(
        host="dbvidevino.crw80yxmagti.us-east-1.rds.amazonaws.com", 
        user="admin", 
        passwd="z38dywYK6ukUE5T", 
        database="dbvidevino"
    )
    cursor = db_connection.cursor()
    cursor.execute("select distinct orderId from `dbvidevino`.`tiny_orders`")
    result = cursor.fetchall()
    for row in result:
        params = {
            "token" : token,
            "formato" : 'json',
            "id": row[0]
        }

        response = requests.request("POST", url, params=params)
        json_input = response.json()
        #print(json_input)
        qtd = len(json_input['retorno']['pedido']['itens'])
        for i in range(0,qtd):
            orderId = json_input['retorno']['pedido']['id']
            itens = json_input['retorno']['pedido']['itens']
            itemsId = itens[i]['item']['id_produto']
            quantify = itens[i]['item']['quantidade']
            unitPrice = itens[i]['item']['valor_unitario']            
            ## INSERT
            db_connection = mysql.connector.connect(
                host="dbvidevino.crw80yxmagti.us-east-1.rds.amazonaws.com", 
                user="admin", 
                passwd="z38dywYK6ukUE5T", 
                database="dbvidevino"
            )
            cursor = db_connection.cursor()
            sql = "INSERT INTO tiny_orders_items (orderId, itemsId, quantify, unitPrice) VALUES (%s,%s,%s,%s)"
            values = (orderId, itemsId, quantify, unitPrice)
            #cursor.execute(sql, values)
            #cursor.close()
            #db_connection.commit()
            
            #"""
            try:
                cursor.execute(sql, values)
                cursor.close()
                db_connection.commit()
                print(f'+    -- Pedido inserido com sucesso! Pedido: {orderId} Item: {itemsId}')
            except Exception as e:
                if str(e).find("Duplicate") != -1:
                    print(f'+    -- Pedido já existe {orderId} Item: {itemsId}')
                else:
                    print(f'Erro: {str(e)}')
        #"""
            db_connection.close()


if __name__ == "__main__":
    loja = int(sys.argv[1])
    if loja == 1:
        token = ''
        id_seq_loja = 1
    elif loja == 2:
        token = '1bb7c94a11a1ba7a41d972fd70d5fe686e8f59e1'
        id_seq_loja = 2
    elif loja == 3:
        token = ''
        id_seq_loja = 3

    check_page_number(url, token, id_seq_loja)
