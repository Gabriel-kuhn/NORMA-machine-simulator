# São os registradores auxiliares que usamos nas macros
MACRO_REG_X = "x" #(COPY_)

MACRO_REG_Y = "y" #(MULT_)
MACRO_REG_Z = "z" #(MULT_)

MACRO_REG_W = "w" #(MIN_)
MACRO_REG_V = "v" #(MIN_)


# DICA EXTREMAMENTE IMPORTANTE:
# quando for fazer uma macro, não pode usar os reg auxiliares que já são usados em outro
# PORQUE: se você usar uma macro dentro de outra macro, os regs aux vão bugar ;-;

def start_macro_aux_registers():
    return (MACRO_REG_X, MACRO_REG_Y, MACRO_REG_Z, MACRO_REG_W, MACRO_REG_V)

def expand_macros(program_lines):
    expanded = []
    next_free_label = 1000  # rótulos "reservados" para macros

    for line in program_lines:
        label, instruction = line.split(":", 1) # quebra a string nas ocorrências do : (1 é pra pegar só a primeira ocorrência)
        label = int(label.strip())
        instruction = instruction.strip()
        tokens = instruction.split()

    
        if "copy_" in instruction:
            expanded, next_free_label = copy(tokens, expanded, label, next_free_label)


        elif "clear_" in instruction:
            expanded, next_free_label = clear(tokens, expanded, label, next_free_label)


        elif "mult_" in instruction:
            expanded, next_free_label = multiply(tokens, expanded, label, next_free_label)

        elif "min_" in instruction:
            expanded, next_free_label = min(tokens, expanded, label, next_free_label)

        elif "max_" in instruction:
            expanded, next_free_label = max(tokens, expanded, label, next_free_label)

        else:
            expanded.append(f"{label}: {instruction}")

    return expanded



def clear(tokens, expanded, l1, next_free_label):
    reg = tokens[1][-1]       # ex: zero_a
    final_jump = int(tokens[3])  # rótulo para pular após zerar
    
    l2 = next_free_label
    next_free_label += 1 # quantidade de labels utilizadas na macro
    
    expanded.append(f"{l1}: se zero_{reg} então vá_para {final_jump} senão vá_para {l2}")
    expanded.append(f"{l2}: faça sub_{reg} vá_para {l1}")

    return expanded, next_free_label
    
# Precisa dos auxiliares: X
def copy(tokens, expanded, l1, next_free_label):
    
    macro_operation = tokens[1]        
    _, origin, destination = macro_operation.split('_')
    final_jump = int(tokens[3])


    x = MACRO_REG_X 
    
    expanded, next_free_label = clear(
        ['faça',"clear_x", "vá_para", next_free_label+1], expanded, l1, next_free_label
    )

    l2 = next_free_label
    l3 = next_free_label + 1
    l4 = next_free_label + 2
    l5 = next_free_label + 3
    l6 = next_free_label + 4
    l7 = next_free_label + 5
    l8 = next_free_label + 6
    next_free_label += 7

    # 1ª parte: esvazia src, acumulando em tmp1 e tmp2
    expanded.append(f"{l2}: se zero_{origin} então vá_para {l5} senão vá_para {l3}")
    expanded.append(f"{l3}: faça sub_{origin} vá_para {l4}")
    expanded.append(f"{l4}: faça add_{x} vá_para {l2}")

    # 2ª parte: restaurar src a partir de tmp1 e enviar cópia para dst
    expanded.append(f"{l5}: se zero_{x} então vá_para {final_jump} senão vá_para {l6}")
    expanded.append(f"{l6}: faça sub_{x} vá_para {l7}")
    expanded.append(f"{l7}: faça add_{origin} vá_para {l8}")
    expanded.append(f"{l8}: faça add_{destination} vá_para {l5}")

    return expanded, next_free_label


# Precisa dos auxiliares: Y, Z
def multiply(tokens, expanded, l1, next_free_label):
    final_jump = int(tokens[3])

    aux = tokens[1]
    aux = aux.split("_")
    # Registradores usados
    # VOu chama-los de a, b, c pq fica mais fácil de compreender o código
    a = aux[1] # vai pegar o 1º registrador passado
    b = aux[2] # vai pegar o 2º registrador passado
    c = aux[3]  # vai pegar o 3º passado, que vai ser o destino do resultado
    i = MACRO_REG_Y
    j = MACRO_REG_Z # chamei de j e i pq normalmente quando fazemos loops usamos essas duas variáveis, mas vão usar outros registradores auxiliares

    # Preparar rótulos auxiliares
    l2 = next_free_label
    l3 = next_free_label + 1
    l4 = next_free_label + 2
    l5 = next_free_label + 3
    l6 = next_free_label + 4
    l7 = next_free_label + 5
    l8 = next_free_label + 6
    next_free_label += 7


    # 1: clear_c vá_para 2
    # 2: copy_a_i vá_para 3
    # 3: se zero_i então vá_para 9 senão vá_para 4
    # 4: sub_i vá_para 5
    # 5: copy_b_j vá_para 6
    # 6: se zero_j então vá_para 3 senão vá_para 7
    # 7: sub_j vá_para 8
    # 8: add_c vá_para 6

    # Dica top: lembrar que não precisa zerar os registradores auxiliares, pq o copy já faz isso

    expanded, next_free_label = clear(['faça', f'clear_{c}', 'vá_para', l2], expanded, l1, next_free_label)
    expanded, next_free_label = copy(['faça', f'copy_{a}_{i}', 'vá_para', l3], expanded, l2, next_free_label)
    expanded.append(f"{l3}: se zero_{i} então vá_para {final_jump} senão vá_para {l4}")
    expanded.append(f"{l4}: faça sub_{i} vá_para {l5}")
    expanded, next_free_label = copy(['faça', f'copy_{b}_{j}', 'vá_para', l6], expanded, l5, next_free_label)
    expanded.append(f"{l6}: se zero_{j} então vá_para {l3} senão vá_para {l7}")
    expanded.append(f"{l7}: faça sub_{j} vá_para {l8}")
    expanded.append(f"{l8}: faça add_{c} vá_para {l6}")

    return expanded, next_free_label


