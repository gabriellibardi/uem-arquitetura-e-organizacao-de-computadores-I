from registradores import regs, regs_esp

# Aritméticas

def add(rd, rs, rt):
    '''
    Atribui à rd a soma de rs e rt
    rd ← rs+rt
    '''
    regs[rd] = regs[rs] + regs[rt]
    if regs[rd] < -2**32 or regs[rd] > 2 ** 32 - 1:
        regs_esp['of'] = 1
    else:
        regs_esp['of'] = 0

def addi(rd, rs, imm):
    '''
    Atribui à rd a soma entre rs e um valor imediato
    rd ← rs+imm
    '''
    regs[rd] = regs[rs] + int(imm)
    if regs[rd] < -2**32 or regs[rd] > 2 ** 32 - 1:
        regs_esp['of'] = 1
    else:
        regs_esp['of'] = 0

def sub(rd, rs, rt):
    '''
    Atribui à rd a subtração de rs e rt
    rd ← rs-rt
    '''
    regs[rd] = regs[rs] - regs[rt]
    if regs[rd] < -2**32 or regs[rd] > 2 ** 32 - 1:
        regs_esp['of'] = 1
    else:
        regs_esp['of'] = 0

def subi(rd, rs, imm):
    '''
    Atribui à rd a subtração entre rs e um valor imediato
    rd ← rs-imm
    '''
    regs[rd] = regs[rs] - int(imm)
    if regs[rd] < -2**32 or regs[rd] > 2 ** 32 - 1:
        regs_esp['of'] = 1
    else:
        regs_esp['of'] = 0

def mul(rd, rs, rt):
    '''
    Atribui à rd o produto entre rs e rt
    rd ← rs*rt
    '''
    regs[rd] = regs[rs] * regs[rt]
    if regs[rd] < -2**32 or regs[rd] > 2 ** 32 - 1:
        regs_esp['of'] = 1
    else:
        regs_esp['of'] = 0

def div(rd, rs, rt):
    '''
    Atribui à rd o quociente da divisão de rs por rt
    rd ← rs div rt
    '''
    regs[rd] = regs[rs] / regs[rt]
    regs_esp['of'] = 0

# Lógicas

def not_(rd, rs):
    '''
    Atribui á rd a negação bit a bit de rs
    rd ← ~rs
    '''
    regs[rd] = ~regs[rs]

def or_(rd, rs, rt):
    '''
    Atribui à rd a disjunção (ou lógico) bit a bit entre rs e rt
    rd ← rs | rd
    '''
    regs[rd] = regs[rs] | regs[rt]

def and_(rd, rs, rt):
    '''
    Atribui à rd a conjunção (e lógico) bit a bit entre rs e rt
    rd ← rs & rd
    '''
    regs[rd] = regs[rs] & regs[rt]

# Desvios

def blti(rs, rt, imm) -> bool:
    '''
    Salta caso rs seja maior que rt
    Se rs > rt então pc ← imm
    Retorna True caso houve desvio
    '''
    if regs[rs] > regs[rt]:
        regs_esp['pc'] = int(imm)
        return True
    return False

def bgti(rs, rt, imm) -> bool:
    '''
    Salta caso rs seja menor que rt
    Se rs < rt então pc ← imm
    Retorna True caso houve desvio
    '''
    if regs[rs] < regs[rt]:
        regs_esp['pc'] = int(imm)
        return True
    return False

def beqi(rs, rt, imm) -> bool:
    '''
    Salta caso rs e rt sejam iguais
    Se rs = rt então pc ← imm
    Retorna True caso houve desvio
    '''
    if regs[rs] == regs[rt]:
        regs_esp['pc'] = int(imm)
        return True
    return False

def blt(rs, rt, rd) -> bool:
    '''
    Salta para rd caso rs seja maior que rt
    Se rs > rt então pc ← rd
    Retorna True caso houve desvio
    '''
    if regs[rs] > regs[rt]:
        regs_esp['pc'] = regs[rd]
        return True
    return False

def bgt(rs, rt, rd) -> bool:
    '''
    Salta para rd caso rs seja menor que rt
    Se rs < rt então pc ← rd
    Retorna True caso houve desvio
    '''
    if regs[rs] < regs[rt]:
        regs_esp['pc'] = regs[rd]
        return True
    return False
    
def beq(rs, rt, rd) -> bool:
    '''
    Salta para rd caso rs e rt sejam iguais
    Se rs = rt então pc ← rd
    Retorna True caso houve desvio
    '''
    if regs[rs] == regs[rt]:
        regs_esp['pc'] = regs[rd]
        return True
    return False

def jr(rd) -> bool:
    '''
    Salto incondicional para rd
    pc ← rd
    Retorna True, já que houve desvio
    '''
    regs_esp['pc'] = regs[rd]
    return True

def jof(rd) -> bool:
    '''
    Salto em caso de overflow
    Se of == 1 então pc ← rd
    Retorna True caso houve desvio
    '''
    if regs_esp['of']:
        regs_esp['pc'] = regs[rd]
        return True
    return False

def jal(imm, mem_principal) -> bool:
    '''
    Salto usado para chamada de função com endereço inicial em imm
    ra ← pc + 8 (próxima instrução) e pc ← imm
    Retorna True, já que houve desvio
    '''
    regs_esp['rsp'] += 1
    mem_principal.enderecos[-regs_esp['rsp']] = regs_esp['pc'] + 1
    mem_principal.qnt_enderecos_retorno += 1
    regs_esp['ra'] = regs_esp['pc'] + 1
    regs_esp['pc'] = int(imm)
    return True

def ret(mem_principal) -> bool:
    '''
    Salto usado para voltar de uma chamada de função
    pc ← ra
    Retorna True, já que houve desvio
    '''
    if regs_esp['rsp'] != 0:
        regs_esp['pc'] = regs_esp['ra']
        regs_esp['rsp'] -= 1
        if regs_esp['rsp'] == 0: # Pilha de retorno esvaziada
            regs_esp['ra'] = 0
        else:
            regs_esp['ra'] = mem_principal.enderecos[-regs_esp['rsp']]
        mem_principal.qnt_enderecos_retorno -= 1
        return True
    else:
        print('Pilha de retorno vazia.')
        quit()

# Memória

def lw(rd, imm):
    '''
    Carrega da memória para o registrador rd
    rd ← M[imm+rs]
    '''

def sw(rs, imm):
    '''
    Armazena o valor de rs na memória
    M[imm+rt] ← rs
    '''

# Movimentação

def mov(rd, rs):
    '''
    Movimentação de registrador para registrador
    rd ← rs
    '''
    regs[rd] = regs[rs]

def movi(rd, imm):
    '''
    Movimentação de imediato para registrador
    rd ← imm
    '''
    regs[rd] = int(imm)
