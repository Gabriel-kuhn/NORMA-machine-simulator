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

    # Parada do programa quando rótulo não existe
    except KeyError as error:
        # Como o nosso erro ocorre quando é usado um valor fora do array de operações
        # Esse endereço fora dos limites (condição de parada) é o rótulo final do programa    
        program_counter = error.args[0]
        computed_registers = tuple(registers.values())
        print(f"({program_counter}, {computed_registers})")




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

    command_token = get_command_token(tokenList)
    
    match command_token:

        case NormaCommand.ZERO:
            reg = tokenList[1][-1]  # pega a letra do registrador (segundo item zero_b e pega ultimo digito b) assim sabemos o registrador da operação 
            next_label_true = int(tokenList[4])   # registrador quando for verdadeiro
            next_label_false = int(tokenList[7])  # registrador quando for falso

            if zero_x(registers, reg):
                next_label = next_label_true
                computed_op_desc = f"em {current_label}, como {reg} = 0, desviou para {next_label}"
            else:
                next_label = next_label_false
                computed_op_desc = f"em {current_label}, como {reg} <> 0, desviou para {next_label}"
            
        case NormaCommand.ADD:
            reg = tokenList[1][-1]  # pega a letra do registrador (segundo item add_b e pega ultimo digito b) assim sabemos o registrador da operação 
            add_x(registers, reg)
            next_label = int(tokenList[3])  # pega o rótulo de "vá_para"
            computed_op_desc = f"subiu 1 no registrador {reg} e desviou para {next_label}"


        case NormaCommand.SUB:
            reg = tokenList[1][-1] # pega a letra do registrador (segundo item sub_b e pega ultimo digito b) assim sabemos o registrador da operação 
            sub_x(registers, reg)
            next_label = int(tokenList[3])  # pega o rótulo de "vá_para"
            computed_op_desc = f"subiu 1 no registrador {reg} e desviou para {next_label}"

        # Como se fosse o else do java, serve para tratar valores inesperados nos cases anteriores
        case _:
            print(next_label)
            raise ValueError(f"Comando inválido: {command_token}")
        


    # Vamos mostrar a computação do rótulo atual, para isso vamos
    # a saída para o terminal    
    computed_registers = tuple(registers.values())
    computed_line = f"({current_label}, {computed_registers}) " 
    print(computed_line + computed_op_desc)


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