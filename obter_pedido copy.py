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
    cursor.execute("select distinct id_pedido from `dbvidevino`.`tb_pedido`")
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
            id_seq_loja = id_seq_loja
            id_pedido = json_input['retorno']['pedido']['id']
            data_pedido = json_input['retorno']['pedido']['data_pedido']
            data_pedido = data_pedido[6:10] + '-' + data_pedido[3:5] + '-' + data_pedido[:2]
            cliente_nome = json_input['retorno']['pedido']['cliente']['nome']
            cliente_cpf_cnpj = json_input['retorno']['pedido']['cliente']['cpf_cnpj']
            numero_ordem_compra = json_input['retorno']['pedido']['numero_ordem_compra']
            situacao = json_input['retorno']['pedido']['situacao']
            itens = json_input['retorno']['pedido']['itens']
            item_id_produto = itens[i]['item']['id_produto']
            item_codigo = itens[i]['item']['codigo']
            item_descricao = itens[i]['item']['descricao']
            item_quantidade = itens[i]['item']['quantidade']
            item_valor_unitario = itens[i]['item']['valor_unitario']
            valor_frete = json_input['retorno']['pedido']['valor_frete']
            valor_desconto = json_input['retorno']['pedido']['valor_desconto']
            outras_despesas = json_input['retorno']['pedido']['outras_despesas']
            total_produtos = json_input['retorno']['pedido']['total_produtos']
            total_pedido = json_input['retorno']['pedido']['total_pedido']            
                        
            ## INSERT
            db_connection = mysql.connector.connect(
                host="dbvidevino.crw80yxmagti.us-east-1.rds.amazonaws.com", 
                user="admin", 
                passwd="z38dywYK6ukUE5T", 
                database="dbvidevino"
            )
            cursor = db_connection.cursor()
            sql = "INSERT INTO tb_vendas (id_seq_loja,id_pedido,data_pedido,cliente_nome,cliente_cpf_cnpj,numero_ordem_compra,situacao,item_id_produto,item_codigo,item_descricao,item_quantidade,item_valor_unitario,valor_frete,valor_desconto,outras_despesas,total_produtos,total_pedido,dt_insert) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, sysdate())"
            values = (id_seq_loja,id_pedido,data_pedido,cliente_nome,cliente_cpf_cnpj,numero_ordem_compra,situacao,item_id_produto,item_codigo,item_descricao,item_quantidade,item_valor_unitario,valor_frete,valor_desconto,outras_despesas,total_produtos,total_pedido)
            try:
                cursor.execute(sql, values)
                cursor.close()
                db_connection.commit()
                print(f'+    -- Pedido inserido com sucesso! Pedido: {id_pedido} item: {item_descricao}')
            except Exception as e:
                if str(e).find("Duplicate") != -1:
                    print(f'+    -- Pedido já existe {id_pedido} item: {item_descricao}')
                else:
                    print(f'Erro: {str(e)}')
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
