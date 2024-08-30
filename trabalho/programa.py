import sys
import io
import instrucoes
import registradores
from memoria import memoria
from cache import cache

NOME_ARQ_CONFIGURACAO = 'config.txt'

registradores_esp = {
    'pc' : 0,
    'rsp' : 0,
    'ra' : 0,
    'of' : 0
}

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
    executa_instrucoes(mem_principal)
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

def executa_instrucoes(mem_principal: memoria):
    '''
    Le as instruções que estão armazenadas na memória principal e executa elas
    '''
    for i in range(mem_principal.qnt_instrucoes):
        instrucao = str(mem_principal.enderecos[i])
        mnemonico = instrucao[0:instrucao.find(' ')].strip()
        args = ((instrucao[instrucao.find(' '):].replace(' ', '')).strip()).split(',')
        executa_instrucao(mnemonico, args)
        registradores_esp['pc'] += 1

def executa_instrucao(instrucao: str, args: list):
    '''
    Executa a *instrucao* com os *argumentos* passados
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
            instrucoes.blti(args[0], args[1], args[2])
        case 'bgti':
            instrucoes.bgti(args[0], args[1], args[2])
        case 'beqi':
            instrucoes.beqi(args[0], args[1], args[2])
        case 'blt':
            instrucoes.blt(args[0], args[1], args[2])
        case 'bgt':
            instrucoes.bgt(args[0], args[1], args[2])
        case 'beq':
            instrucoes.beq(args[0], args[1], args[2])
        case 'jr':
            instrucoes.jr(args[0])
        case 'jof':
            instrucoes.jof(args[0])
        case 'jal':
            instrucoes.jal(args[0])
        case 'ret':
            instrucoes.ret()
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

if __name__ == '__main__':
    main()
