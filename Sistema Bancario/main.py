# ===============================================
# ARQUIVO: main.py
# Propósito: Ponto de entrada do programa e Menu Principal.
# ===============================================

from banco import Banco  # Importa a classe Banco


def main():
    # Cria a instância principal do Banco
    banco = Banco()

    while True:
        print("\n\n--- 🏦 Sistema Bancário Principal 🏦 ---")
        print("1) Atendimento ao Cliente")
        print("2) Atendimento ao Funcionário")
        print("3) Sair")

        opc = input("Escolha a opção: ")

        if opc == '1':
            # Chama o menu de cliente (que cuidará de todo o login e transações)
            banco.atendimento_cliente()
        elif opc == '2':
            # Chama o menu de funcionário (que cuidará do login e opções)
            banco.atendimento_funcionario()
        elif opc == '3':
            print("Obrigado por usar o sistema. Até logo!")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")


# Garante que a função main() seja o ponto de partida quando o arquivo é executado
if __name__ == "__main__":
    main()
