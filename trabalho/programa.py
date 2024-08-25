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
    

    aplica_configuracoes()
    busca_instrucoes(arq_instrucoes)
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
        
    global mem_principal
    global mem_cache
    mem_principal = memoria(configuracoes['numero_de_palavras'])
    mem_cache = cache(configuracoes['palavras_por_linha'],
               configuracoes['linhas_por_conjunto'],
                 configuracoes['numero_de_conjuntos'])
    arq_configuracao.close()

def busca_instrucoes(arq_instrucoes : io.TextIOWrapper):
    '''
    Passa pelo arquivo de instruções e realiza a instrução especificada em cada linha
    '''
    linha = arq_instrucoes.readline()
    while(linha):
        print('------------- PC = ' + str(registradores.regs['pc']) + ' --------------')
        instrucao = linha[0:linha.find(' ')].strip()
        args = ((linha[linha.find(' '):].replace(' ', '')).strip()).split(',')
        executa_instrucoes(instrucao, args)
        registradores.imprime_registradores()
        registradores.regs['pc'] += 1
        linha = arq_instrucoes.readline()

def executa_instrucoes(instrucao: str, args: list):
    '''
    Executa a *instrucao* com os *argumentos* passados
    '''
    # Aritméticas
    if instrucao == 'add':
        instrucoes.add(args[0], args[1], args[2])
    if instrucao == 'addi':
        instrucoes.addi(args[0], args[1], args[2])
    if instrucao == 'sub':
        instrucoes.sub(args[0], args[1], args[2])
    if instrucao == 'subi':
        instrucoes.subi(args[0], args[1], args[2])
    if instrucao == 'mul':
        instrucoes.mul(args[0], args[1], args[2])
    if instrucao == 'sub':
        instrucoes.div(args[0], args[1], args[2])
    # Lógicas
    if instrucao == 'not':
        instrucoes.not_(args[0], args[1])
    if instrucao == 'or':
        instrucoes.or_(args[0], args[1], args[2])
    if instrucao == 'and':
        instrucoes.and_(args[0], args[1], args[2])
    # Desvios
    if instrucao == 'blti':
        instrucoes.blti(args[0], args[1], args[2])
    if instrucao == 'bgti':
        instrucoes.bgti(args[0], args[1], args[2])
    if instrucao == 'beqi':
        instrucoes.beqi(args[0], args[1], args[2])
    if instrucao == 'blt':
        instrucoes.blt(args[0], args[1], args[2])
    if instrucao == 'bgt':
        instrucoes.bgt(args[0], args[1], args[2])
    if instrucao == 'beq':
        instrucoes.beq(args[0], args[1], args[2])
    if instrucao == 'jr':
        instrucoes.jr(args[0])
    if instrucao == 'jof':
        instrucoes.jof(args[0])
    if instrucao == 'jal':
        instrucoes.jal(args[0])
    if instrucao == 'ret':
        instrucoes.ret()
    # Memória
    if instrucao == 'lw':
        instrucoes.lw(args[0], args[1])
    if instrucao == 'sw':
        instrucoes.sw(args[0], args[1])
    # Movimentação
    if instrucao == 'mov':
        instrucoes.mov(args[0], args[1])
    if instrucao == 'movi':
        instrucoes.movi(args[0], args[1])

if __name__ == '__main__':
    main()
