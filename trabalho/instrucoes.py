from registradores import regs

# Aritméticas

def add(rd, rs, rt):
    '''
    Atribui à rd a soma de rs e rt
    rd ← rs+rt
    '''
    regs[rd] = regs[rs] + regs[rt]

def addi(rd, rs, imm):
    '''
    Atribui à rd a soma entre rs e um valor imediato
    rd ← rs+imm
    '''
    regs[rd] = regs[rs] + int(imm)

def sub(rd, rs, rt):
    '''
    Atribui à rd a subtração de rs e rt
    rd ← rs-rt
    '''
    regs[rd] = regs[rs] - regs[rt]

def subi(rd, rs, imm):
    '''
    Atribui à rd a subtração entre rs e um valor imediato
    rd ← rs-imm
    '''
    regs[rd] = regs[rs] - int(imm)

def mul(rd, rs, rt):
    '''
    Atribui à rd o produto entre rs e rt
    rd ← rs*rt
    '''
    regs[rd] = regs[rs] * regs[rt]

def div(rd, rs, rt):
    '''
    Atribui à rd o quociente da divisão de rs por rt
    rd ← rs div rt
    '''
    regs[rd] = regs[rs] / regs[rt]

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

def blti(rs, rt, imm):
    '''
    Salta caso rs seja maior que rt
    Se rs > rt então pc ← imm
    '''
    if regs[rs] > regs[rt]:
        regs['pc'] = int(imm)

def bgti(rs, rt, imm):
    '''
    Salta caso rs seja menor que rt
    Se rs < rt então pc ← imm
    '''
    if regs[rs] < regs[rt]:
        regs['pc'] = int(imm)

def beqi(rs, rt, imm):
    '''
    Salta caso rs e rt sejam iguais
    Se rs = rt então pc ← imm
    '''
    if regs[rs] == regs[rt]:
        regs['pc'] = int(imm)

def blt(rs, rt, rd):
    '''
    Salta para rd caso rs seja maior que rt
    Se rs > rt então pc ← rd
    '''
    if regs[rs] > regs[rt]:
        regs['pc'] = regs[rd]

def bgt(rs, rt, rd):
    '''
    Salta para rd caso rs seja menor que rt
    Se rs < rt então pc ← rd
    '''
    if regs[rs] < regs[rt]:
        regs['pc'] = regs[rd]
    
def beq(rs, rt, rd):
    '''
    Salta para rd caso rs e rt sejam iguais
    Se rs = rt então pc ← rd
    '''
    if regs[rs] == regs[rt]:
        regs['pc'] = regs[rd]

def jr(rd):
    '''
    Salto incondicional para rd
    pc ← rd
    '''
    regs['pc'] = regs[rd]

def jof(rd):
    '''
    Salto em caso de overflow
    Se of == 1 então pc ← rd
    '''
    if regs['of'] == 1:
        regs['pc'] == regs[rd]

def jal(imm):
    '''
    Salto usado para chamada de função com endereço inicial em imm
    ra ← pc + 8 (próxima instrução) e pc ← imm
    '''

def ret():
    '''
    Salto usado para voltar de uma chamada de função
    pc ← ra
    '''
    regs['pc'] = regs['ra']

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
