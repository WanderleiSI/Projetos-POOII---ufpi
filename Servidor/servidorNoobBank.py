import socket, threading
from bancoDeDados import BancoDeDados
from threadsNoobBank import Threads

class Servidor():
    def __init__(self,host='',port=8000):
        self.conectServer = self.conectarServidor(host,port)
        self.sinc = threading.Lock()

    def conectarServidor(self,host,port):
        servidor = host
        porta = port
        addr = (servidor,porta)
        self.serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv_socket.bind(addr)
        """self.serv_socket.listen(10)
        print('Aguardando conexao...')
        self.con, self.cliente = self.serv_socket.accept()
        print('Conectado')
        print('Aguardando mensagens...')"""
    
    def criarBancoDeDados(self):    
        self.bd = BancoDeDados()
        self.bd.conectarBanco()
        self.bd.TabelaUsuario()
        #self.bd.TabelaUsuario()
        self.bd.TabelaTransacoes()

    def receberRequisicao(self):
        mensagem = self.con.recv(1024)
        mensagem = mensagem.decode()
        print(mensagem)
        if mensagem[0] == 'CLIENTE':
            print("OPA")
            self.requisicaoChecagem()

        pass

    def requisicaoValor(self,requisição=None,valores=None):
        if requisição == 'DEPOSITO':
            if not(valores[0] == '' or valores[1] == ''):
                try:
                    float(valores[0])
                except:
                    self.con.send('2'.encode())
                else:    
                    valor = float(valores[0])
                    self.sinc.acquire()
                    if self.bd.conexao.is_connected():
                        self.sinc.release()
                        try:
                            self.sinc.acquire()
                            if self.bd.confereSenha(valores[2],valores[1]):
                                self.sinc.release()
                                if valor > 0.0:
                                    try:
                                        self.sinc.acquire()
                                        conta = self.bd.buscaUsuario(valores[2])
                                        self.sinc.release()
                                        valor += conta[5]
                                        self.sinc.acquire()
                                        self.bd.atualizaSaldo(deposita=True,dinheiro=valor,conta = conta[0])
                                        self.sinc.release()
                                        valor -= conta[5]
                                        self.sinc.acquire()
                                        self.bd.transacao(conta[0],"DEPOSITO",valor,conta[0]) 
                                        self.sinc.release()
                                        self.con.send('6'.encode())
                                    except:
                                        self.con.send('3'.encode())
                                else:
                                    self.con.send('5'.encode())
                            else: 
                                self.con.send('4'.encode()) 
                        except:
                            self.con.send('3'.encode())
                    else: 
                        self.con.send('3'.encode())       
            else:
                self.con.send('1'.encode())
        elif requisição == 'SAQUE':
            if not(valores[0] == '' or valores[1] == ''):
                try:
                    float(valores[0])
                except:
                    self.con.send('2'.encode())
                else:
                    valor = float(valores[0])
                    self.sinc.acquire()
                    if self.bd.conexao.is_connected():
                        self.sinc.release()
                        try:
                            self.sinc.acquire()
                            if self.bd.confereSenha(valores[2],valores[1]):
                                self.sinc.release()
                                if valor > 0.0:
                                    self.sinc.acquire()
                                    conta = self.bd.buscaUsuario(valores[2])
                                    self.sinc.release()
                                    if conta[5] >= valor:
                                        self.sinc.acquire()
                                        self.bd.atualizaSaldo(saca=True,dinheiro= (conta[5] - valor),conta = conta[0])
                                        self.sinc.release()
                                        self.sinc.acquire()
                                        self.bd.transacao(conta[0],"SAQUE",valor,conta[0])
                                        self.sinc.release()
                                        self.con.send('7'.encode())
                                    else:
                                        self.con.send('6'.encode())
                                else:
                                    self.con.send('5'.encode())
                            else:
                                self.con.send('4'.encode())
                        except:
                            self.con.send('3'.encode())
                    else:  
                        self.con.send('3'.encode())     
            else:
                self.con.send('1'.encode())
        elif requisição == 'TRANSFERENCIA':
            if not(valores[0] == '' or valores[1] == '' or valores[2] == ''):
                try:
                    float(valores[0])
                except:
                    self.con.send('2'.encode())
                else:       
                    valor = float(valores[0])
                    self.sinc.acquire()
                    if self.bd.conexao.is_connected():
                        self.sinc.release()
                        try:
                            self.sinc.acquire()
                            conta = self.bd.buscaUsuario(valores[3])
                            self.sinc.release()
                            if conta[5] >= valor:
                                try:
                                    int(valores[1])
                                except:
                                    self.con.send('5'.encode())
                                else:
                                    numConta = int(valores[1])
                                    self.sinc.acquire()
                                    destinatario = self.bd.buscaUsuario(nConta=True,conta=numConta)
                                    self.sinc.release()
                                    if destinatario != None:
                                        if destinatario[0] != conta[0]:
                                            self.sinc.acquire()
                                            if self.bd.confereSenha(valores[3],valores[2]):
                                                self.sinc.release()
                                                self.sinc.acquire()
                                                self.bd.atualizaSaldo(saca=True,dinheiro=(conta[5]-valor),conta=conta[0])
                                                self.sinc.release()
                                                self.sinc.acquire()
                                                self.bd.transacao(conta[0],"TRANSFERENCIA FEITA PARA",valor,destinatario[0])
                                                self.sinc.release()

                                                valor += destinatario[5]
                                                self.sinc.acquire()
                                                self.bd.atualizaSaldo(deposita=True,dinheiro=valor,conta=destinatario[0])
                                                self.sinc.release()
                                                self.sinc.acquire()
                                                self.bd.transacao(destinatario[0],"TRANSFERENCIA RECEBIDA POR",valor-destinatario[5],conta[0])
                                                self.sinc.release()

                                                self.con.send('9'.encode())
                                            else:
                                                self.con.send('8'.encode())
                                        else: 
                                            self.con.send('7'.encode())  
                                    else:
                                        self.con.send('6'.encode())
                            else:  
                                self.con.send('4'.encode())
                        except:
                            self.con.send('3'.encode())
                    else: 
                        self.con.send('3'.encode())        
            else:
                self.con.send('1'.encode())
        

    def requisicaoChecagem(self,tela=None,valores=None):
        if tela == 'CLIENTE':
            try:
                int(valores[0])
            except:
                self.con.send('1'.encode())
            else:
                cpf = valores[0]
                senha =  valores[1]
                self.sinc.acquire()
                if self.bd.conexao.is_connected():
                    self.sinc.release()
                    try:
                        self.sinc.acquire()
                        conta = self.bd.buscaUsuario(cpf)
                        self.sinc.release()
                        if not(cpf == '' or senha == ''):
                            if (conta != None):
                                self.sinc.acquire()
                                if self.bd.confereSenha(cpf,senha):
                                    self.sinc.release()
                                    usuario = F"{conta[0]},{conta[1]},{conta[2]},{conta[3]},{conta[4]},{conta[5]}"
                                    self.con.send(usuario.encode())
                                else:
                                    self.con.send('5'.encode())
                            else:
                                self.con.send('4'.encode())
                        else:
                            self.con.send('3'.encode())
                    except: 
                        self.con.send('2'.encode())  
                else:
                    self.con.send('2'.encode())
        elif tela == 'CADASTRO':
            try:
                int(valores[0])
            except:
                nome =  valores[0]
                try:
                    int(valores[1])
                except:
                    sobrenome = valores[1]
                    try:
                        int(valores[2])
                    except:
                        return 3
                    else:
                        cpf = valores[2]
                        senha = valores[3]
                        confirmarSenha = valores[4]
                        if not (nome == '' or sobrenome == '' or cpf == '' or senha == '' or confirmarSenha == ''):
                            if senha == confirmarSenha:
                                self.sinc.acquire()
                                if self.bd.conexao.is_connected():
                                    self.sinc.release()
                                    try:
                                        self.sinc.acquire()
                                        if (self.bd.InsereUsuario(nome,sobrenome,cpf,senha)):
                                            self.sinc.release()
                                            self.con.send('7'.encode())
                                        else:
                                            self.con.send('8'.encode())
                                    except:
                                        self.con.send('6'.encode())
                                else:
                                    self.con.send('6'.encode())
                            else:
                                self.con.send('5'.encode())
                        else:
                            self.con.send('4'.encode())
                else:
                    self.con.send('2'.encode())
            else:
                self.con.send('1'.encode())

    def reconectar(self):
        self.sinc.acquire()
        self.bd.conectarBanco()
        self.sinc.release()
        if self.bd.conectado:
            self.sinc.acquire()
            self.bd.TabelaUsuario()
            self.sinc.release()
            self.sinc.acquire()
            self.bd.TabelaTransacoes()
            self.sinc.release()
            return True
        
    def desconectarServidor(self):
        self.sinc.acquire()
        self.bd.EncerraBanco()
        self.sinc.release()
        self.serv_socket.close()
        
