import sys
import os

from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import QMainWindow,QApplication,QMessageBox,QFileDialog

from Cliente.telaCadastro import Tela_Cadastro
from Cliente.telaCliente import Tela_Cliente
from Cliente.telaPrincipal import Tela_Principal
from Cliente.telaDeposito import Tela_Deposito
from Cliente.telaSaque import Tela_Saque
from Cliente.telaTransferencia import Tela_Transferencia
from Cliente.telaFalhaConexao import Tela_FalhaConexao
from Servidor.bancoDeDados import BancoDeDados

#from Servidor.servidorNoobBank import Servidor
from Cliente.clienteNoobBank import Cliente

class Ui_Main(QtWidgets.QWidget): 
    def setupUi(self,Main):
        Main.setObjectName("Main")
        Main.resize(640,480)

        self.QtStack = QtWidgets.QStackedLayout()

        self.stack0 = QtWidgets.QMainWindow()
        self.stack1 = QtWidgets.QMainWindow()
        self.stack2 = QtWidgets.QMainWindow()
        self.stack3 = QtWidgets.QMainWindow()
        self.stack4 = QtWidgets.QMainWindow()
        self.stack5 = QtWidgets.QMainWindow()
        self.stack6 = QtWidgets.QMainWindow()

        self.tela_principal = Tela_Principal()
        self.tela_principal.setupUi(self.stack0)
        
        self.tela_cadastro = Tela_Cadastro()
        self.tela_cadastro.setupUi(self.stack1)

        self.tela_cliente = Tela_Cliente()
        self.tela_cliente.setupUi(self.stack2)

        self.tela_deposito = Tela_Deposito()
        self.tela_deposito.setupUi(self.stack3)

        self.tela_saque = Tela_Saque()
        self.tela_saque.setupUi(self.stack4)

        self.tela_transferencia = Tela_Transferencia()
        self.tela_transferencia.setupUi(self.stack5)

        self.tela_falhaconexao = Tela_FalhaConexao()
        self.tela_falhaconexao.setupUi(self.stack6)

        self.QtStack.addWidget(self.stack0)
        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)
        self.QtStack.addWidget(self.stack4)
        self.QtStack.addWidget(self.stack5)
        self.QtStack.addWidget(self.stack6)

