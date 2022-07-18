import json
import requests
import time
import sys
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
        #for i in range(0,qtd):
        orderId = json_input['retorno']['pedido']['id']
        customerId = json_input['retorno']['pedido']['cliente']['cpf_cnpj']
        customerId = customerId
        orderCode = json_input['retorno']['pedido']['numero_ordem_compra']
        subTotal = json_input['retorno']['pedido']['total_produtos']
        deliveryFee = json_input['retorno']['pedido']['valor_frete']
        benefits = json_input['retorno']['pedido']['valor_desconto']
        orderAmount = json_input['retorno']['pedido']['total_pedido']

        ## INSERT
        db_connection = mysql.connector.connect(
            host="dbvidevino.crw80yxmagti.us-east-1.rds.amazonaws.com", 
            user="admin", 
            passwd="z38dywYK6ukUE5T", 
            database="dbvidevino"
        )
        cursor = db_connection.cursor()
        sql = "INSERT INTO tiny_orders_detail (orderId, customerId, orderCode, subTotal, deliveryFee, benefits, orderAmount) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        values = (orderId, customerId, orderCode, subTotal, deliveryFee, benefits, orderAmount)
        try:
            cursor.execute(sql, values)
            cursor.close()
            db_connection.commit()
            print(f'+    -- Pedido inserido com sucesso! Pedido: {orderId}')
        except Exception as e:
            if str(e).find("Duplicate") != -1:
                print(f'+    -- Pedido já existe {orderId}')
            else:
                print(f'Erro: {str(e)}')
        db_connection.close()


if __name__ == "__main__":
    loja = int(sys.argv[1])
    if loja == 3:
        token = '82f18bdb6d897adb0755910892851be9a10e469e'
        id_seq_loja = 3
    elif loja == 4:
        token = '09cb1e55dcf4fe3e5e778759cbbc7ce7f103d9fb'
        id_seq_loja = 4
    elif loja == 5:
        token = '0a37316c1ebd827b50a2d166c9f63ecb14f72529'
        id_seq_loja = 5

    check_page_number(url, token, id_seq_loja)