# Precisa dos auxiliares: Z, W
def min(tokens, expanded, l1, next_free_label):
    final_jump = int(tokens[3])

    aux = tokens[1]
    aux = aux.split("_")
    a = aux[1]  # primeiro valor
    b = aux[2]  # segundo valor
    c = aux[3]  # destino
    d = MACRO_REG_W  # auxiliar 1 (cópia de a)
    e = MACRO_REG_V  # auxiliar 2 (cópia de b)

    # Preparar rótulos auxiliares
    l2 = next_free_label
    l3 = next_free_label + 1
    l4 = next_free_label + 2
    l5 = next_free_label + 3
    l6 = next_free_label + 4
    l7 = next_free_label + 5
    l8 = next_free_label + 6
    next_free_label += 7

    # 1: faça copy_a_d vá_para 2
    # 2: faça copy_b_e vá_para 3
    # 3: se zero_d então vá_para 7 senão vá_para 4
    # 4: se zero_e então vá_para 8 senão vá_para 5
    # 5: faça sub_d vá_para 6
    # 6: faça sub_e vá_para 3
    # 7: faça copy_a_c vá_para 50
    # 8: faça copy_b_c vá_para 50

    expanded, next_free_label = copy(['faça', f'copy_{a}_{d}', 'vá_para', l2], expanded, l1, next_free_label)
    expanded, next_free_label = copy(['faça', f'copy_{b}_{e}', 'vá_para', l3], expanded, l2, next_free_label)
    expanded.append(f"{l3}: se zero_{d} então vá_para {l7} senão vá_para {l4}")
    expanded.append(f"{l4}: se zero_{e} então vá_para {l8} senão vá_para {l5}")
    expanded.append(f"{l5}: faça sub_{d} vá_para {l6}")
    expanded.append(f"{l6}: faça sub_{e} vá_para {l3}")
    expanded, next_free_label = copy(['faça', f'copy_{a}_{c}', 'vá_para', final_jump], expanded, l7, next_free_label) # Aqui o menor é a
    expanded, next_free_label = copy(['faça', f'copy_{b}_{c}', 'vá_para', final_jump], expanded, l8, next_free_label) # Aqui o menor é b

    return expanded, next_free_label

# Precisa dos auxiliares: Z, W
def max(tokens, expanded, l1, next_free_label):

# DICA: é exatamente e mesma coisa do anterior (min_), mas quando a é menor, c vai receber o valor de b
# Porque eu quero saber quem é maior dessa vez

    final_jump = int(tokens[3])

    aux = tokens[1]
    aux = aux.split("_")
    a = aux[1]  # primeiro valor
    b = aux[2]  # segundo valor
    c = aux[3]  # destino
    d = MACRO_REG_W  # auxiliar 1 (cópia de a)
    e = MACRO_REG_V  # auxiliar 2 (cópia de b)

    # Preparar rótulos auxiliares
    l2 = next_free_label
    l3 = next_free_label + 1
    l4 = next_free_label + 2
    l5 = next_free_label + 3
    l6 = next_free_label + 4
    l7 = next_free_label + 5
    l8 = next_free_label + 6
    next_free_label += 7

    # 1: faça copy_a_d vá_para 2
    # 2: faça copy_b_e vá_para 3
    # 3: se zero_d então vá_para 7 senão vá_para 4
    # 4: se zero_e então vá_para 8 senão vá_para 5
    # 5: faça sub_d vá_para 6
    # 6: faça sub_e vá_para 3
    # 7: faça copy_a_c vá_para 50
    # 8: faça copy_b_c vá_para 50

    expanded, next_free_label = copy(['faça', f'copy_{a}_{d}', 'vá_para', l2], expanded, l1, next_free_label)
    expanded, next_free_label = copy(['faça', f'copy_{b}_{e}', 'vá_para', l3], expanded, l2, next_free_label)
    expanded.append(f"{l3}: se zero_{d} então vá_para {l7} senão vá_para {l4}")
    expanded.append(f"{l4}: se zero_{e} então vá_para {l8} senão vá_para {l5}")
    expanded.append(f"{l5}: faça sub_{d} vá_para {l6}")
    expanded.append(f"{l6}: faça sub_{e} vá_para {l3}")
    expanded, next_free_label = copy(['faça', f'copy_{a}_{c}', 'vá_para', final_jump], expanded, l8, next_free_label) # Aqui o maior é b
    expanded, next_free_label = copy(['faça', f'copy_{b}_{c}', 'vá_para', final_jump], expanded, l7, next_free_label) # Aqui o maior é a

    return expanded, next_free_label