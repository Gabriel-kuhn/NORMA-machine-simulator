import norma_compiler
from terminal_cleaner import TerminalOperator
from macro_compiler import start_macro_aux_registers

def main():
    print(".:|=== Simulador de Máquina NORMA ===|:.")

    registers = {}
    command_lines = []

    # Aqui a gente vai ler o programa que vai rodar na nossa máquina NORMA de um arquivo de texto fixo no projeto
    # A primeira linha do arquivo são os valores iniciais dos registradores
    # As demais linhas são referentes as instruções do programa (basicamente o programa em si)
    with open("program.txt", "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]

    # Setando os registradores com os valores do arquivo de texto
    initial_values = list(map(int, lines[0].split()))
    for i, val in enumerate(initial_values):
        # Vamos usar símbolos alfanuméricos para representar os registradores
        # Assim fica mais simples pro usuário. Só que precisamos converter para char
        name = chr(ord('a') + i)
        registers[name] = val

    # Antes de inicarmos o programa precisamos ver se os registradores usados pelo usuário não
    # vão conflitar com os registradores que usamos para as macros
    reserved = set(start_macro_aux_registers())
    conflict = reserved.intersection(registers.keys())
    if conflict:
        print(f"ERRO: Os registradores {', '.join(conflict)} são reservados para uso interno das macros.")
        return

    # Agora adicionamos os auxiliares (se passou na validação)
    for aux in reserved:
        registers[aux] = 0

    # Vamos adicionar a nossa lista de registradores os auxiliares das macros (vão sempre inicializar em 0)
    for aux in start_macro_aux_registers():
        registers[aux] = 0


    # O resto das linhas são o programa que será executado pela máquina
    command_lines = lines[1:]

    print("\n.:|=== Configuração da máquina concluída ===|:.")

    # chamamos nosso compilador para rodar o programa
    norma_compiler.run(registers, command_lines)


if __name__ == "__main__":
    TerminalOperator.clear()
    main()