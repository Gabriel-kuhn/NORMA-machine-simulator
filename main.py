import norma_compiler

def main():
    print(".:|=== Simulador de Máquina NORMA ===|:.")

    # Primeiro vamos pedir ao usuário a quantidade de registradores que ele vai precisar usar
    register_qnt = int(input("Digite a quantidade de registradores: "))

    # Loop para preencher os valores dos registradores
    registers = {}
    for i in range(register_qnt):
        # Os registradores serão simbolizados por números, fica mais simples pra gente
        start_value = int(input(f"Digite um valor inicial para o registrador {i}: "))
        registers[i] = start_value

    # Aqui o usuário pode colar ou digitar linha por linha o comando para rodar no simulador
    # Para encerrar, basta dar ENTER vazio
    print("\nVocê pode digitar linha por linha ou colar o código inteiro,")
    print("quando terminar dê ENTER sem conteúdo.\nDigite o script: ")
    command_lines = []
    while True:
        line = input()
        if not line.strip():
            break
        command_lines.append(line.strip())

    print("\n.:|=== Configuração da máquina concluída ===|:.")
    print("Registradores:", registers)
    print("Linhas de comando:")
    for line in command_lines:
        print("  ", line)

    # TODO apagar a linha de teste
    test_lines = ["1: se zero_b então vá_para 9 senão vá_para 2",
"2: faça add_a vá_para 3",
"3: faça add_a vá_para 4",
"4: faça sub_b vá_para 1"]
    
    norma_compiler.run(registers, test_lines)


if __name__ == "__main__":
    main()



# 1: se zero_b então vá_para 9 senão vá_para 2
# 2: faça add_a vá_para 3
# 3: faça add_a vá_para 4
# 4: faça sub_b vá_para 1