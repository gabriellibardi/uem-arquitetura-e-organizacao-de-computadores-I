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
    
    mem_principal, cache_dados, cache_instrucoes = aplica_configuracoes()
    armazena_instrucoes(arq_instrucoes, mem_principal)
    executa_instrucoes(mem_principal, cache_dados, cache_instrucoes)
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
    cache_dados = cache(configuracoes['palavras_por_linha'],
               configuracoes['linhas_por_conjunto'],
                 configuracoes['numero_de_conjuntos'])
    cache_instrucoes = cache(configuracoes['palavras_por_linha'],
               configuracoes['linhas_por_conjunto'],
                 configuracoes['numero_de_conjuntos'])
    arq_configuracao.close()
    return (mem_principal, cache_dados, cache_instrucoes)

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

def executa_instrucoes(mem_principal: memoria, cache_dados: cache, cache_instrucoes: cache):
    '''
    Le as instruções que estão armazenadas na memória principal e executa elas
    '''
    while registradores.regs_esp['pc'] < mem_principal.qnt_instrucoes:
        instrucao = str(mem_principal.enderecos[registradores.regs_esp['pc']])
        print('-->  ' + instrucao)
        print()
        if instrucao == 'ret': # A instrução ret não possui argumentos
            mnemonico = instrucao
        else:
            mnemonico = instrucao[0:instrucao.find(' ')].strip()
        args = ((instrucao[instrucao.find(' '):].replace(' ', '')).strip()).split(',')
        desvio = executa_instrucao(mem_principal, cache_dados, mnemonico, args) # Executa a instrução e vê se houve desvio
        if mem_principal.qnt_instrucoes + \
            mem_principal.qnt_dados + \
                mem_principal.qnt_enderecos_retorno == mem_principal.tamanho: # Memória principal está cheia
            print('Memória principal cheia')
            quit()
        if not desvio: # PC só é incrementado caso a instrução não seja de desvio
            registradores.regs_esp['pc'] += 1
        imprime_estado(mem_principal, cache_dados, cache_instrucoes)

def executa_instrucao(mem_principal: memoria, cache_dados: cache, instrucao: str, args: list) -> bool:
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
            return instrucoes.jal(args[0], mem_principal)
        case 'ret':
            return instrucoes.ret(mem_principal)
        # Memória
        case 'lw':
            instrucoes.lw(args[0], args[1], mem_principal, cache_dados)
        case 'sw':
            instrucoes.sw(args[0], args[1])
        # Movimentação
        case 'mov':
            instrucoes.mov(args[0], args[1])
        case 'movi':
            instrucoes.movi(args[0], args[1])
    return False

def busca_memoria(mem_principal: memoria, cache: cache, endereco: int) -> str:
    '''
    Busca e retorna o valor armazenado no endereço na memória
    '''
    bloco = endereco // cache.tam_linha
    conjunto = bloco % cache.num_conjuntos

    hit, valor = cache.busca(endereco, bloco, conjunto)

    if hit:
        return valor
    else:
        return mem_principal.busca(endereco)

def imprime_estado(mem_principal, cache_dados, cache_instrucoes):
    '''
    Imprime o atual estado do simulador:
    Registradores, Memória principal e Memória Cache
    '''
    registradores.imprime_registradores()
    print('\n' + '-' * 55 + ' MEMÓRIA PRINCIPAL: ' + '-' * 55 + '\n')
    print(mem_principal)
    print('------ MEMÓRIA CACHE: -------\n')
    print('Dados:')
    print(cache_dados)
    print('\nInstruções:')
    print(cache_instrucoes)
    print('\n' + '▂' * 130 + '\n')

if __name__ == '__main__':
    main()
