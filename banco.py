import sys

class BancoSistema:
    def __init__(self):
        self.pessoas = []
        self.bancos = []
        self.carregar_dados('dados.csv')

    def menu(self):
        while True:
            print('-------------------------------')
            print('1 - Cadastrar pessoa')
            print('2 - Cadastrar banco')
            print('3 - Criar conta corrente')
            print('4 - Criar conta poupança')
            print('5 - Listar contas de um cliente')
            print('6 - Listar contas de um banco')
            print('7 - Depositar')
            print('8 - Sacar')
            print('9 - Simular passagem de mês')
            print('0 - Sair')
            print('-------------------------------')
            opcao = input('Escolha uma opção: ')
            if opcao == '1':
                self.cadastrar_pessoa()
            elif opcao == '2':
                self.cadastrar_banco()
            elif opcao == '3':
                self.criar_conta_corrente()
            elif opcao == '4':
                self.criar_conta_poupanca()
            elif opcao == '5':
                self.listar_contas_cliente()
            elif opcao == '6':
                self.listar_contas_banco()
            elif opcao == '7':
                self.depositar()
            elif opcao == '8':
                self.sacar()
            elif opcao == '9':
                self.novo_mes()
            elif opcao == '0':
                self.salvar_dados('dados.csv')
                print('Sistema encerrado.')
                break
            else:
                print('Opção inválida.')

    def cadastrar_pessoa(self):
        nome = input("Nome: ")
        sobrenome = input("Sobrenome: ")
        idade = int(input("Idade: "))
        cpf = input("CPF: ")
        pessoa = Pessoa(nome, sobrenome, idade, cpf)
        self.pessoas.append(pessoa)
        print("Pessoa cadastrada com sucesso!")

    def cadastrar_banco(self):
        nome = input("Nome do banco: ")
        cnpj = input("CNPJ: ")
        nro_banco = int(input("Número do banco: "))
        banco = Banco(nome, cnpj, nro_banco)
        self.bancos.append(banco)
        print("Banco cadastrado com sucesso!")

    def criar_conta_corrente(self):
        print("Criação de Conta Corrente")
        cpf = input("CPF do titular: ")
        nro_banco = int(input("Número do banco: "))
        pessoaachada = None
        bancoachado = None
        for pessoa in self.pessoas:
            if pessoa.cpf == cpf:
                pessoaachada = pessoa
        for banco in self.bancos:
            if banco.nro_banco == nro_banco:
                bancoachado = banco
        if pessoaachada and bancoachado:
            numero = int(input("Número da conta: "))
            saldo = float(input("Saldo inicial: "))
            senha = input("Senha da conta: ")
            taxas = float(input("Taxas mensais: "))
            conta = ContaCorrente(pessoaachada, bancoachado, numero, saldo, senha, taxas)
            pessoaachada.contas.append(conta)
            bancoachado.contas.append(conta)
            print("Conta corrente criada com sucesso!")
        else:
            print("Pessoa ou banco não encontrados.")

    def criar_conta_poupanca(self):
        print("Criação de Conta Poupança")
        cpf = input("CPF do titular: ")
        nro_banco = int(input("Número do banco: "))
        pessoaachada = None
        bancoachado = None
        for pessoa in self.pessoas:
            if pessoa.cpf == cpf:
                pessoaachada = pessoa
        for banco in self.bancos:
            if banco.nro_banco == nro_banco:
                bancoachado = banco
        if pessoaachada and bancoachado:
            numero = int(input("Número da conta: "))
            saldo = float(input("Saldo inicial: "))
            senha = input("Senha da conta: ")
            rendimento = float(input("Rendimento mensal (ex: 0.01 para 1%): "))
            saques_mensais = int(input("Saques mensais permitidos: "))
            conta = ContaPoupanca(pessoaachada, bancoachado, numero, saldo, senha, rendimento, saques_mensais, saques_mensais)
            pessoaachada.contas.append(conta)
            bancoachado.contas.append(conta)
            print("Conta poupança criada com sucesso!")
        else:
            print("Pessoa ou banco não encontrados.")

    def listar_contas_cliente(self):
        cpf = input("CPF do cliente: ").strip()
        pessoaachada = None
        for pessoa in self.pessoas:
            if pessoa.cpf == cpf:
                pessoaachada = pessoa
        if pessoaachada:
            if pessoaachada.contas:
                print(f"Contas de {pessoaachada.nome} {pessoaachada.sobrenome}:")
                for conta in pessoaachada.contas:
                    print(conta)
            else:
                print("Cliente sem contas.")
        else:
            print("Pessoa não encontrada.")

    def listar_contas_banco(self):
        nro_banco = int(input("Número do banco: "))
        bancoachado = None
        for banco in self.bancos:
            if banco.nro_banco == nro_banco:
                bancoachado = banco
        if bancoachado:
            print(f"Contas do banco {bancoachado.nome}:")
            for conta in bancoachado.contas:
                print(conta)
        else:
            print("Banco não encontrado.")

    def depositar(self):
        nro_banco = int(input("Número do banco: "))
        numero_conta = int(input("Número da conta: "))
        bancoachado = None
        contaachada = None
        for banco in self.bancos:
            if banco.nro_banco == nro_banco:
                bancoachado = banco
        if bancoachado:
            for conta in bancoachado.contas:
                if conta.numero == numero_conta:
                    contaachada = conta
        if contaachada:
            valor = float(input("Valor do depósito: "))
            contaachada.deposito(valor)
        else:
            print("Conta não encontrada.")

    def sacar(self):
        nro_banco = int(input("Número do banco: "))
        numero_conta = int(input("Número da conta: "))
        bancoachado = None
        contaachada = None
        for banco in self.bancos:
            if banco.nro_banco == nro_banco:
                bancoachado = banco
        if bancoachado:
            for conta in bancoachado.contas:
                if conta.numero == numero_conta:
                    contaachada = conta
        if contaachada:
            senha = input("Digite a senha da conta: ")
            if contaachada.verifica_senha(senha):
                valor = float(input("Valor do saque: "))
                contaachada.saque(valor)
            else:
                print("Senha incorreta.")
        else:
            print("Conta não encontrada.")

    def novo_mes(self):
        nro_banco = int(input("Número do banco: "))
        numero_conta = int(input("Número da conta: "))
        bancoachado = None
        contaachada = None
        for banco in self.bancos:
            if banco.nro_banco == nro_banco:
                bancoachado = banco
        if bancoachado:
            for conta in bancoachado.contas:
                if conta.numero == numero_conta:
                    contaachada = conta
        if contaachada:
            contaachada.novo_mes()
            print("Novo mês simulado para a conta.")
        else:
            print("Conta não encontrada.")

    def salvar_dados(self, arquivo_nome):
        bancos_salvos = set()
        with open(arquivo_nome, 'w', encoding='utf-8') as arquivo:
            for pessoa in self.pessoas:
                arquivo.write('#\n')
                arquivo.write(f'{pessoa.nome},{pessoa.sobrenome},{pessoa.idade},{pessoa.cpf}\n')
                bancos_escritos = set()
                for conta in pessoa.contas:
                    banco = conta.banco
                    if banco not in bancos_escritos:
                        arquivo.write(f'{banco.nome},{banco.cnpj},{banco.nro_banco}\n')
                        bancos_escritos.add(banco)
                        bancos_salvos.add(banco)
                for conta in pessoa.contas:
                    if isinstance(conta, ContaCorrente):
                        arquivo.write(f'{conta.numero},{conta.saldo:.2f},{conta.senha},{conta.taxas_mensais:.2f}\n')
                    elif isinstance(conta, ContaPoupanca):
                        arquivo.write(f'{conta.numero},{conta.saldo:.2f},{conta.senha},{conta.rendimento:.4f},{conta.saques_mensais},{conta.saques_restantes}\n')
            for banco in self.bancos:
                if banco not in bancos_salvos:
                    arquivo.write('#\n')
                    arquivo.write(',,,\n')
                    arquivo.write(f'{banco.nome},{banco.cnpj},{banco.nro_banco}\n')

    @classmethod
    def carregar_tres_arquivos(cls, pessoas_arquivo, bancos_arquivo, contas_arquivo):
        sistema = cls.__new__(cls)
        sistema.pessoas = []
        sistema.bancos = []
        try:
            with open(pessoas_arquivo, 'r', encoding='utf-8') as arquivo:
                next(arquivo)
                for linha in arquivo:
                    nome, sobrenome, idade, cpf = linha.strip().split(',')
                    pessoa = Pessoa(nome, sobrenome, int(idade), cpf)
                    sistema.pessoas.append(pessoa)
        except FileNotFoundError:
            print('Arquivo de pessoas não encontrado')
        try:
            with open(bancos_arquivo, 'r', encoding='utf-8') as arquivo:
                next(arquivo)
                for linha in arquivo:
                    nome, cnpj, nro_banco = linha.strip().split(',')
                    banco = Banco(nome, cnpj, int(nro_banco))
                    sistema.bancos.append(banco)
        except FileNotFoundError:
            print('Arquivo de bancos não encontrado')
        try:
            with open(contas_arquivo, 'r', encoding='utf-8') as arquivo:
                next(arquivo)
                for linha in arquivo:
                    dados = linha.strip().split(',')
                    if len(dados) < 7:
                        continue
                    tipo, cpf, nro_banco, numero, saldo, senha = dados[:6]
                    nro_banco = int(nro_banco)
                    numero = int(numero)
                    saldo = float(saldo)
                    pessoa = None
                    banco = None
                    for p in sistema.pessoas:
                        if p.cpf == cpf:
                            pessoa = p
                    for b in sistema.bancos:
                        if b.nro_banco == nro_banco:
                            banco = b
                    if pessoa is not None and banco is not None:
                        if tipo == 'corrente':
                            taxas = float(dados[6])
                            conta = ContaCorrente(pessoa, banco, numero, saldo, senha, taxas)
                        elif tipo == 'poupanca':
                            if len(dados) < 9:
                                continue
                            rendimento = float(dados[6])
                            saques_mensais = int(dados[7])
                            saques_restantes = int(dados[8])
                            conta = ContaPoupanca(pessoa, banco, numero, saldo, senha, rendimento, saques_mensais, saques_restantes)
                        pessoa.contas.append(conta)
                        banco.contas.append(conta)
        except FileNotFoundError:
            print('Arquivo de contas não encontrado')
        return sistema