class Main(QMainWindow, Ui_Main):
    def __init__(self, parent=None):
        super(Main,self).__init__(parent)
        self.setupUi(self)

        #self.servidor = Servidor()
        #self.servidor.criarBancoDeDados()
    
        """if not self.servidor.bd.conectado:
            self.QtStack.setCurrentIndex(6)
        else:
            self.servidor.bd.TabelaUsuario()
            self.servidor.bd.TabelaTransacoes()"""
        
        self.cliente = Cliente()
        if not self.cliente.conectado:
            QMessageBox.information(None,'NOOBBANK','Não foi possível conectar ao servidor :(')
            sys.exit()
            
        self.tela_principal.botaoPrincipalEntrar.clicked.connect(self.abrirTelaCliente)
        self.tela_principal.botaoPrincipalCadastrar.clicked.connect(self.abrirTelaCadastro)
        self.tela_principal.botaoPrincipalSair.clicked.connect(self.sairPrincipal)

        self.tela_cadastro.pushButton.clicked.connect(self.criarConta)
        self.tela_cadastro.pushButton_2.clicked.connect(self.botaoVoltar)

        self.tela_cliente.pushButton_2.clicked.connect(self.botaoVoltar)
        self.tela_cliente.botaoUsuarioDepositar.clicked.connect(self.abrirDeposito)
        self.tela_cliente.botaoUsuarioSacar.clicked.connect(self.abrirSaque)
        self.tela_cliente.botaoUsuarioTransferir.clicked.connect(self.abrirTransferencia)
        
        
        self.tela_deposito.botaoDepositar.clicked.connect(self.deposita)
        self.tela_deposito.botaoDepositoVoltar.clicked.connect(self.sairDeposito)
        
        self.tela_saque.botaoSacar.clicked.connect(self.sacar)
        self.tela_saque.botaoSacarVoltar.clicked.connect(self.sairSaque)

        self.tela_transferencia.botaoTransferir.clicked.connect(self.transferir)
        self.tela_transferencia.botaoTransferenciaVoltar.clicked.connect(self.sairTransferencia)

        self.tela_falhaconexao.botaoReconecta.clicked.connect(self.reconectar)

    def reconectar(self):
        self.cliente.requisicao('CONECTAR_BANCO_DE_DADOS')
        self.cliente.resposta()
        if self.cliente.retorno == 'CONECTADO':
            self.tela_principal.lineEdit.setText('')
            self.tela_principal.lineEdit_2.setText('')
            self.QtStack.setCurrentIndex(0)
            
            
    def abrirTelaCadastro(self):
        self.tela_cadastro.lineEdit.setText('')
        self.tela_cadastro.lineEdit_2.setText('')
        self.tela_cadastro.lineEdit_3.setText('')
        self.tela_cadastro.lineEdit_4.setText('')
        self.tela_cadastro.lineEdit_5.setText('')
        self.QtStack.setCurrentIndex(1)

    def abrirTelaCliente(self):
        self.cliente.requisicao(f"CLIENTE,{self.tela_principal.lineEdit.text()},{self.tela_principal.lineEdit_2.text()}")
        self.cliente.resposta()
        try:
            #if isinstance(self.cliente.retorno,str):
            int(self.cliente.retorno)
        except:
            usuario = self.cliente.retorno.split(',')
            _translate = QtCore.QCoreApplication.translate
            self.tela_cliente.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:18pt;\">Bem-vindo(a) {}</span></p></body></html>").format(usuario[1]))
            self.tela_cliente.label_8.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">R${}</span></p></body></html>").format(usuario[5]))
            self.tela_cliente.label_10.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\"> {} {}</span></p></body></html>").format(usuario[1],usuario[2]))
            self.tela_cliente.label_11.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\"> {}</span></p></body></html>").format(usuario[3]))
            self.tela_cliente.label_12.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\"> {}</span></p></body></html>").format(str(usuario[0])))

            #self.historico(usuario[0])
            self.QtStack.setCurrentIndex(2)
            
        else:
            retorno = int(self.cliente.retorno)
            if retorno == 1:
                QMessageBox.information(None,'NOOBBANK','Cpf inválido.')
                self.tela_principal.lineEdit.setText('')
                self.tela_principal.lineEdit_2.setText('')
            elif retorno == 2:
                self.QtStack.setCurrentIndex(6)
            elif retorno == 3:
                QMessageBox.information(None,'NOOBBANK','Todos os campos devem ser preenchidos.')
            elif retorno == 4:
                QMessageBox.information(None,'NOOBBANK','Conta não encontrada.')
            elif retorno == 5:
                QMessageBox.information(None,'NOOBBANK','Cpf ou senha inválidos.')
                
             
    def historico(self,idCliente=None):
        self.tela_cliente.listWidget.clear()
        self.cliente.requisicao(F'HISTORICO,{idCliente}')
        self.cliente.resposta()
        historico = self.cliente.retorno
        if historico != 'False':
            historico = self.cliente.retorno.split("|")
            historico.pop()
            for h in historico:
                aux = h[1:-1].split(",")
                if aux[2] == " 'DEPOSITO'":
                    self.tela_cliente.listWidget.addItem(F"Depósito de R${float(aux[4]):.2f}")
                elif aux[2] == " 'SAQUE'":
                    self.tela_cliente.listWidget.addItem(F"Saque de R${float(aux[4]):.2f}")
                elif aux[2] == " 'TRANSFERENCIA FEITA PARA'":
                    self.tela_cliente.listWidget.addItem(F"Transferência de R${float(aux[4]):.2f} para conta nº {aux[3]}")
                elif aux[2] == " 'TRANSFERENCIA RECEBIDA POR'":
                    self.tela_cliente.listWidget.addItem(F"Transferência de R${float(aux[4]):.2f} por conta nº {aux[3]}")
        self.QtStack.setCurrentIndex(2)

    def sairPrincipal(self):
        self.cliente.requisicao("DESCONECTAR_SERVIDOR")
        sys.exit()

    def criarConta(self):
        self.cliente.requisicao(f"CADASTRO,{self.tela_cadastro.lineEdit.text()},{self.tela_cadastro.lineEdit_2.text()},{self.tela_cadastro.lineEdit_3.text()},{self.tela_cadastro.lineEdit_4.text()},{self.tela_cadastro.lineEdit_5.text()}")
        self.cliente.resposta()
        retorno = int(self.cliente.retorno)
        if retorno == 1:
            QMessageBox.information(None,'NOOBBANK','Valor do campo nome inválido.')
        elif retorno == 2:
            QMessageBox.information(None,'NOOBBANK','Valor do campo sobrenome inválido.')
        elif retorno == 3:    
            QMessageBox.information(None,'NOOBBANK','Valor do campo cpf inválido.')
        elif retorno == 4:
            QMessageBox.information(None,'NOOBBANK','Todos os campos devem ser preenchidos!')
        elif retorno == 5:
            QMessageBox.information(None,'NOOBBANK','Senhas devem ser iguais')
        elif retorno == 6:
            self.QtStack.setCurrentIndex(6)
        elif retorno == 7:
            QMessageBox.information(None,'NOOBBANK','Conta cadastrada com sucesso')
            self.tela_cadastro.lineEdit.setText('')
            self.tela_cadastro.lineEdit_2.setText('')
            self.tela_cadastro.lineEdit_3.setText('')
            self.tela_cadastro.lineEdit_4.setText('')
            self.tela_cadastro.lineEdit_5.setText('')
            self.QtStack.setCurrentIndex(0)
        elif retorno == 8:
            QMessageBox.information(None,'NOOBBANK','CPF já cadastrado!')
            
    def botaoVoltar(self):
        self.tela_principal.lineEdit.setText('')
        self.tela_principal.lineEdit_2.setText('')
        self.QtStack.setCurrentIndex(0)
        
    def abrirDeposito(self):
        self.tela_deposito.lineEdit.setText('')
        self.tela_deposito.lineEdit_2.setText('')
        self.QtStack.setCurrentIndex(3)

    def sairDeposito(self):
        self.tela_deposito.lineEdit.setText('')
        self.tela_deposito.lineEdit_2.setText('')
        self.abrirTelaCliente()

    def deposita(self):
        self.cliente.requisicao(F"DEPOSITO,{self.tela_deposito.lineEdit.text()},{self.tela_deposito.lineEdit_2.text()},{self.tela_principal.lineEdit.text()},{self.tela_principal.lineEdit_2.text()}")
        self.cliente.resposta()
        retorno = int(self.cliente.retorno)
        if retorno == 1:
            QMessageBox.information(None,'NOOBBANK','Todos os campos devem ser preenchidos.')
        elif retorno == 2:
            QMessageBox.information(None,'NOOBBANK','Valor para depósito inválido.')
            self.tela_deposito.lineEdit.setText('')
            self.tela_deposito.lineEdit_2.setText('')
        elif retorno == 3:
            self.QtStack.setCurrentIndex(6)
        elif retorno == 4:
            QMessageBox.information(None,'NOOBBANK','Senha incorreta.')
            self.tela_deposito.lineEdit_2.setText('')
        elif retorno == 5:
            QMessageBox.information(None,'NOOBBANK','Valor para depótivo inválido.')
            self.tela_deposito.lineEdit.setText('')
            self.tela_deposito.lineEdit_2.setText('')
        elif retorno == 6:
            QMessageBox.information(None,'NOOBBANK','Depósito realizado com sucesso.')
            self.tela_deposito.lineEdit.setText('')
            self.tela_deposito.lineEdit_2.setText('')

    def abrirSaque(self):
        self.tela_saque.lineEdit.setText('')
        self.tela_saque.lineEdit_2.setText('')
        self.QtStack.setCurrentIndex(4)

    def sairSaque(self):
        self.tela_saque.lineEdit.setText('')
        self.tela_saque.lineEdit_2.setText('')
        self.abrirTelaCliente()

    def sacar(self):
        self.cliente.requisicao(F"SAQUE,{self.tela_saque.lineEdit.text()},{self.tela_saque.lineEdit_2.text()},{self.tela_principal.lineEdit.text()},{self.tela_principal.lineEdit_2.text()}")
        self.cliente.resposta()
        retorno = int(self.cliente.retorno)
        if retorno == 1:
            QMessageBox.information(None,'NOOBBANK','Todos os campos devem ser preenchidos.')
        elif retorno == 2:
            QMessageBox.information(None,'NOOBBANK','Valor de saque inválido')
            self.tela_saque.lineEdit.setText('')
            self.tela_saque.lineEdit_2.setText('')
        elif retorno == 3:
            self.QtStack.setCurrentIndex(6)
        elif retorno == 4:
            QMessageBox.information(None,'NOOBBANK','Senha incorreta.')
            self.tela_saque.lineEdit_2.setText('')
        elif retorno == 5:
            QMessageBox.information(None,'NOOBBANK','Valor para saque inválido.')
            self.tela_saque.lineEdit.setText('')
            self.tela_saque.lineEdit_2.setText('')
        elif retorno == 6:
            QMessageBox.information(None,'NOOBBANK','Saldo insuficiente para realizar saque.')
            self.tela_saque.lineEdit.setText('')
            self.tela_saque.lineEdit_2.setText('')
        elif retorno == 7:
            QMessageBox.information(None,'NOOBBANK','Saque realizado com sucesso.')
            self.tela_saque.lineEdit.setText('')
            self.tela_saque.lineEdit_2.setText('')

    def abrirTransferencia(self):
        self.tela_transferencia.lineEdit.setText('')
        self.tela_transferencia.lineEdit_3.setText('')
        self.tela_transferencia.lineEdit_2.setText('')
        self.QtStack.setCurrentIndex(5)

    def transferir(self):
        self.cliente.requisicao(F"TRANSFERENCIA,{self.tela_transferencia.lineEdit.text()},{self.tela_transferencia.lineEdit_3.text()},{self.tela_transferencia.lineEdit_2.text()},{self.tela_principal.lineEdit.text()},{self.tela_principal.lineEdit_2.text()}")
        self.cliente.resposta()
        retorno = int(self.cliente.retorno)
        if retorno == 1:
            QMessageBox.information(None,'NOOBBANK','Todos os campos devem ser preenchidos.')
        elif retorno == 2:
            QMessageBox.information(None,'NOOBBANK','Valor de transferência inválido.')
            self.tela_transferencia.lineEdit.setText('')
            self.tela_transferencia.lineEdit_3.setText('')
            self.tela_transferencia.lineEdit_2.setText('')
        elif retorno == 3:
            self.QtStack.setCurrentIndex(6)
        elif retorno == 4:
            QMessageBox.information(None,'NOOBBANK','Saldo insuficiente para realizar transferência.')
            self.tela_transferencia.lineEdit.setText('')
            self.tela_transferencia.lineEdit_3.setText('')
            self.tela_transferencia.lineEdit_2.setText('')
        elif retorno == 5:
            QMessageBox.information(None,'NOOBBANK','Número de conta inválido.')
            self.tela_transferencia.lineEdit_3.setText('')
            self.tela_transferencia.lineEdit_2.setText('')
        elif retorno == 6:
            QMessageBox.information(None,'NOOBBANK','Conta não encontrada.')
            self.tela_transferencia.lineEdit_3.setText('')
            self.tela_transferencia.lineEdit_2.setText('')
        elif retorno == 7:
            QMessageBox.information(None,'NOOBBANK','Não é possível realizar transferência para a mesma conta.')
            self.tela_transferencia.lineEdit_3.setText('')
            self.tela_transferencia.lineEdit_2.setText('')
        elif retorno == 8:
            QMessageBox.information(None,'NOOBBANK','Senha incorreta.')
            self.tela_transferencia.lineEdit.setText('')
            self.tela_transferencia.lineEdit_3.setText('')
            self.tela_transferencia.lineEdit_2.setText('')
        elif retorno == 9:
            QMessageBox.information(None,'NOOBBANK','Transferência realizada com sucesso.')
            self.tela_transferencia.lineEdit.setText('')
            self.tela_transferencia.lineEdit_3.setText('')
            self.tela_transferencia.lineEdit_2.setText('')

    def sairTransferencia(self):
        self.tela_transferencia.lineEdit.setText('')
        self.tela_transferencia.lineEdit_3.setText('')
        self.tela_transferencia.lineEdit_2.setText('')
        self.abrirTelaCliente()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    show_main = Main()
    sys.exit(app.exec_())