import socket

class Cliente:
    def __init__(self,ip='localhost',port=8000):
        self.addr = ((ip,port))
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conectado = False
        self.conectClient = self.conectarServidor()
        

    def conectarServidor(self):
        try:
            self.client_socket.connect(self.addr)
            self.conectado = True
        except:
            self.conectado = False
    
    def requisicao(self,requisicao=None):
        self.client_socket.send(requisicao.encode())
    
    def resposta(self):
        self.retorno = self.client_socket.recv(1024).decode()
