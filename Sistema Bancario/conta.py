# ===============================================
# ARQUIVO: conta.py
# Propósito: Define a classe Conta e seus métodos de transação.
# ===============================================

class Conta:
    def __init__(self, numero, titular, senha, saldo_inicial):
        self.numero = numero
        self.titular = titular
        # Armazenando a senha (como int ou str, mas mantendo a consistência)
        self.senha = senha
        self.saldo = saldo_inicial

        print(f"Conta {self.numero} criada para {self.titular}.")

    # --- MÉTODOS DE OPERAÇÃO ---

    def depositar(self, valor):
        """Realiza um depósito na conta."""
        if valor > 0:
            self.saldo += valor
            print(f"✅ Depósito de R$ {valor:.2f} realizado com sucesso.")
            return True
        else:
            print("❌ O valor do depósito deve ser positivo.")
            return False

    def sacar(self, senha_digitada, valor):
        """Realiza um saque, verificando a senha e o saldo."""
        # Note: A conversão para int é importante se a senha for armazenada como int
        if int(senha_digitada) != self.senha:
            print("❌ Senha incorreta. Saque negado.")
            return False

        if valor <= 0:
            print("❌ O valor do saque deve ser positivo.")
            return False

        if valor > self.saldo:
            print("❌ Saldo insuficiente.")
            return False

        # Se passou nas verificações
        self.saldo -= valor
        print(f"✅ Saque de R$ {valor:.2f} realizado com sucesso.")
        return True

    def ver_saldo(self, senha_digitada):
        """Retorna o saldo se a senha estiver correta."""
        # Note: A conversão para int é importante se a senha for armazenada como int
        if int(senha_digitada) == self.senha:
            return self.saldo
        else:
            print("❌ Senha incorreta. Acesso negado.")
            return -1  # Retorna -1 para sinalizar falha
