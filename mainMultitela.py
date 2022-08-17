import sys
import os

from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import QMainWindow,QApplication,QMessageBox,QFileDialog

from telaCadastro import Tela_Cadastro
from telaCliente import Tela_Cliente
from telaPrincipal import Tela_Principal
from telaDeposito import Tela_Deposito
from telaSaque import Tela_Saque
from telaTransferencia import Tela_Transferencia
from telaFalhaConexao import Tela_FalhaConexao
from bancoDeDados import BancoDeDados


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

        self.bd = BancoDeDados()
        self.bd.conectarBanco()
        if not self.bd.conectado:
            self.QtStack.setCurrentIndex(6)
        else:
            self.bd.TabelaUsuario()
            self.bd.TabelaTransacoes()
        
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
        self.bd.conectarBanco()
        if self.bd.conectado:
            self.bd.TabelaUsuario()
            self.bd.TabelaTransacoes()
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
        try:
            int(self.tela_principal.lineEdit.text())
        except:
            QMessageBox.information(None,'NOOBBANK','Cpf inválido.')
            self.tela_principal.lineEdit.setText('')
            self.tela_principal.lineEdit_2.setText('')
        else:
            cpf = self.tela_principal.lineEdit.text()
            senha = self.tela_principal.lineEdit_2.text()
            if self.bd.conexao.is_connected():
                try:
                    conta = self.bd.buscaUsuario(cpf)
                    if not(cpf == '' or senha == ''):
                        if (conta != None):
                            if senha == conta[4]:
                                _translate = QtCore.QCoreApplication.translate
                                self.tela_cliente.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:18pt;\">Bem-vindo(a) {}</span></p></body></html>").format(conta[1]))
                                self.tela_cliente.label_8.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">R${}</span></p></body></html>").format(conta[5]))
                                self.tela_cliente.label_10.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\"> {} {}</span></p></body></html>").format(conta[1],conta[2]))
                                self.tela_cliente.label_11.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\"> {}</span></p></body></html>").format(conta[3]))
                                self.tela_cliente.label_12.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\"> {}</span></p></body></html>").format(str(conta[0])))
                               
                                self.tela_cliente.listWidget.clear()
                                historico = self.bd.PreencheHistorico(conta[0])
                                if historico:
                                    for transacao in historico:
                                        if transacao[2] == "DEPOSITO":
                                            self.tela_cliente.listWidget.addItem(F"Depósito de R${transacao[4]:.2f}")
                                        elif transacao[2] == "SAQUE":
                                            self.tela_cliente.listWidget.addItem(F"Saque de R${transacao[4]:.2f}")
                                        elif transacao[2] == "TRANSFERENCIA RECEBIDA POR":
                                            self.tela_cliente.listWidget.addItem(F"Transferência de R${transacao[4]:.2f} por conta nº {transacao[3]}")
                                        elif transacao[2] == "TRANSFERENCIA FEITA PARA":
                                            self.tela_cliente.listWidget.addItem(F"Transferência de R${transacao[4]:.2f} para conta nº {transacao[3]}") 
                                

                                self.QtStack.setCurrentIndex(2)
                            else:
                                QMessageBox.information(None,'NOOBBANK','Cpf ou senha inválidos.')
                        else:
                            QMessageBox.information(None,'NOOBBANK','Conta não encontrada.')
                    else:
                        QMessageBox.information(None,'NOOBBANK','Todos os campos devem ser preenchidos.')
                except:
                    self.QtStack.setCurrentIndex(6)     
            else:
                self.QtStack.setCurrentIndex(6)

    def sairPrincipal(self):
        self.bd.EncerraBanco()
        sys.exit()

    def criarConta(self):
        try:
            int(self.tela_cadastro.lineEdit.text())
        except:
            nome =  self.tela_cadastro.lineEdit.text()
            try:
                int(self.tela_cadastro.lineEdit_2.text())
            except:
                sobrenome = self.tela_cadastro.lineEdit_2.text()
                try:
                    int(self.tela_cadastro.lineEdit_3.text())
                except:
                    QMessageBox.information(None,'NOOBBANK','Valor do campo cpf inválido.')
                else:
                    cpf = self.tela_cadastro.lineEdit_3.text()
                    senha = self.tela_cadastro.lineEdit_4.text()
                    confirmarSenha = self.tela_cadastro.lineEdit_5.text()
                    if not (nome == '' or sobrenome == '' or cpf == '' or senha == '' or confirmarSenha == ''):
                        if senha == confirmarSenha:
                            if self.bd.conexao.is_connected():
                                try:
                                    if (self.bd.InsereUsuario(nome,sobrenome,cpf,senha)):
                                        QMessageBox.information(None,'NOOBBANK','Conta cadastrada com sucesso')
                                        nome =  self.tela_cadastro.lineEdit.setText('')
                                        sobrenome = self.tela_cadastro.lineEdit_2.setText('')
                                        cpf = self.tela_cadastro.lineEdit_3.setText('')
                                        senha = self.tela_cadastro.lineEdit_4.setText('')
                                        confirmarSenha = self.tela_cadastro.lineEdit_5.setText('')
                                        self.QtStack.setCurrentIndex(0)
                                    else:
                                        QMessageBox.information(None,'NOOBBANK','CPF já cadastrado!')
                                except:
                                    self.QtStack.setCurrentIndex(6)
                            else:
                                self.QtStack.setCurrentIndex(6)
                        else:
                            QMessageBox.information(None,'NOOBBANK','Senhas devem ser iguais')
                    else:
                        QMessageBox.information(None,'NOOBBANK','Todos os campos devem ser preenchidos!')
            else:
                QMessageBox.information(None,'NOOBBANK','Valor do campo nome inválido.')
        else:
            QMessageBox.information(None,'NOOBBANK','Valor do campo sobrenome inválido.')
            
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
        if not(self.tela_deposito.lineEdit.text() == '' or self.tela_deposito.lineEdit_2.text() == ''):
            try:
                float(self.tela_deposito.lineEdit.text())
            except:
                QMessageBox.information(None,'NOOBBANK','Valor para depósito inválido.')
                self.tela_deposito.lineEdit.setText('')
                self.tela_deposito.lineEdit_2.setText('')
            else:    
                valor = float(self.tela_deposito.lineEdit.text())
                if self.bd.conexao.is_connected():
                    if self.bd.confereSenha(self.tela_principal.lineEdit.text(),self.tela_deposito.lineEdit_2.text()):
                        if valor > 0.0:
                            try:
                                conta = self.bd.buscaUsuario(self.tela_principal.lineEdit.text())
                                valor += conta[5]
                                self.bd.atualizaSaldo(deposita=True,dinheiro=valor,conta = conta[0])
                                QMessageBox.information(None,'NOOBBANK','Depósito realizado com sucesso.')
                                self.tela_deposito.lineEdit.setText('')
                                self.tela_deposito.lineEdit_2.setText('')
                                _translate = QtCore.QCoreApplication.translate 
                                self.tela_cliente.label_8.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">R${}</span></p></body></html>").format(conta[5]))
                                
                                valor -= conta[5]
                                self.bd.transacao(conta[0],"DEPOSITO",valor,conta[0])
                                
                                '''self.tela_cliente.listWidget.clear()
                                conta.historico.transacoes.append(F"Depósito de R${(valor):.2f}")
                                for transacao in range(len(conta.historico.transacoes)-1,-1,-1):
                                    self.tela_cliente.listWidget.addItem(conta.historico.transacoes[transacao])'''
                                
                            except:
                                self.QtStack.setCurrentIndex(6)
                        else:
                            QMessageBox.information(None,'NOOBBANK','Valor para depótivo inválido.')
                            self.tela_deposito.lineEdit.setText('')
                            self.tela_deposito.lineEdit_2.setText('')
                    else:
                        QMessageBox.information(None,'NOOBBANK','Senha incorreta.')
                        self.tela_deposito.lineEdit_2.setText('')  
                else:
                    self.QtStack.setCurrentIndex(6)         
        else:
            QMessageBox.information(None,'NOOBBANK','Todos os campos devem ser preenchidos.')

    def abrirSaque(self):
        self.tela_saque.lineEdit.setText('')
        self.tela_saque.lineEdit_2.setText('')
        self.QtStack.setCurrentIndex(4)

    def sairSaque(self):
        self.tela_saque.lineEdit.setText('')
        self.tela_saque.lineEdit_2.setText('')
        self.abrirTelaCliente()

    def sacar(self):
        if not(self.tela_saque.lineEdit.text() == '' or self.tela_saque.lineEdit_2.text() == ''):
            try:
                float(self.tela_saque.lineEdit.text())
            except:
                QMessageBox.information(None,'NOOBBANK','Valor de saque inválido')
                self.tela_saque.lineEdit.setText('')
                self.tela_saque.lineEdit_2.setText('')
            else:
                valor = float(self.tela_saque.lineEdit.text())
                if self.bd.conexao.is_connected():
                    try:
                        if self.bd.confereSenha(self.tela_principal.lineEdit.text(),self.tela_saque.lineEdit_2.text()):
                            if valor > 0.0:
                                conta = self.bd.buscaUsuario(self.tela_principal.lineEdit.text())
                                if conta[5] >= valor:
                                    self.bd.atualizaSaldo(saca=True,dinheiro= (conta[5] - valor),conta = conta[0])
                                    QMessageBox.information(None,'NOOBBANK','Saque realizado com sucesso.')
                                    self.tela_saque.lineEdit.setText('')
                                    self.tela_saque.lineEdit_2.setText('')
                                    _translate = QtCore.QCoreApplication.translate
                                    self.tela_cliente.label_8.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">R${}</span></p></body></html>").format(conta[5]))
                        
                                    self.bd.transacao(conta[0],"SAQUE",valor,conta[0])

                                    ''' self.tela_cliente.listWidget.clear()
                                    conta.historico.transacoes.append(F"Saque de R${(valor):.2f}")
                                    for transacao in range(len(conta.historico.transacoes)-1,-1,-1):
                                        self.tela_cliente.listWidget.addItem(conta.historico.transacoes[transacao])'''
                                else:
                                    QMessageBox.information(None,'NOOBBANK','Saldo insuficiente para realizar saque.')
                                    self.tela_saque.lineEdit.setText('')
                                    self.tela_saque.lineEdit_2.setText('')
                            else:
                                QMessageBox.information(None,'NOOBBANK','Valor para saque inválido.')
                                self.tela_saque.lineEdit.setText('')
                                self.tela_saque.lineEdit_2.setText('')
                        else:
                            QMessageBox.information(None,'NOOBBANK','Senha incorreta.')
                            self.tela_saque.lineEdit_2.setText('')
                    except:
                        self.QtStack.setCurrentIndex(6)
                else:
                    self.QtStack.setCurrentIndex(6)        
        else:
            QMessageBox.information(None,'NOOBBANK','Todos os campos devem ser preenchidos.')

    def abrirTransferencia(self):
        self.tela_transferencia.lineEdit.setText('')
        self.tela_transferencia.lineEdit_3.setText('')
        self.tela_transferencia.lineEdit_2.setText('')
        self.QtStack.setCurrentIndex(5)

    def transferir(self):
        if not(self.tela_transferencia.lineEdit.text() == '' or self.tela_transferencia.lineEdit_3.text() == '' or self.tela_transferencia.lineEdit_2.text() == ''):
            try:
                float(self.tela_transferencia.lineEdit.text())
            except:
                QMessageBox.information(None,'NOOBBANK','Valor de transferência inválido.')
                self.tela_transferencia.lineEdit.setText('')
                self.tela_transferencia.lineEdit_3.setText('')
                self.tela_transferencia.lineEdit_2.setText('')
            else:       
                valor = float(self.tela_transferencia.lineEdit.text())
                if self.bd.conexao.is_connected():
                    try:
                        conta = self.bd.buscaUsuario(self.tela_principal.lineEdit.text())
                        if conta[5] >= valor:
                            try:
                                int(self.tela_transferencia.lineEdit_3.text())
                            except:
                                QMessageBox.information(None,'NOOBBANK','Número de conta inválido.')
                                self.tela_transferencia.lineEdit_3.setText('')
                                self.tela_transferencia.lineEdit_2.setText('')
                            else:
                                numConta = int(self.tela_transferencia.lineEdit_3.text())
                                destinatario = self.bd.buscaUsuario(nConta=True,conta=numConta)
                                if destinatario != None:
                                    if destinatario[0] != conta[0]:
                                        if self.bd.confereSenha(self.tela_principal.lineEdit.text(),self.tela_transferencia.lineEdit_2.text()):
                                            self.bd.atualizaSaldo(saca=True,dinheiro=(conta[5]-valor),conta=conta[0])
                                            self.bd.transacao(conta[0],"TRANSFERENCIA FEITA PARA",valor,destinatario[0])

                                            valor += destinatario[5]
                                            self.bd.atualizaSaldo(deposita=True,dinheiro=valor,conta=destinatario[0])
                                            self.bd.transacao(destinatario[0],"TRANSFERENCIA RECEBIDA POR",valor-destinatario[5],conta[0])

                                            QMessageBox.information(None,'NOOBBANK','Transferência realizada com sucesso.')
                                            self.tela_transferencia.lineEdit.setText('')
                                            self.tela_transferencia.lineEdit_3.setText('')
                                            self.tela_transferencia.lineEdit_2.setText('')
                                            _translate = QtCore.QCoreApplication.translate
                                            self.tela_cliente.label_8.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">R${}</span></p></body></html>").format(conta[5]))

                                        else:
                                            QMessageBox.information(None,'NOOBBANK','Senha incorreta.')
                                            self.tela_transferencia.lineEdit.setText('')
                                            self.tela_transferencia.lineEdit_3.setText('')
                                            self.tela_transferencia.lineEdit_2.setText('')
                                    else:
                                        QMessageBox.information(None,'NOOBBANK','Não é possível realizar transferência para a mesma conta.')
                                        self.tela_transferencia.lineEdit_3.setText('')
                                        self.tela_transferencia.lineEdit_2.setText('')   
                                else:
                                    QMessageBox.information(None,'NOOBBANK','Conta não encontrada.')
                                    self.tela_transferencia.lineEdit.setText('')
                        else:
                            QMessageBox.information(None,'NOOBBANK','Saldo insuficiente para realizar transferência.')
                            self.tela_transferencia.lineEdit.setText('')
                            self.tela_transferencia.lineEdit_3.setText('')
                            self.tela_transferencia.lineEdit_2.setText('')  
                    except:
                        self.QtStack.setCurrentIndex(6)
                else:
                    self.QtStack.setCurrentIndex(6)         
        else:
            QMessageBox.information(None,'NOOBBANK','Todos os campos devem ser preenchidos.')
   
    def sairTransferencia(self):
        self.tela_transferencia.lineEdit.setText('')
        self.tela_transferencia.lineEdit_3.setText('')
        self.tela_transferencia.lineEdit_2.setText('')
        self.abrirTelaCliente()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    show_main = Main()
    sys.exit(app.exec_())