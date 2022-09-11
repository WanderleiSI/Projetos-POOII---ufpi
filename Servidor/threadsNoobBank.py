import threading
#import copy

class Threads(threading.Thread):
    def __init__(self,sinc,clientAddress,clientSock,servidor):
        threading.Thread.__init__(self)
        self.sinc = sinc
        self.clientAddress = clientAddress
        self.clientSock = clientSock
        #self.servidor = copy.deepcopy(servidor)
        #self.servidor.con = self.clientSock
        self.servidor = servidor
        #servidor.con = self.clientSock
    def run(self):
        #requisicao = servidor.con.recv(1024)
        #requisicao = requisicao.decode()
        #requisicao = requisicao.split(',')
        print("Entrei no run")
        while True:
            print("Entrei no While")
            requisicao = self.clientSock.recv(1024)
            requisicao = requisicao.decode()
            requisicao = requisicao.split(',')
            #print(servidor.con.recv(1024).decode())
            
            self.sinc.acquire()
            if requisicao[0] == 'CLIENTE':
                self.servidor.requisicaoChecagem('CLIENTE',(requisicao[1],requisicao[2]),self.clientSock)
            elif requisicao == 'CONECTAR_BANCO_DE_DADOS':
                self.servidor.bd.conectarBanco()
                if self.servidor.bd.conexao.is_connected():
                    self.servidor.con.send("CONECTADO".encode())
                else:
                    self.servidor.con.send("DESCONECTADO".encode())
            elif requisicao[0] == 'CADASTRO':
                self.servidor.requisicaoChecagem('CADASTRO',(requisicao[1],requisicao[2],requisicao[3],requisicao[4],requisicao[5]),self.clientSock)
            elif requisicao[0] == 'DEPOSITO':
                self.servidor.requisicaoValor('DEPOSITO',(requisicao[1],requisicao[2],requisicao[3],requisicao[4]),self.clientSock)
            elif requisicao[0] == 'SAQUE':
                self.servidor.requisicaoValor('SAQUE',(requisicao[1],requisicao[2],requisicao[3],requisicao[4]),self.clientSock)
            elif requisicao[0] == 'TRANSFERENCIA':
                self.servidor.requisicaoValor('TRANSFERENCIA',(requisicao[1],requisicao[2],requisicao[3],requisicao[4],requisicao[5]),self.clientSock)
            elif requisicao[0] == 'DESCONECTAR_SERVIDOR':
                #self.servidor.desconectarServidor()
                #self.sinc.release()
                self.clientSock.close()
                break
            elif requisicao[0] == 'HISTORICO':
                print(requisicao)
                historico = self.servidor.bd.PreencheHistorico(requisicao[1])
                self.servidor.conexao = self.clientSock
                if len(historico) == 0:
                    #self.servidor.con.send('False'.encode())
                    self.servidor.conexao.send('False'.encode())
                else:
                    retorno = ""
                    for h in historico:
                        retorno += F"{h}"
                        retorno += "|"
                    #self.servidor.con.send(retorno.encode())
                    self.servidor.conexao.send(retorno.encode())
            self.sinc.release()            
