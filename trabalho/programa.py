import sys
from registradores import regs
from memoria import memoria
from cache import cache

NOME_ARQ_CONFIGURACAO = 'config.txt'

def main():
    if len(sys.argv) != 2: # Verifica se o programa recebe o número correto de argumentos
        print('Número inválido de argumentos.')
        quit()
    
    aplica_configuracoes()


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

    memoria = memoria(configuracoes['numero_de_palavras'])
    cache = cache(configuracoes['palavras_por_linha'],
               configuracoes['linhas_por_conjunto'],
                 configuracoes['numero_de_conjuntos'])

if __name__ == '__main__':
    main()
