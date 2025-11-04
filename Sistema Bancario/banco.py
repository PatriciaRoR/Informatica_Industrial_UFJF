# ===============================================
# ARQUIVO: banco.py
# Propósito: Define a classe Banco, gerenciando contas, senha do gerente e menus de atendimento.
# ===============================================

from conta import Conta  # Importa a classe Conta


class Banco:
    def __init__(self):
        # Dados do Banco
        self.senha_gerente = 123456  # Senha para acesso de funcionário

        # Inicialização com Contas de Teste (Objetos Conta)
        self.contas = []
        self.contas.append(Conta(1, "Joao Silva", 1234, 300.00))
        self.contas.append(Conta(2, "Maria Souza", 4567, 800.00))

        # Contador para garantir números de conta únicos
        self.proximo_numero_conta = 3

    # --- FERRAMENTAS ---
    def busca_conta(self, numero):
        """Busca uma conta pelo número e retorna o objeto Conta ou None."""
        try:
            numero = int(numero)
        except ValueError:
            return None  # Retorna None se o número não for válido

        for conta in self.contas:
            if conta.numero == numero:
                return conta
        return None

    # --- ATENDIMENTO FUNCIONÁRIO ---
    def mudar_senha_gerente(self):
        print("\n--- Mudança de Senha do Gerente ---")
        try:
            nova_senha = int(input("Digite a nova senha numérica: "))
            self.senha_gerente = nova_senha
            print("✅ Senha do Gerente atualizada com sucesso.")
        except ValueError:
            print("❌ Senha inválida. Use apenas números.")

    def cadastrar_cliente(self):
        print("\n--- Cadastro de Novo Cliente ---")

        novo_numero = self.proximo_numero_conta
        self.proximo_numero_conta += 1

        titular = input("Nome do Titular: ")

        try:
            senha = int(input("Senha da Conta (somente números): "))
            saldo = float(input("Saldo Inicial (ex: 100.00): R$ "))
        except ValueError:
            print("❌ Entrada inválida para senha ou saldo. Cadastro cancelado.")
            self.proximo_numero_conta -= 1  # Volta o contador
            return

        # Cria o novo objeto Conta e adiciona
        nova_conta = Conta(novo_numero, titular, senha, saldo)
        self.contas.append(nova_conta)

        print(f"✅ Conta {novo_numero} para {titular} cadastrada com sucesso!")

    def atendimento_funcionario(self):
        print("\n--- Acesso Funcionário ---")
        try:
            senha_digitada = int(input("Digite a senha: "))
        except ValueError:
            print("❌ Senha deve ser um número.")
            return

        if senha_digitada == self.senha_gerente:
            print("✅ Acesso concedido!")
            while True:
                print("\nOpções do Funcionário:")
                print("1 - Mudar senha do Gerente")
                print("2 - Cadastrar novo Cliente")
                print("3 - Voltar ao Menu Principal")

                opc = input("Opção: ")

                if opc == '1':
                    self.mudar_senha_gerente()
                elif opc == '2':
                    self.cadastrar_cliente()
                elif opc == '3':
                    break
                else:
                    print("❌ Opção inválida.")
        else:
            print("❌ Senha incorreta. Acesso negado.")

    # --- ATENDIMENTO CLIENTE ---
    def atendimento_cliente(self):
        print("\n--- Atendimento ao Cliente ---")

        num_conta_str = input("Digite o número da sua conta: ")
        conta = self.busca_conta(num_conta_str)

        if conta is None:
            print("❌ Conta não encontrada.")
            return

        print(f"Olá, {conta.titular}!")

        while True:
            print("\nOpções de Transação:")
            print("1 - Ver Saldo")
            print("2 - Realizar Saque")
            print("3 - Realizar Depósito")
            print("4 - Voltar ao Menu Principal")

            opc = input("Escolha a operação: ")

            try:
                if opc == '1':
                    senha_digitada = input("Digite a senha: ")
                    saldo = conta.ver_saldo(senha_digitada)
                    if saldo != -1:
                        print(f"💰 Seu saldo é: R$ {saldo:.2f}")

                elif opc == '2':
                    senha_digitada = input("Digite a senha: ")
                    valor = float(input("Valor do saque: R$ "))
                    conta.sacar(senha_digitada, valor)

                elif opc == '3':
                    valor = float(input("Valor do depósito: R$ "))
                    conta.depositar(valor)

                elif opc == '4':
                    break

                else:
                    print("❌ Opção inválida.")
            except ValueError:
                print("❌ Valor digitado é inválido (use apenas números).")
