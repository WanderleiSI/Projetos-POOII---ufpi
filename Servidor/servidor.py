import socket
host = ''#Aceita requisições de outras máquinas, localhost permite apenas a máquina local
port = 8000
addr = (host,port)
serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.bind(addr)
serv_socket.listen(10)
print('Aguardando conexao...')
con, cliente = serv_socket.accept()
print('Conectado')
print('Aguardando mensagens...')

while True:
    try:
        recebe = con.recv(1024)
        print('Mensagem reccebida: ' + recebe.decode())
        if recebe.decode() == 'TCHAU':
            #print("Entrei no if")
            enviar = "TCHAU"

            con.send(enviar.encode())
            print('enviou')
            serv_socket.close()
            break
        else:
            #print("Entrei no else")
            enviar = input('Digite uma mensagem para enviar ao cliente: ')
            if enviar == "TCHAU":
                con.send(enviar.encode())
                serv_socket.close()  
                break
            else:
                con.send(enviar.encode())
    except:
        serv_socket.close()
        break