class Pessoa:
    def __init__(self, nome, sobrenome, idade, cpf):
        self._nome = nome
        self._sobrenome = sobrenome
        self._idade = idade
        self._cpf = cpf
        self.contas = []

    @property
    def nome(self):
        return self._nome

    @property
    def sobrenome(self):
        return self._sobrenome

    @property
    def idade(self):
        return self._idade

    @property
    def cpf(self):
        return self._cpf

class Banco:
    def __init__(self, nome, cnpj, nro_banco):
        self._nome = nome
        self._cnpj = cnpj
        self._nro_banco = nro_banco
        self.contas = []

    @property
    def nome(self):
        return self._nome

    @property
    def cnpj(self):
        return self._cnpj

    @property
    def nro_banco(self):
        return self._nro_banco

class ContaBancaria:
    def __init__(self, titular, banco, numero, saldo, senha):
        self.titular = titular
        self.banco = banco
        self.numero = numero
        self.saldo = saldo
        self.senha = senha

    def verifica_senha(self, senha):
        return self.senha == senha

    def saque(self, valor):
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            print('Saque realizado com sucesso!')
        else:
            print('Saldo insuficiente ou valor inválido.')

    def deposito(self, valor):
        if valor > 0:
            self.saldo += valor
            print('Depósito realizado com sucesso!')
        else:
            print('Valor inválido.')

