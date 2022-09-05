import socket, threading

class ClienteThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.name = ''
        print("Nova conxao: ", clientAddress)

    def run(self):
        self.name = self.csocket.recv(1024).decode()
        print(self.name," se conectou")
        #print("Conectado de: ", clientAddress)
        msg = ''
        while True:
            data = self.csocket.recv(1024)
            msg = data.decode()
            if msg == 'bye':
                #self.csocket.send('bye'.encode())
                break
            print("From ", self.name + ": ",msg)
            #print("From cliente", clientAddress, msg)
            self.csocket.send(msg.encode())
        print("Cliente at ", clientAddress, " disconnected...")
if __name__ == '__main__':
    localhost = ''
    port = 7001
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    server.bind((localhost, port))
    print("Servidor iniciado!")
    print("Aguardando nova conexao...")
    while True:
        server.listen(1)
        clientsock, clientAddress = server.accept()
        newthread = ClienteThread(clientAddress,clientsock)
        newthread.start()