import mysql.connector
from mysql.connector import Error
import hashlib
#from testeConexao import testeConexao

class BancoDeDados:
    def __init__(self):
        self.conectado = None
        
    def conectarBanco(self):
        try:
            #self.conexao = mysql.connector.connect(host='localhost',database='noobbank',user='root',password='')
            self.conexao = mysql.connector.connect(host='localhost',port='3300', database='noobbank',user='wanderlei',password='wanderlei')
            self.cursor = self.conexao.cursor()
            self.conectado = True
        except Error as erro:
            self.conectado = False

    def TabelaUsuario(self):
        #sql = """CREATE TABLE IF NOT EXISTS usuarios (id integer PRIMARY KEY auto_increment NOT NULL, nome text NOT NULL, endereco text NOT NULL,cpf varchar(11) NOT NULL, nascimento varchar(10) NOT NULL);"""
        sql = """CREATE TABLE IF NOT EXISTS clientes(
                nConta int NOT NULL AUTO_INCREMENT,
                nome varchar(50) NOT NULL,
                sobrenome varchar(50) NOT NULL,
                cpf varchar(14) NOT NULL,
                senha varchar(50) NOT NULL,
                saldo float default 0.0,
            PRIMARY KEY (nConta)
            )DEFAULT CHARSET = utf8mb4;"""
        self.cursor.execute(sql) 
        self.conexao.commit()

    def TabelaTransacoes(self):
        sql = """CREATE TABLE IF NOT EXISTS transacoes(
                nTransacao INT NOT NULL AUTO_INCREMENT,
                idCliente INT,
                transacao  ENUM("DEPOSITO","SAQUE","TRANSFERENCIA FEITA PARA","TRANSFERENCIA RECEBIDA POR") NOT NULL,
                destinatario INT,
                valor FLOAT NOT NULL,
                PRIMARY KEY(nTransacao),
                FOREIGN KEY(idCliente) REFERENCES clientes(nConta),
                FOREIGN KEY(destinatario) REFERENCES clientes(nConta)
            )DEFAULT CHARSET = utf8mb4;"""
        self.cursor.execute(sql)
        self.conexao.commit()

    def PreencheHistorico(self,idCliente):
        #sql = F"SELECT * FROM transacoes WHERE idCliente = {idCliente};"
        sql = F"SELECT * FROM transacoes WHERE idCliente = {idCliente} ORDER BY nTransacao DESC;"
        self.cursor.execute(sql)
        historico = []
        for transacao in self.cursor.fetchall():
            historico.append(transacao)
        return historico

    def transacao(self,idCliente,transacao,valor,destinatario=False):
        dados = F"{idCliente},'{transacao}',{valor},{destinatario});"
        sql = """INSERT INTO transacoes(idCliente,transacao,valor,destinatario) VALUES(""" + dados
        self.cursor.execute(sql)
        self.conexao.commit()
    
    def InsereUsuario(self,nome,sobrenome,cpf,senha):
        pessoa = self.buscaUsuario(cpf)
        if pessoa == None: 
            hash = hashlib.md5()
            hash.update(senha.encode('utf8'))
            hash = hash.hexdigest()
            #print(hash)
            dados = F"'{nome}','{sobrenome}','{cpf}','{hash}');"
            sql = """INSERT INTO clientes (nome,sobrenome,cpf,senha) VALUES(""" + dados
            self.cursor.execute(sql)
            self.conexao.commit()
            return True
        else:
            return False

    def buscaUsuario(self,cpf=None,nConta=False,conta=None):
        if nConta:
            self.cursor.execute(F"SELECT * from clientes WHERE nConta = {conta};")
            for pessoa in self.cursor.fetchall():
                if conta == pessoa[0]:
                    return pessoa
            else:
                return None
        else:
            self.cursor.execute(F"SELECT * from clientes WHERE cpf = {cpf};")
            for pessoa in self.cursor.fetchall():
                if cpf == pessoa[3]:
                    return pessoa
            return None
    
    def confereSenha(self,cpf,senha):
        pessoa = self.buscaUsuario(cpf)
        if pessoa != None:
            hash = hashlib.md5()
            hash.update(senha.encode('utf8'))
            hash = hash.hexdigest()
            if  hash == pessoa[4]:
                return True
            else:
                return False
        else:
            return False
        
    def atualizaSaldo(self,deposita=False,saca=False,transfere=False,dinheiro = 0.0, conta=None,contaTransfere=None):
        if deposita:
            self.cursor.execute(F"UPDATE clientes SET saldo = {dinheiro} WHERE nConta = {conta};")
            self.conexao.commit()
        if saca:
            self.cursor.execute(F"UPDATE clientes SET saldo = {dinheiro} WHERE nConta = {conta};")
            self.conexao.commit()
        if transfere:
            self.cursor.execute(F"UPDATE clientes SET saldo = {dinheiro} WHERE nConta = {conta};")
            self.cursor.execute(F"UPDATE clientes SET saldo = {dinheiro} WHERE nConta = {contaTransfere};")
            self.conexao.commit()

    def EncerraBanco(self):
        self.conexao.commit()
        self.cursor.close()
        self.conexao.close()