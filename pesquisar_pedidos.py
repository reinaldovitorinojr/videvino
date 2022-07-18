import requests
import mysql.connector

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
        #print(list_pedidos)
        
        for i in range(0,len(list_pedidos)):
            id_seq_loja = id_seq_loja
            orderCode = list_pedidos[i]['pedido']['id']
            orderData = list_pedidos[i]['pedido']['data_pedido']
            orderData = orderData[6:10] +'-'+ orderData[3:5] +'-'+ orderData[:2]+' '+ orderData[11:]
            orderAmount = list_pedidos[i]['pedido']['valor']
            status = list_pedidos[i]['pedido']['situacao']
            print(orderCode, orderData, orderAmount, status)
            ## INSERT
            #"""
            db_connection = mysql.connector.connect(host="dbvidevino.crw80yxmagti.us-east-1.rds.amazonaws.com", user="admin", passwd="z38dywYK6ukUE5T", database="dbvidevino")
            cursor = db_connection.cursor()
            sql = "INSERT INTO tiny_orders (orderCode, orderData, orderAmount, status) VALUES (%s, %s, %s, %s)"
            values = (orderCode, orderData, orderAmount, status)
            try:
                cursor.execute(sql, values)
                cursor.close()
                db_connection.commit()
                print(f'+    -- Pedido inserido com sucesso! Pedido: {orderCode} data: {orderData}')
            except Exception as e:
                if str(e).find("Duplicate") != -1:
                    print(f'+    -- Pedido já existe {orderCode} data: {orderData}')
            db_connection.close()
            #"""

if __name__ == "__main__":
    token = ''
    for loja in range(1,6):
        if loja == 3:
            token = '82f18bdb6d897adb0755910892851be9a10e469e'
            id_seq_loja = 3
        elif loja == 4:
            token = '09cb1e55dcf4fe3e5e778759cbbc7ce7f103d9fb'
            id_seq_loja = 4
        elif loja == 5:
            token = '0a37316c1ebd827b50a2d166c9f63ecb14f72529'
            id_seq_loja = 5
        #data_inicio = date.today().strftime("%d/%m/%Y")
        #data_fim = data_inicio
        data_inicio = '01/03/2022'
        data_fim = '31/03/2022'
        if token != '':
            check_page_number(data_inicio, data_fim, url, token, id_seq_loja)