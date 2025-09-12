
MACRO_X = "x"

def start_macro_aux_registers():
    return (MACRO_X, "i", "j")

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
    

def copy(tokens, expanded, l1, next_free_label):
    
    macro_operation = tokens[1]        
    _, origin, destination = macro_operation.split('_')
    final_jump = int(tokens[3])


    x = MACRO_X 
    
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



def multiply(tokens, expanded, l1, next_free_label):
    final_jump = int(tokens[3])

    # Registradores usados
    a = "a"
    b = "b"
    c = "c"
    i = "i"
    j = "j"

    # Preparar rótulos auxiliares
    l2 = next_free_label
    l3 = next_free_label + 1
    l4 = next_free_label + 2
    l5 = next_free_label + 3
    l6 = next_free_label + 4
    l7 = next_free_label + 5
    l8 = next_free_label + 6
    next_free_label += 7

    # 0: clear c
    expanded, next_free_label = clear(['faça', f'clear_{c}', 'vá_para', l2], expanded, l1, next_free_label)

    # 1: copy a -> i
    expanded, next_free_label = copy(['faça', f'copy_{a}_{i}', 'vá_para', l3], expanded, l2, next_free_label)

    # # 2: copy b -> j
    # expanded, next_free_label = copy(['faça', f'copy_{b}_{j}', 'vá_para', l4], expanded, l3, next_free_label)

    # 3: se zero i então vá_para l9 senão vá_para l5
    expanded.append(f"{l3}: se zero_{i} então vá_para {final_jump} senão vá_para {l4}")

    # 4: sub i
    expanded.append(f"{l4}: faça sub_{i} vá_para {l5}")

    # 5: copy b -> j
    expanded, next_free_label = copy(['faça', f'copy_{b}_{j}', 'vá_para', l6], expanded, l5, next_free_label)

    # 5.1: se zero j então vá_para l4 senão vá_para l8
    expanded.append(f"{l6}: se zero_{j} então vá_para {l3} senão vá_para {l7}")

    # 6: sub j
    expanded.append(f"{l7}: faça sub_{j} vá_para {l8}")

    # 7: add c
    expanded.append(f"{l8}: faça add_{c} vá_para {l6}")

    return expanded, next_free_label
