def main():
    print("=== Simulador de Máquina NORMA ===")

    # Primeiro vamos pedir ao usuário a quantidade de registradores que ele vai precisar usar
    registersQnt = int(input("Enter the number of registers: "))

    # Loop pra ele preencher os valores dos registradores
    registers = {}
    for i in range(registersQnt):
        # Os registradores serão simbolizados por números, fica mais simples pra gente
        startValue = int(input(f"Digite um valor inicial para o registrador {i}: "))
        registers[i] = startValue

    # Aqui o usuário vai colcar, ou se ele quiser digitar, o comando pra rodar no nosso simulador de máquina normal

    # Fiz com que ele pudesse só colar todo script ou se ele quiser ficar digitando e dando ENTER, também funciona.
    # Dai pra para de entrar código, final do código, ele da um ENTER vazio. 
    print("\nVocê pode digitar linha por linha ou colar o código inteiro, quando terminar dê ENTER sem conteúdo \nDigite o script: ")
    program_lines = []
    while True:
        line = input()
        if not line.strip():
            break
        program_lines.append(line.strip())

    
    print("\n=== Configuração da máquina concluída ===")
    print("Registradores: ", registers)
    print("Linhas de comando: ")
    for line in program_lines:
        print("  ", line)


if __name__ == "__main__":
    main()
