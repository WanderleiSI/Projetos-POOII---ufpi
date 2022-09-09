import threading

class Threads(threading.Thread):
    def __init__(self,sinc,clientAddress,clientSock):
        self.sinc = sinc
        self.clientAddress = clientAddress
        self.clientSock = clientSock

    def run(self,requisicao,servidor):
        #requisicao = servidor.con.recv(1024)
        #requisicao = requisicao.decode()
        #requisicao = requisicao.split(',')
        while True:
            requisicao = self.clientSock.recv(1024)
            requisicao = self.clientSock.decode()
            requisicao = self.clientSock.split(',')
            
            self.sinc.acquire()
            if requisicao[0] == 'CLIENTE':
                    servidor.requisicaoChecagem('CLIENTE',(requisicao[1],requisicao[2]))
            elif requisicao == 'CONECTAR_BANCO_DE_DADOS':
                servidor.bd.conectarBanco()
                if servidor.bd.conexao.is_connected():
                    servidor.con.send("CONECTADO".encode())
                else:
                    servidor.con.send("DESCONECTADO".encode())
            elif requisicao[0] == 'CADASTRO':
                servidor.requisicaoChecagem('CADASTRO',(requisicao[1],requisicao[2],requisicao[3],requisicao[4],requisicao[5]))
            elif requisicao[0] == 'DEPOSITO':
                servidor.requisicaoValor('DEPOSITO',(requisicao[1],requisicao[2],requisicao[3],requisicao[4]))
            elif requisicao[0] == 'SAQUE':
                servidor.requisicaoValor('SAQUE',(requisicao[1],requisicao[2],requisicao[3],requisicao[4]))
            elif requisicao[0] == 'TRANSFERENCIA':
                servidor.requisicaoValor('TRANSFERENCIA',(requisicao[1],requisicao[2],requisicao[3],requisicao[4],requisicao[5]))
            elif requisicao[0] == 'DESCONECTAR_SERVIDOR':
                servidor.desconectarServidor()
                #break
            elif requisicao[0] == 'HISTORICO':
                historico = servidor.bd.PreencheHistorico(requisicao[1])
                if len(historico) == 0:
                    servidor.con.send('False'.encode())
                else:
                    retorno = ""
                    for h in historico:
                        retorno += F"{h}"
                        retorno += "|"
                    servidor.con.send(retorno.encode())
            self.sinc.release()            
