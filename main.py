import norma_compiler
from terminal_cleaner import TerminalOperator

def main():
    print(".:|=== Simulador de Máquina NORMA ===|:.")

    registers = {}
    command_lines = []

    # Aqui a gente vai ler o programa que vai rodar na nossa máquina NORMA de um arquivo de texto fixo no projeto
    # A primeira linha do arquivo são os valores iniciais dos registradores
    # As demais linhas são referentes as instruções do programa (basicamente o programa em si)
    with open("program.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Setando os registradores com os valores do arquivo de texto
    initial_values = list(map(int, lines[0].split()))
    for i, val in enumerate(initial_values):
        # Vamos usar símbolos alfanuméricos para representar os registradores
        # Assim fica mais simples pro usuário. Só que precisamos converter para char
        name = chr(ord('a') + i)
        registers[name] = val

    # O resto das linhas são o programa que será executado pela máquina
    command_lines = lines[1:]

    print("\n.:|=== Configuração da máquina concluída ===|:.")

    # chamamos nosso compiler para rodar o programa
    norma_compiler.run(registers, command_lines)


if __name__ == "__main__":
    TerminalOperator.clear()
    main()



# Exemplo de input.txt
# Primeira linha: valores iniciais dos registradores
# Demais linhas: instruções do programa
#
# 3 0
# 1: se zero_b então vá_para 9 senão vá_para 2
# 2: faça add_a vá_para 3
# 3: faça add_a vá_para 4
# 4: faça sub_b vá_para 1
