from audioop import add
import socket
ip = input('Digite o ip de conexao: ')
port = 7001
#Troquei a porta de 8001 para 7001
name = input("Qual seu nome? ")
addr = ((ip,port))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(addr)
client_socket.send(name.encode())
while True:
    mensagem = input("Digite uma mensagame para enviar ao servidor: ")
    if mensagem == 'bye':
        client_socket.send(mensagem.encode())
        break
    client_socket.send(mensagem.encode())
    #recebida = client_socket.recv(1024).decode()
    #if recebida == 'bye':
        #client_socket.close()
    print(client_socket.recv(1024).decode())
    print('Mensagem enviada')

client_socket.close()