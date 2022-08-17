from historico import Historico

class Conta:
    __slots__ = ['Conta_total_contas','_Conta_numero_contas','_numero','_nome','_sobrenome','_cpf','_senha','_saldo','_historico']
    _total_contas = 0
    _numero_conta = 1

    def __init__(self,nome,sobrenome,cpf,senha):
        self._numero = Conta._numero_conta
        self._nome = nome
        self._sobrenome = sobrenome
        self._cpf = cpf
        self._senha = senha
        self._saldo = 0.0
        self._historico = Historico()
        Conta._total_contas += 1
        Conta._numero_conta += 1

    @staticmethod
    def total_contas():
        return Conta._total_contas

    @property
    def numero(self):
        return self._numero
    
    @numero.setter
    def numero(self,numero):
        self._numero = numero
    
    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self,nome):
        self._nome = nome

    @property
    def sobrenome(self):
        return self._sobrenome

    @sobrenome.setter
    def sobrenome(self,sobrenome):
        self._sobrenome = sobrenome

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self,cpf):
        self._cpf = cpf

    @property
    def senha(self):
        return self._senha

    @senha.setter
    def senha(self,senha):
        self._senha = senha

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self,saldo):
        self._saldo = saldo

    @property
    def historico(self):
        return self._historico

    def deposita(self,valor,tranferencia = True):
        if valor <= 0:
            return False
        else:
            self._saldo += valor
            if tranferencia:
                self._historico.transacoes.append(F'Depósito de R${valor:.2f}')
            return True
    
    def saca(self,valor,tranferencia = True):
        if valor <= 0:
            return False
        else:
            if self._saldo < valor:
                return False
            else:
                self._saldo -= valor
                if tranferencia:
                    self._historico.transacoes.append(F'Saque de R${valor:.2f}')
                return True
    
    def transfere(self,destino,valor):
        if self.saca(valor,False):
            destino.deposita(valor)
            self._historico.transacoes.append(F'Transferência de R${valor:.2f} para conta {destino.numero}')
            return True
        else:
            return False
        
    def extrato(self):
        print(F'Numero da conta: {self._numero} - Cliente: {self._titular._nome} {self._titular._sobrenome} - saldo atual: R${self._saldo} - limite: R${self._limite}')
    
    """def __str__(self):
        print(F'Numero da conta: {self._numero} - Cliente: {self._titular._nome} {self._titular._sobrenome} - saldo atual: R${self._saldo} - limite: R${self._limite}')"""
