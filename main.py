from classes import ContaBancaria,ContaCorrente,ContaPoupanca,Banco,Pessoa
class SistemaBancario:
    def __init__(self):
        self.bancos = []

    def carregar_dados(self):
        self.carregar_bancos()
        self.carregar_pessoas()
        self.carregar_contas()

    def carregar_bancos(self):
        try:
            with open('bancos.csv', 'r', encoding='utf-8') as arquivo:
                arquivo.readline()
                for linha in arquivo:
                    linha = linha.strip()
                    if linha:
                        dados = linha.split(',')
                        nome = dados[0]
                        cnpj = dados[1]
                        numeroBanco = int(dados[2])
                        banco = Banco(nome, cnpj, numeroBanco)
                        self.bancos.append(banco)
        except FileNotFoundError:
            print("Arquivo bancos.csv não encontrado.")

    def carregar_pessoas(self):
        try:
            with open('pessoas.csv', 'r', encoding='utf-8') as arquivo:
                arquivo.readline()
                for linha in arquivo:
                    linha = linha.strip()
                    if linha:
                        dados = linha.split(',')
                        nome = dados[0]
                        sobrenome = dados[1]
                        idade = int(dados[2])
                        cpf = dados[3]
                        pessoa = Pessoa(nome, sobrenome, idade, cpf)
                        numeroBanco = int(dados[4]) if len(dados) > 4 else 1
                        for banco in self.bancos:
                            if banco.numeroBanco == numeroBanco:
                                banco.pessoas.append(pessoa)
        except FileNotFoundError:
            print("Arquivo pessoas.csv não encontrado.")

    def carregar_contas(self):
        try:
            with open('contas.csv', 'r', encoding='utf-8') as arquivo:
                arquivo.readline()
                for linha in arquivo:
                    linha = linha.strip()
                    if linha:
                        dados = linha.split(',')
                        tipo = dados[0]
                        cpf = dados[1]
                        numeroBanco = int(dados[2])
                        numeroConta = int(dados[3])
                        saldo = float(dados[4])
                        senha = dados[5]
                        bancoachado = None
                        for banco in self.bancos:
                            if banco.numeroBanco == numeroBanco:
                                bancoachado = banco
                        if bancoachado:
                            pessoaachada = None
                            for pessoa in bancoachado.pessoas:
                                if pessoa.cpf == cpf:
                                    pessoaachada = pessoa
                            if pessoaachada:
                                if tipo == 'corrente':
                                    taxasMensais = float(dados[6])
                                    conta = ContaCorrente(pessoaachada, bancoachado, numeroConta, saldo, senha, taxasMensais)
                                elif tipo == 'poupanca':
                                    rendimento = float(dados[6])
                                    saquesMensais = int(dados[7])
                                    saquesRestantes = int(dados[8])
                                    conta = ContaPoupanca(pessoaachada, bancoachado, numeroConta, saldo, senha, rendimento, saquesMensais)
                                    conta.saquesRestantes = saquesRestantes
                                pessoaachada.contasBancarias.append(conta)
                                bancoachado.contasBancarias.append(conta)
        except FileNotFoundError:
            print("Arquivo contas.csv não encontrado.")

    def salvar_dados(self):
        self.salvar_bancos()
        self.salvar_pessoas()
        self.salvar_contas()

    def salvar_bancos(self):
        with open('bancos.csv', 'w', encoding='utf-8') as arquivo:
            arquivo.write("nome,cnpj,nro_banco\n")
            for banco in self.bancos:
                arquivo.write(f"{banco.nome},{banco.cnpj},{banco.numeroBanco}\n")

    def salvar_pessoas(self):
        with open('pessoas.csv', 'w', encoding='utf-8') as arquivo:
            arquivo.write("nome,sobrenome,idade,cpf,nro_banco\n")
            for banco in self.bancos:
                for pessoa in banco.pessoas:
                    arquivo.write(f"{pessoa.nome},{pessoa.sobrenome},{pessoa.idade},{pessoa.cpf},{banco.numeroBanco}\n")

    def salvar_contas(self):
        with open('contas.csv', 'w', encoding='utf-8') as arquivo:
            arquivo.write("tipo,cpf,nro_banco,numero,saldo,senha,taxasrendimento,saquesmensais,saquesrestantes\n")
            for banco in self.bancos:
                for conta in banco.contasBancarias:
                    if isinstance(conta, ContaCorrente):
                        arquivo.write(f"corrente,{conta._titular.cpf},{banco.numeroBanco},{conta._numeroConta},{conta._saldo},{conta._senha},{conta.taxasMensais}\n")
                    elif isinstance(conta, ContaPoupanca):
                        arquivo.write(f"poupanca,{conta._titular.cpf},{banco.numeroBanco},{conta._numeroConta},{conta._saldo},{conta._senha},{conta.rendimento},{conta.saquesMensais},{conta.saquesRestantes}\n")

    def cadastrar_banco(self):
        banco = Banco.criar_banco()
        self.bancos.append(banco)
        self.salvar_dados()
        print("Banco cadastrado com sucesso")

    def buscar_banco(self):
        codigo = int(input("Código do banco: "))
        bancoachado = None
        for banco in self.bancos:
            if banco.numeroBanco == codigo:
                bancoachado = banco
        if bancoachado:
            return bancoachado
        else:
            print("Banco não encontrado.")

    def buscar_pessoa(self, bancoachado):
        cpf = input("CPF do titular: ")
        pessoaachada = None
        for pessoa in bancoachado.pessoas:
            if pessoa.cpf == cpf:
                pessoaachada = pessoa
        if pessoaachada:
            return pessoaachada
        else:
            print("Pessoa não encontrada.")

    def cadastrar_pessoa(self):
        bancoachado = self.buscar_banco()
        if bancoachado:
            pessoa = Pessoa.criar_pessoa()
            bancoachado.pessoas.append(pessoa)
            self.salvar_dados()
            print("Pessoa cadastrada com sucesso")

    def criar_conta_corrente(self):
        bancoachado = self.buscar_banco()
        if bancoachado:
            pessoaachada = self.buscar_pessoa(bancoachado)
            if pessoaachada:
                contaachada = ContaCorrente.criar_conta_corrente(pessoaachada, bancoachado)
                pessoaachada.contasBancarias.append(contaachada)
                bancoachado.criar_conta(contaachada)
                self.salvar_dados()
                print("Conta corrente criada com sucesso")

    def criar_conta_poupanca(self):
        bancoachado = self.buscar_banco()
        if bancoachado:
            pessoaachada = self.buscar_pessoa(bancoachado)
            if pessoaachada:
                contaachada = ContaPoupanca.criar_conta_poupanca(pessoaachada, bancoachado)
                pessoaachada.contasBancarias.append(contaachada)
                bancoachado.criar_conta(contaachada)
                self.salvar_dados()
                print("Conta poupança criada com sucesso")

    def listar_contas_cliente(self):
        cpf = input("CPF do cliente: ")
        pessoaachada = None
        encontra = False
        for banco in self.bancos:
            if not encontra:
                for pessoa in banco.pessoas:
                    if not encontra and pessoa.cpf == cpf:
                        pessoaachada = pessoa
                        encontra = True
        
        if pessoaachada:
            if len(pessoaachada.contasBancarias) > 0:
                print(f"Contas de {pessoaachada.nome} {pessoaachada.sobrenome}:")
                print('-------------------------------')
                pessoaachada.info_contas()
            else:
                print("Cliente sem contas.")
        else:
            print("Pessoa não encontrada em nenhum banco.")

    def listar_contas_banco(self):
        bancoachado = self.buscar_banco()
        if bancoachado:
            bancoachado.info_contas()

    def buscar_conta(self):
        bancoachado = self.buscar_banco()
        if bancoachado:
            numeroConta = int(input("Número da conta: "))
            contaachada = None
            for conta in bancoachado.contasBancarias:
                if conta._numeroConta == numeroConta:
                    contaachada = conta
            if contaachada:
                return contaachada
            else:
                print("Conta não encontrada.")

    def depositar(self):
        contaachada = self.buscar_conta()
        if contaachada:
            contaachada.deposito_input()
            self.salvar_dados()

    def sacar(self):
        contaachada = self.buscar_conta()
        if contaachada:
            if contaachada.verifica_senha_input():
                contaachada.saque_input()
                self.salvar_dados()
            else:
                print("Senha incorreta.")

    def simular_novo_mes(self):
        contaachada = self.buscar_conta()
        if contaachada:
            contaachada.novo_mes()
            self.salvar_dados()
            print("Novo mês simulado para a conta.")

    def fechar_conta(self):
        bancoachado = self.buscar_banco()
        if bancoachado:
            numeroConta = int(input("Número da conta a ser fechada: "))
            contaachada = None
            for conta in bancoachado.contasBancarias:
                if conta._numeroConta == numeroConta:
                    contaachada = conta
            if contaachada:
                contaachada._titular.contasBancarias.remove(contaachada)
                bancoachado.fechar_conta(contaachada)
                self.salvar_dados()
                print("Conta fechada com sucesso")
            else:
                print("Conta não encontrada.")

    def menu(self):
        self.carregar_dados() 
        continuar = True
        while continuar:
            print('-------------------------------')
            print('1 - Cadastrar banco')
            print('2 - Cadastrar pessoa em um banco')
            print('3 - Criar conta corrente')
            print('4 - Criar conta poupança')
            print('5 - Listar contas de um cliente')
            print('6 - Listar contas de um banco')
            print('7 - Depositar')
            print('8 - Sacar')
            print('9 - Simular passagem de mês')
            print('10 - Fechar conta')
            print('0 - Sair')
            print('-------------------------------')
            opcao = input('Escolha uma opção: ')

            if opcao == '1':
                self.cadastrar_banco()
            elif opcao == '2':
                self.cadastrar_pessoa()
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
                self.simular_novo_mes()
            elif opcao == '10':
                self.fechar_conta()
            elif opcao == '0':
                print("Sistema encerrado.")
                continuar = False
            else:
                print("Opção inválida.")

if __name__ == '__main__':
    sistema = SistemaBancario()
    sistema.menu() 
   