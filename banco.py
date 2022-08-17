class Banco:
    __slots__ = ['_contas']

    def __init__(self):
        self._contas = []

    def cadastra(self,conta):
        existe = self.busca(conta.cpf)
        if (existe == None):
            self._contas.append(conta)
            return True
        else:
            return False

    def busca(self,cpf = None,numeroConta = False,numero = None):
        if numeroConta:
            for conta in self._contas:
                if conta.numero == numero:
                    return conta
            return None
        else:
            for conta in self._contas:
                if conta.cpf == cpf:
                    return conta
            return None

    @property
    def contas(self):
        return self._contas