class Pessoa:
    def __init__(self, nome: str, sobrenome: str, idade: int, cpf: str):
        self.nome: str = nome
        self.sobrenome: str = sobrenome
        self.idade: int = idade
        self._cpf: str = cpf
        self._contasBancarias = []

    @property
    def cpf(self):
        return self._cpf
    @cpf.setter
    def cpf(self, valor):
        self._cpf = valor
        
    @property
    def contasBancarias(self):
        return self._contasBancarias
    @contasBancarias.setter
    def contasBancarias(self, valor):
        self._contasBancarias = valor

    def info(self):
        print(f"Nome: {self.nome} {self.sobrenome}\n Idade: {self.idade}\n CPF: {self._cpf}")

    def info_contas(self):
        for conta in self._contasBancarias:
            conta.info()

    @classmethod
    def criar_pessoa(cls):
        print("Cadastro de Pessoa")
        nome = input("Nome: ")
        sobrenome = input("Sobrenome: ")
        idade = int(input("Idade: "))
        cpf = input("CPF: ")
        return cls(nome, sobrenome, idade, cpf)

class Banco:
    def __init__(self, nome: str, cnpj: str, numeroBanco: int):
        self._nome: str = nome
        self._cnpj: str = cnpj
        self._numeroBanco: int = numeroBanco
        self._contasBancarias = []
        self._pessoas = []

    @property
    def nome(self):
        return self._nome
    @nome.setter
    def nome(self, valor):
        self._nome = valor

    @property
    def cnpj(self):
        return self._cnpj
    @cnpj.setter
    def cnpj(self, valor):
        self._cnpj = valor

    @property
    def numeroBanco(self):
        return self._numeroBanco
    @numeroBanco.setter
    def numeroBanco(self, valor):
        self._numeroBanco = valor

    @property
    def contasBancarias(self):
        return self._contasBancarias
    @contasBancarias.setter
    def contasBancarias(self, valor):
        self._contasBancarias = valor

    @property
    def pessoas(self):
        return self._pessoas
    @pessoas.setter
    def pessoas(self, valor):
        self._pessoas = valor

    def info_banco(self):
        print(f"Banco: {self._nome}\n CNPJ: {self._cnpj}\n Número: {self._numeroBanco}")

    def info_contas(self):
        for conta in self._contasBancarias:
            conta.info()

    @classmethod
    def criar_banco(cls):
        print("Cadastro de Banco")
        nome = input("Nome do banco: ")
        cnpj = input("CNPJ: ")
        numeroBanco = int(input("Número do banco: "))
        return cls(nome, cnpj, numeroBanco)

    def criar_conta(self, conta):
        if conta not in self._contasBancarias:
            self._contasBancarias.append(conta)
            print("Conta adicionada ao banco com sucesso.")
        else:
            print("Conta já existe no banco.")

    def fechar_conta(self, conta):
        if conta in self._contasBancarias:
            self._contasBancarias.remove(conta)
            print("Conta removida do banco com sucesso.")
        else:
            print("Conta não encontrada no banco.")

class ContaBancaria:
    def __init__(self, titular: 'Pessoa', banco: 'Banco', numeroConta: int, saldo: float, senha: str):
        self._titular: Pessoa = titular
        self._banco: Banco = banco
        self._numeroConta: int = numeroConta
        self._saldo: float = saldo
        self._senha: str = senha

    def saque(self, valor):
        pass

    def deposito(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        else:
            print("Valor inválido para depósito.")

    def verifica_senha(self, senha):
        return senha == self._senha

    def verifica_senha_input(self):
        senha = input("Digite a senha da conta: ")
        return self.verifica_senha(senha)

    @property
    def numero(self):
        return self._numeroConta
    @numero.setter
    def numero(self, valor):
        if valor > 0:
            self._numeroConta = valor

    @property
    def saldo(self):
        return self._saldo
    @saldo.setter
    def saldo(self, valor):
        if valor >= 0:
            self._saldo = valor

    @property
    def senha(self):
        return self._senha
    @senha.setter
    def senha(self, valor):
        if valor != "":
            self._senha = valor

    def deposito_input(self):
        valor = float(input("Valor do depósito: "))
        self.deposito(valor)

    def saque_input(self):
        valor = float(input("Valor do saque: "))
        self.saque(valor)

class ContaCorrente(ContaBancaria):
    def __init__(self, titular: 'Pessoa', banco: 'Banco', numeroConta: int, saldo: float, senha: str, taxasMensais: float):
        super().__init__(titular, banco, numeroConta, saldo, senha)
        self.taxasMensais: float = taxasMensais

    def info(self):
        print(f"Conta Corrente - Banco: {self._banco.nome}\n Número: {self._numeroConta}\n Titular: {self._titular.nome}\n Saldo: R$ {self._saldo:.2f}\n Taxas: R$ {self.taxasMensais:.2f}")

    def saque(self, valor):
        if valor > 0 and valor <= self._saldo:
            self._saldo -= valor
            print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
        else:
            print("Saldo insuficiente ou valor inválido.")

    def novo_mes(self):
        self._saldo -= self.taxasMensais

    @classmethod
    def criar_conta_corrente(cls, titular, banco):
        print("Criação de Conta Corrente")
        numeroConta = int(input("Número da conta: "))
        saldo = float(input("Saldo: "))
        senha = input("Senha: ")
        taxasMensais = float(input("Taxas mensais: "))
        return cls(titular, banco, numeroConta, saldo, senha, taxasMensais)

class ContaPoupanca(ContaBancaria):
    def __init__(self, titular: 'Pessoa', banco: 'Banco', numeroConta: int, saldo: float, senha: str, rendimento: float, saquesMensais: int):
        super().__init__(titular, banco, numeroConta, saldo, senha)
        self.rendimento: float = rendimento
        self.saquesMensais: int = saquesMensais
        self.saquesRestantes: int = saquesMensais

    def info(self):
        print(f"Conta Poupança - Banco: {self._banco.nome}\n Número: {self._numeroConta}\n Titular: {self._titular.nome}\n Saldo: R$ {self._saldo:.2f}\n Rendimento: {self.rendimento*100:.2f}%\n Saques restantes: {self.saquesRestantes}")

    def saque(self, valor):
        if self.saquesRestantes > 0:
            if valor > 0 and valor <= self._saldo:
                self._saldo -= valor
                self.saquesRestantes -= 1
                print(f"Saque de R$ {valor:.2f} realizado com sucesso. Saques restantes: {self.saquesRestantes}")
            else:
                print("Saldo insuficiente ou valor inválido.")
        else:
            print("Limite de saques do mês atingido.")

    def novo_mes(self):
        self._saldo += self._saldo * self.rendimento
        self.saquesRestantes = self.saquesMensais

    @classmethod
    def criar_conta_poupanca(cls, titular, banco):
        print("Criação de Conta Poupança")
        numeroConta = int(input("Número da conta: "))
        saldo = float(input("Saldo: "))
        senha = input("Senha: ")
        rendimento = float(input("Rendimento mensal: "))
        saquesMensais = 3 
        return cls(titular, banco, numeroConta, saldo, senha, rendimento, saquesMensais)