if __name__ == '__main__':
    servidor = Servidor()
    servidor.criarBancoDeDados()
    sinc = threading.Lock()
    while True:
        try:
            """mensagem = servidor.con.recv(1024)
            mensagem = mensagem.decode()
            mensagem = mensagem.split(',')
            if mensagem[0] == 'CLIENTE':
                servidor.requisicaoChecagem('CLIENTE',(mensagem[1],mensagem[2]))
            elif mensagem[0] == 'CONECTAR_BANCO_DE_DADOS':
                servidor.bd.conectarBanco()
                if servidor.bd.conexao.is_connected():
                    servidor.con.send("CONECTADO".encode())
                else:
                    servidor.con.send("DESCONECTADO".encode())
            elif mensagem[0] == 'CADASTRO':
                servidor.requisicaoChecagem('CADASTRO',(mensagem[1],mensagem[2],mensagem[3],mensagem[4],mensagem[5]))
            elif mensagem[0] == 'DEPOSITO':
                servidor.requisicaoValor('DEPOSITO',(mensagem[1],mensagem[2],mensagem[3],mensagem[4]))
            elif mensagem[0] == 'SAQUE':
                servidor.requisicaoValor('SAQUE',(mensagem[1],mensagem[2],mensagem[3],mensagem[4]))
            elif mensagem[0] == 'TRANSFERENCIA':
                servidor.requisicaoValor('TRANSFERENCIA',(mensagem[1],mensagem[2],mensagem[3],mensagem[4],mensagem[5]))
            elif mensagem[0] == 'DESCONECTAR_SERVIDOR':
                servidor.desconectarServidor()
                break
            elif mensagem[0] == 'HISTORICO':
                historico = servidor.bd.PreencheHistorico(mensagem[1])
                if len(historico) == 0:
                    servidor.con.send('False'.encode())
                else:
                    retorno = ""
                    for h in historico:
                        retorno += F"{h}"
                        retorno += "|"
                    servidor.con.send(retorno.encode())"""
            print("Dentro do loop do servidor")
            servidor.serv_socket.listen(10)
            print("Escutei uma conexao")
            #servidor.con, servidor.cliente = servidor.serv_socket.accept()
            clientsocket, clientAddress = servidor.serv_socket.accept()
            #servidor.con = clientsocket
            #servidor.cliente = clientAddress
            print("Aceitei a conexao")
            thread = Threads(sinc,clientAddress,clientsocket,servidor)
            #thread = Threads(sinc,servidor.cliente, servidor.con,servidor)
            print("Criei a thread")
            #thread.run(servidor)
            thread.start()
            #thread.join()
            print("Startei a thread")

        except:
            servidor.serv_socket.close()
            break
