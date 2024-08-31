import sys
import io
import instrucoes
import registradores
from memoria import memoria
from cache import cache

NOME_ARQ_CONFIGURACAO = 'config.txt'

def main():
    if len(sys.argv) != 2: # Verifica se o programa recebe o número correto de argumentos
        print('Número inválido de argumentos.')
        quit()
    
    try:
        arq_instrucoes = open(sys.argv[1], 'r')
    except:
        print('Arquivo de instruções não encontrado.')
        quit()
    
    mem_principal, mem_cache = aplica_configuracoes()
    armazena_instrucoes(arq_instrucoes, mem_principal)
    executa_instrucoes(mem_principal, mem_cache)
    arq_instrucoes.close()

def aplica_configuracoes():
    '''
    Abre o arquivo de configurações e aplica as configurações passadas
    para criar as memórias do simulador
    '''
    try:
        arq_configuracao = open(NOME_ARQ_CONFIGURACAO, 'r')
    except:
        print('Arquivo de configurações não encontrado.')
        quit()
    configuracoes = {}
    buffer = arq_configuracao.readline()
    while buffer:
        if buffer[0] == '#': # linha de comentário
            buffer = arq_configuracao.readline()
        else:
            linha = buffer.split('=')
            configuracoes[linha[0].strip()] = int(linha[1].strip())
            buffer = arq_configuracao.readline()
    if configuracoes['numero_de_palavras'] < (configuracoes['palavras_por_linha'] *
                                               configuracoes['linhas_por_conjunto'] *
                                                 configuracoes['numero_de_conjuntos']):
        print('O tamanho da memória principal é menor que o da cache.')
        quit()
    mem_principal = memoria(configuracoes['numero_de_palavras'])
    mem_cache = cache(configuracoes['palavras_por_linha'],
               configuracoes['linhas_por_conjunto'],
                 configuracoes['numero_de_conjuntos'])
    arq_configuracao.close()
    return (mem_principal, mem_cache)

def armazena_instrucoes(arq_instrucoes : io.TextIOWrapper, mem_principal : memoria):
    '''
    Passa pelo arquivo de instruções e coloca elas na memória
    '''
    linha = (arq_instrucoes.readline()).strip()
    pos = 0
    while(linha):
        mem_principal.enderecos[pos] = linha
        mem_principal.qnt_instrucoes += 1
        pos += 1
        linha = (arq_instrucoes.readline()).strip()

def executa_instrucoes(mem_principal: memoria, mem_cache: cache):
    '''
    Le as instruções que estão armazenadas na memória principal e executa elas
    '''
    while registradores.regs_esp['pc'] < mem_principal.qnt_instrucoes:
        instrucao = str(mem_principal.enderecos[registradores.regs_esp['pc']])
        print('-->  ' + instrucao)
        print()
        mnemonico = instrucao[0:instrucao.find(' ')].strip()
        args = ((instrucao[instrucao.find(' '):].replace(' ', '')).strip()).split(',')
        desvio = executa_instrucao(mnemonico, args) # Executa a instrução e vê se houve desvio
        if not desvio: # PC só é incrementado caso a instrução não seja de desvio
            registradores.regs_esp['pc'] += 1
        imprime_estado(mem_principal, mem_cache)

def executa_instrucao(instrucao: str, args: list) -> bool:
    '''
    Executa a *instrucao* com os *argumentos* passados e retorna true
    caso seja uma instrução de desvio
    '''
    match instrucao:
        # Aritméticas
        case 'add':
            instrucoes.add(args[0], args[1], args[2])
        case 'addi':
            instrucoes.addi(args[0], args[1], args[2])
        case 'sub':
            instrucoes.sub(args[0], args[1], args[2])
        case 'subi':
            instrucoes.subi(args[0], args[1], args[2])
        case 'mul':
            instrucoes.mul(args[0], args[1], args[2])
        case 'sub':
            instrucoes.div(args[0], args[1], args[2])
        # Lógicas
        case 'not':
            instrucoes.not_(args[0], args[1])
        case 'or':
            instrucoes.or_(args[0], args[1], args[2])
        case 'and':
            instrucoes.and_(args[0], args[1], args[2])
        # Desvios
        case 'blti':
            return instrucoes.blti(args[0], args[1], args[2])
        case 'bgti':
            return instrucoes.bgti(args[0], args[1], args[2])
        case 'beqi':
            return instrucoes.beqi(args[0], args[1], args[2])
        case 'blt':
            return instrucoes.blt(args[0], args[1], args[2])
        case 'bgt':
            return instrucoes.bgt(args[0], args[1], args[2])
        case 'beq':
            return instrucoes.beq(args[0], args[1], args[2])
        case 'jr':
            return instrucoes.jr(args[0])
        case 'jof':
            return instrucoes.jof(args[0])
        case 'jal':
            return instrucoes.jal(args[0])
        case 'ret':
            return instrucoes.ret()
        # Memória
        case 'lw':
            instrucoes.lw(args[0], args[1])
        case 'sw':
            instrucoes.sw(args[0], args[1])
        # Movimentação
        case 'mov':
            instrucoes.mov(args[0], args[1])
        case 'movi':
            instrucoes.movi(args[0], args[1])
    return False
    
def imprime_estado(mem_principal, mem_cache):
    '''
    Imprime o atual estado do simulador:
    Registradores, Memória principal e Memória Cache
    '''
    registradores.imprime_registradores()
    print('\n' + '-' * 55 + ' MEMÓRIA PRINCIPAL: ' + '-' * 55 + '\n')
    print(mem_principal)
    print('\n------ MEMÓRIA CACHE: -------\n')
    print(mem_cache)
    print('\n' + '▂' * 130 + '\n')

if __name__ == '__main__':
    main()
