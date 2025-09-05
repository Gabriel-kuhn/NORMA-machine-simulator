from norma_commands import NormaCommand


def run(registers: dict, typed_lines: list):
    
    # Vamos converter as linhas digitas para um formato que nossa máquina possa interpretar corretamente.
    program = convert_typed_lines_to_command_lines(typed_lines)


    # Começa pelo menor rótulo, normalmente é 0 ou 1 mas o usuário pode acabar querendo começar pelo 7...
    program_counter = min(program.keys())

    # Aqui está toda jogada, vamos iniciar somente uma instrução. Faremos o resto recursivo
    # Porque cada instrução nela mesma contém para qual rótulo deve seguir, então ela mesma vai decidir a próxima etapa
    # o try é para a codinção de parada. Na NORMA, quando queremos terminar o programa, nós dizemos que vamos 
    # para o rótulo inexistente, ou nao definido, assim, quando acontecer um OutOfBoundException sabemos que 
    # a instrução está levando para um condição de parada.
    try:
        interpret(registers, program, program_counter)

    except KeyError:
        # Parada do programa quando rótulo não existe
        print("\n.:|=== Execução finalizada ===|:.")
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
        
    return program



# Essa função é usada para interpretar cada linha de comando
def interpret(registers: dict, program: dict, current_label: int):
    
    # pega a instrução pelo rótulo atual (current_label)
    instruction = program[current_label]
    tokenList = instruction.split()

    print(f"\n{current_label}: {instruction}")
    print(registers)

    command_token = get_command_token(tokenList)
    
    match command_token:

        case NormaCommand.ZERO:
            reg = tokenList[1][-1]  # pega a letra do registrador (segundo item zero_b e pega ultimo digito b) assim sabemos o registrador da operação 
            next_label_true = int(tokenList[4])   # registrador quando for verdadeiro
            next_label_false = int(tokenList[7])  # registrador quando for falso

            if zero_x(registers, reg):
                next_label = next_label_true
            else:
                next_label = next_label_false
            
        case NormaCommand.ADD:
            reg = tokenList[1][-1]  # pega a letra do registrador (segundo item add_b e pega ultimo digito b) assim sabemos o registrador da operação 
            add_x(registers, reg)
            next_label = int(tokenList[3])  # pega o rótulo de "vá_para"


        case NormaCommand.SUB:
            reg = tokenList[1][-1] # pega a letra do registrador (segundo item sub_b e pega ultimo digito b) assim sabemos o registrador da operação 
            sub_x(registers, reg)
            next_label = int(tokenList[3])  # pega o rótulo de "vá_para"


        # Como se fosse o else do java, serve para tratar valores inesperados nos cases anteriores
        case _:
            print(next_label)
            raise ValueError(f"Comando inválido: {command_token}")


    # Chamada recursiva para a próxima instrução referente ao valor de next_label
    interpret(registers, program, next_label)

    


# .:| === Função para pegar o token do comando |:. === 
def get_command_token(tokenList: list):

    zero_command = next((t for t in tokenList if "zero_" in t), None)
    add_command  = next((t for t in tokenList if "add_" in t), None)
    sub_command  = next((t for t in tokenList if "sub_" in t), None)

    if (zero_command):
        return NormaCommand.ZERO
    
    if (add_command):
        return NormaCommand.ADD
    
    if (sub_command):
        return NormaCommand.SUB

    return None



# .:| === Funções nativas da máquina NORMA === |:.

def add_x(registers: dict, reg: int):
    registers[reg] += 1

def sub_x(registers: dict, reg: int):
    if registers[reg] > 0:
        registers[reg] -= 1

def zero_x(registers: dict, reg: int):
    return registers[reg] == 0