class ContaCorrente(ContaBancaria):
    def __init__(self, titular, banco, numero, saldo, senha, taxas_mensais):
        super().__init__(titular, banco, numero, saldo, senha)
        self._taxas_mensais = taxas_mensais

    @property
    def taxas_mensais(self):
        return self._taxas_mensais

    def novo_mes(self):
        self.saldo -= self.taxas_mensais

    def __str__(self):
        return f"Conta Corrente - Banco: {self.banco.nome}\n Número: {self.numero}\n Titular: {self.titular.nome}\n Saldo: R$ {self.saldo:.2f}\n Taxas: R$ {self.taxas_mensais:.2f}"

class ContaPoupanca(ContaBancaria):
    def __init__(self, titular, banco, numero, saldo, senha, rendimento, saques_mensais, saques_restantes):
        super().__init__(titular, banco, numero, saldo, senha)
        self._rendimento = rendimento
        self._saques_mensais = saques_mensais
        self._saques_restantes = saques_restantes

    @property
    def rendimento(self):
        return self._rendimento

    @property
    def saques_mensais(self):
        return self._saques_mensais

    @property
    def saques_restantes(self):
        return self._saques_restantes

    def novo_mes(self):
        self.saldo += self.saldo * self.rendimento
        self._saques_restantes = self.saques_mensais

    def saque(self, valor):
        if self._saques_restantes > 0 and valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            self._saques_restantes -= 1
            print('Saque realizado com sucesso!')
        else:
            print('Limite de saques atingido ou saldo insuficiente.')

    def __str__(self):
        return f"Conta Poupança - Banco: {self.banco.nome}\n Número: {self.numero}\n Titular: {self.titular.nome}\n Saldo: R$ {self.saldo:.2f}\n Rendimento: {self.rendimento:.2%}"

if __name__ == '__main__':
    sistema = BancoSistema.carregar_tres_arquivos('pessoas.csv', 'bancos.csv', 'contas.csv')
    sistema.menu() 