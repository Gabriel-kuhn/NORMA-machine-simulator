from norma_commands import NormaCommand
from macro_compiler import expand_macros


def run(registers: dict, typed_lines: list):
    
    # Vamos compilar as operações macros, vamos meio que traduzir elas, pq a norma não entende nada além de add sub e zero
    # então precisamos traduzir para uma forma que ela consiga "ler"
    typed_lines = expand_macros(typed_lines)

    # Vamos converter as linhas digitas para um formato que nossa máquina possa interpretar corretamente.
    program = convert_typed_lines_to_command_lines(typed_lines)


    # Começa pelo menor rótulo, normalmente é 0 ou 1 mas o usuário pode acabar querendo começar pelo 7...
    program_counter = min(program.keys())

    # Mostra o estado inicial da máquina
    formated_regs = tuple(registers.values())
    print(f"({program_counter}, {formated_regs})")

    # Aqui está toda jogada, vamos iniciar somente uma instrução. Faremos o resto recursivo
    # Porque cada instrução nela mesma contém para qual rótulo deve seguir, então ela mesma vai decidir a próxima etapa
    # o try é para a codinção de parada. Na NORMA, quando queremos terminar o programa, nós dizemos que vamos 
    # para o rótulo inexistente, ou nao definido, assim, quando acontecer um OutOfBoundException sabemos que 
    # a instrução está levando para um condição de parada.
    try:
        interpret(registers, program, program_counter)

    
    except ValueError as e:
        # Se der erro de usar um registrador sem ter declarado ele cai aqui
        print(f"\nERRO: {e}")

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
        if ":" in line: # Isso é uma segurança para pegar só as linhas que contém o formato (1: faça ...) 

            # Colocamos em um dicionário o rótulo e a instrução daquele rótulo
            # Para isso vamos separa-los pelo "1:" que cada linha (rótulo) tem

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
            validateRegister(registers, reg)   # antes de usar o registrador, precisamos validar se ele foi declarado corretamente
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
            validateRegister(registers, reg)   # antes de usar o registrador, precisamos validar se ele foi declarado corretamente
            add_x(registers, reg)
            next_label = int(tokenList[3])  # pega o rótulo de "vá_para"
            computed_op_desc = f"subiu 1 no registrador {reg} e desviou para {next_label}"


        case NormaCommand.SUB:
            reg = tokenList[1][-1]  # pega a letra do registrador (segundo item sub_b e pega ultimo digito b) assim sabemos o registrador da operação 
            validateRegister(registers, reg)   # antes de usar o registrador, precisamos validar se ele foi declarado corretamente
            sub_x(registers, reg)
            next_label = int(tokenList[3])  # pega o rótulo de "vá_para"
            computed_op_desc = f"diminuiu 1 no registrador {reg} e desviou para {next_label}"

        # Como se fosse o else do java, serve para tratar valores inesperados nos cases anteriores
        case _:
            #print(next_label)
            raise ValueError(f"Comando inválido: {command_token}")
        


    # Vamos mostrar a computação do rótulo atual, para isso vamos
    # a saída para o terminal    
    computed_registers = tuple(registers.values())
    computed_line = f"({current_label}, {computed_registers}) " 
    print(computed_line + computed_op_desc)


    # Chamada recursiva para a próxima instrução referente ao valor de next_label
    interpret(registers, program, next_label)

    
# .:| === Função para validar se o registrador usado foi declarado |:. === 
def validateRegister(registers: dict, reg: str):
    if reg not in registers:
        raise ValueError(
            f"O programa tentou usar o registrador '{reg}' porém ele não foi declarado no arquivo do programa!"
        )


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


