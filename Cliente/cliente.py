import socket
ip = 'localhost'
port = 8000
addr = ((ip,port))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(addr)

while True:
    try:
        mensagem = input('Digite uma mensagem para enviar ao servidor: ')
        client_socket.send(mensagem.encode())
        print('Mensagem enviada')
        recebe = client_socket.recv(1024).decode()
        print('Mensagem recebida: '+ recebe)
        if recebe == "TCHAU":
            client_socket.close()
            break
    except:
        client_socket.close()