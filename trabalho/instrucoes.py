from registradores import regs, regs_esp
from programa import busca_memoria
from memoria import Memoria
from cache import Cache

# Aritméticas

def add(rd: str, rs: str, rt: str):
    '''
    Atribui à rd a soma de rs e rt
    rd ← rs+rt
    '''
    regs[rd] = regs[rs] + regs[rt]
    if regs[rd] < -2**32 or regs[rd] > 2 ** 32 - 1:
        regs_esp['of'] = 1
    else:
        regs_esp['of'] = 0

def addi(rd: str, rs: str, imm: str):
    '''
    Atribui à rd a soma entre rs e um valor imediato
    rd ← rs+imm
    '''
    regs[rd] = regs[rs] + int(imm)
    if regs[rd] < -2**32 or regs[rd] > 2 ** 32 - 1:
        regs_esp['of'] = 1
    else:
        regs_esp['of'] = 0

def sub(rd: str, rs: str, rt: str):
    '''
    Atribui à rd a subtração de rs e rt
    rd ← rs-rt
    '''
    regs[rd] = regs[rs] - regs[rt]
    if regs[rd] < -2**32 or regs[rd] > 2 ** 32 - 1:
        regs_esp['of'] = 1
    else:
        regs_esp['of'] = 0

def subi(rd: str, rs: str, imm: str):
    '''
    Atribui à rd a subtração entre rs e um valor imediato
    rd ← rs-imm
    '''
    regs[rd] = regs[rs] - int(imm)
    if regs[rd] < -2**32 or regs[rd] > 2 ** 32 - 1:
        regs_esp['of'] = 1
    else:
        regs_esp['of'] = 0

def mul(rd: str, rs: str, rt: str):
    '''
    Atribui à rd o produto entre rs e rt
    rd ← rs*rt
    '''
    regs[rd] = regs[rs] * regs[rt]
    if regs[rd] < -2**32 or regs[rd] > 2 ** 32 - 1:
        regs_esp['of'] = 1
    else:
        regs_esp['of'] = 0

def div(rd: str, rs: str, rt: str):
    '''
    Atribui à rd o quociente da divisão de rs por rt
    rd ← rs div rt
    '''
    regs[rd] = regs[rs] // regs[rt]
    regs_esp['of'] = 0

# Lógicas

def not_(rd: str, rs: str):
    '''
    Atribui á rd a negação bit a bit de rs
    rd ← ~rs
    '''
    regs[rd] = ~regs[rs]

def or_(rd: str, rs: str, rt: str):
    '''
    Atribui à rd a disjunção (ou lógico) bit a bit entre rs e rt
    rd ← rs | rd
    '''
    regs[rd] = regs[rs] | regs[rt]

def and_(rd: str, rs: str, rt: str):
    '''
    Atribui à rd a conjunção (e lógico) bit a bit entre rs e rt
    rd ← rs & rd
    '''
    regs[rd] = regs[rs] & regs[rt]

# Desvios

def blti(rs: str, rt: str, imm: str) -> bool:
    '''
    Salta caso rs seja maior que rt
    Se rs > rt então pc ← imm
    Retorna True caso houve desvio
    '''
    if regs[rs] > regs[rt]:
        regs_esp['pc'] = int(imm)
        return True
    return False

def bgti(rs: str, rt: str, imm: str) -> bool:
    '''
    Salta caso rs seja menor que rt
    Se rs < rt então pc ← imm
    Retorna True caso houve desvio
    '''
    if regs[rs] < regs[rt]:
        regs_esp['pc'] = int(imm)
        return True
    return False

def beqi(rs: str, rt: str, imm: str) -> bool:
    '''
    Salta caso rs e rt sejam iguais
    Se rs = rt então pc ← imm
    Retorna True caso houve desvio
    '''
    if regs[rs] == regs[rt]:
        regs_esp['pc'] = int(imm)
        return True
    return False

def blt(rs: str, rt: str, rd: str) -> bool:
    '''
    Salta para rd caso rs seja maior que rt
    Se rs > rt então pc ← rd
    Retorna True caso houve desvio
    '''
    if regs[rs] > regs[rt]:
        regs_esp['pc'] = regs[rd]
        return True
    return False

def bgt(rs: str, rt: str, rd: str) -> bool:
    '''
    Salta para rd caso rs seja menor que rt
    Se rs < rt então pc ← rd
    Retorna True caso houve desvio
    '''
    if regs[rs] < regs[rt]:
        regs_esp['pc'] = regs[rd]
        return True
    return False
    
def beq(rs: str, rt: str, rd: str) -> bool:
    '''
    Salta para rd caso rs e rt sejam iguais
    Se rs = rt então pc ← rd
    Retorna True caso houve desvio
    '''
    if regs[rs] == regs[rt]:
        regs_esp['pc'] = regs[rd]
        return True
    return False

def jr(rd: str) -> bool:
    '''
    Salto incondicional para rd
    pc ← rd
    Retorna True, já que houve desvio
    '''
    regs_esp['pc'] = regs[rd]
    return True

def jof(rd: str) -> bool:
    '''
    Salto em caso de overflow
    Se of == 1 então pc ← rd
    Retorna True caso houve desvio
    '''
    if regs_esp['of']:
        regs_esp['pc'] = regs[rd]
        return True
    return False

def jal(imm: str, mem_principal: Memoria) -> bool:
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

def lw(rd: str, arg: str, mem_principal: Memoria, mem_cache: Cache):
    '''
    Carrega da memória para o registrador rd
    rd ← M[imm+rs]
    '''
    imm = arg[:arg.find('(')]
    rs = arg[arg.find('(') + 1 : -1]
    endereco = int(imm) + regs[rs]

    # Endereço fora do espaço de memória para dados
    if endereco < mem_principal.qnt_instrucoes or \
        endereco > mem_principal.tamanho - 1 - mem_principal.qnt_enderecos_retorno:
        print('Endereço indisponível.')
        quit()

    regs[rd] = int(busca_memoria(mem_principal, mem_cache, endereco))

def sw(rs: str, arg: str, mem_principal: Memoria, cache: Cache):
    '''
    Armazena o valor de rs na memória
    M[imm+rt] ← rs
    '''
    imm = arg[:arg.find('(')]
    rt = arg[arg.find('(') + 1 : -1]
    endereco = int(imm) + regs[rt]

    # Endereço fora do espaço de memória para dados
    if endereco < mem_principal.qnt_instrucoes or \
        endereco > mem_principal.tamanho - 1 - mem_principal.qnt_enderecos_retorno:
        print('Endereço indisponível.')
        quit()
        
    # Verifica se o endereço está na cache, se sim, modifica e escreve na memória
    # seguindo a política Write Through
    num_bloco = endereco // cache.tam_linha
    num_conjunto = num_bloco % cache.num_conjuntos
    for linha in cache.enderecos[num_conjunto]:
        if linha.tag == num_bloco:
            linha.palavras[endereco % cache.tam_linha] = regs[rs]
            break

    mem_principal.enderecos[endereco] = regs[rs]
    # Insere na lista de endereços ocupados
    mem_principal.enderecos_dados_ocupados.append(endereco)
    mem_principal.enderecos_dados_ocupados.sort()

# Movimentação

def mov(rd: str, rs: str):
    '''
    Movimentação de registrador para registrador
    rd ← rs
    '''
    regs[rd] = regs[rs]

def movi(rd: str, imm: str):
    '''
    Movimentação de imediato para registrador
    rd ← imm
    '''
    regs[rd] = int(imm)
