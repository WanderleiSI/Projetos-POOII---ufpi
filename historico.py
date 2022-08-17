import datetime
class Historico:
    __slots__ = ['_data_abertura','_transacoes']

    def __init__(self):
        self._data_abertura = datetime.datetime.today()
        self._transacoes = []
        #self._teste  = 'teste'
    
    @property
    def data_abertura(self):
        return self._data_abertura
    
    @data_abertura.setter
    def data_abertura(self,data_abertura):
        self._data_abertura = data_abertura
    
    @property
    def transacoes(self):
        return self._transacoes

    @transacoes.setter
    def transacoes(self,transacoes):
        self._transacoes = transacoes

    def imprime(self):
        print("Data de abertura: ",self._data_abertura)
        print('Transações')
        for t in self._transacoes:
            print('- ',t)