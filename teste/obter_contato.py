import json
import requests
import time
from datetime import datetime, timedelta, date, timezone
import mysql.connector

# [START variables]
token = '1bb7c94a11a1ba7a41d972fd70d5fe686e8f59e1'
url = "https://api.tiny.com.br/api2/contato.obter.php"

#data_inicio = str(date.today() - timedelta(days=3))
#data_fim = data_inicio
data_inicio = '01/06/2022'
data_fim = '01/06/2022'
print('==================================')
print(f'Data Inicio: {str(data_inicio)}  Data Fim: {str(data_fim)}')

# [END variables]

def create_id_execution():
    id = int(round(time.time() * 1000))
    return id

def get_updated_at():
    now = datetime.now(timezone("America/Sao_Paulo"))
    return datetime.strftime(now, "%Y-%m-%d %H:%M:%S")

def check_page_number(data_inicio, data_fim, url, token):
    params = {
        "token" : token,
        "formato" : 'json',
        "id": 687050754
    }

    response = requests.request("POST", url, params=params)
    json_input = response.json()
    print(json_input)
    qtd = len(json_input['retorno']['pedido']['itens'])
    for i in range(0,qtd):
        id = json_input['retorno']['pedido']['id']
        numero = json_input['retorno']['pedido']['numero']
        data_pedido = json_input['retorno']['pedido']['data_pedido']
        data_pedido = data_pedido[6:10] + '-' + data_pedido[3:5] + '-' + data_pedido[:2]
        #print(data_pedido)
        
        valor_frete = json_input['retorno']['pedido']['valor_frete']
        valor_desconto = json_input['retorno']['pedido']['valor_desconto']
        outras_despesas = json_input['retorno']['pedido']['outras_despesas']
        total_produtos = json_input['retorno']['pedido']['total_produtos']
        total_pedido = json_input['retorno']['pedido']['total_pedido']
        numero_ordem_compra = json_input['retorno']['pedido']['numero_ordem_compra']
        situacao = json_input['retorno']['pedido']['situacao']

        cliente_nome = json_input['retorno']['pedido']['cliente']['nome']
        cliente_codigo = json_input['retorno']['pedido']['cliente']['codigo']
        cliente_cpf_cnpj = json_input['retorno']['pedido']['cliente']['cpf_cnpj']
        cliente_endereco = json_input['retorno']['pedido']['cliente']['endereco']
        cliente_numero = json_input['retorno']['pedido']['cliente']['numero']
        cliente_complemento = json_input['retorno']['pedido']['cliente']['complemento']
        cliente_bairro = json_input['retorno']['pedido']['cliente']['bairro']
        cliente_cidade = json_input['retorno']['pedido']['cliente']['cidade']
        cliente_uf = json_input['retorno']['pedido']['cliente']['uf']
        cliente_cep = json_input['retorno']['pedido']['cliente']['cep']
        
        itens = json_input['retorno']['pedido']['itens']
        item_id_produto = itens[i]['item']['id_produto']
        item_codigo = itens[i]['item']['codigo']
        item_descricao = itens[i]['item']['descricao']
        item_quantidade = itens[i]['item']['quantidade']
        item_valor_unitario = itens[i]['item']['valor_unitario']
        
        ## INSERT
        """
        db_connection = mysql.connector.connect(host="dbvidevino.crw80yxmagti.us-east-1.rds.amazonaws.com", user="admin", passwd="z38dywYK6ukUE5T", database="dbvidevino")
        cursor = db_connection.cursor()
        sql = "INSERT INTO tb_vendas (id,numero,data_pedido,cliente_nome,cliente_codigo,cliente_cpf_cnpj,cliente_endereco,cliente_numero,cliente_complemento,cliente_bairro,cliente_cidade,cliente_uf,cliente_cep,valor_frete,valor_desconto,outras_despesas,total_produtos,total_pedido,numero_ordem_compra,situacao,item_id_produto,item_codigo,item_descricao,item_quantidade,item_valor_unitario) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (id,numero,data_pedido,cliente_nome,cliente_codigo,cliente_cpf_cnpj,cliente_endereco,cliente_numero,cliente_complemento,cliente_bairro,cliente_cidade,cliente_uf,cliente_cep,valor_frete,valor_desconto,outras_despesas,total_produtos,total_pedido,numero_ordem_compra,situacao,item_id_produto,item_codigo,item_descricao,item_quantidade,item_valor_unitario)
        cursor.execute(sql, values)
        cursor.close()
        db_connection.commit()
        db_connection.close()
        """
        print(f'Pedido: {id} - {item_descricao} carregado!')
        
check_page_number(data_inicio, data_fim, url, token)
