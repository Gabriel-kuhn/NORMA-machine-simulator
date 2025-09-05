
def run(registers: dict, typed_lines: list):
    
    # Vamos converter as linhas digitas para um formato que nossa máquina possa interpretar corretamente.
    command_lines = convert_typed_lines_to_command_lines(typed_lines)


    # Começa pelo menor rótulo, normalmente é 0 ou 1 mas o usuário pode acabar querendo começar pelo 7...
    program_counter = min(command_lines.keys())

    # Aqui está toda jogada, vamos iniciar somente uma instrução. Faremos o resto recursivo
    # Porque cada instrução nela mesma contém para qual rótulo deve seguir, então ela mesma vai decidir a próxima etapa
    # o try é para a codinção de parada. Na NORMA, quando queremos terminar o programa, nós dizemos que vamos 
    # para o rótulo inexistente, ou nao definido, assim, quando acontecer um OutOfBoundException sabemos que 
    # a instrução está levando para um condição de parada.
    try:
        interpret(registers, command_lines, program_counter)

    except KeyError:
        # Parada do programa quando rótulo não existe
        print("\n=== Execução finalizada ===")
        print("Registradores finais:", registers)




def convert_typed_lines_to_command_lines(typed_lines):
    program = {}
    
    for line in typed_lines:
        if ":" in line:
            # Colocamos em um dicionário o rótulo e a instrução daquele rótulo
            # Para isso vamos separa-los pelo "1:"" que cada linha (rótulo) tem

            # Exemplo:
            # 4: faça sub_b vá_para 1
            # Vai virar {4, faça sub_b vá_para 1}
            label, instruction = line.split(":", 1)
            program[int(label.strip())] = instruction.strip()

            print()
            print(label + " " + instruction)
        
    return program

# Essa função é usada para interpretar cada linha de comando
def interpret(command_line: str):
    ##commands = command_line.split(" ")
    print("commands")
    

# Funções nativas da máquina NORMA

def add_x(registers: dict, reg: int):
    registers[reg] += 1

def sub_x(registers: dict, reg: int):
    if registers[reg] > 0:
        registers[reg] -= 1

def zero_x(registers: dict, reg: int):
    return registers[reg] == 0