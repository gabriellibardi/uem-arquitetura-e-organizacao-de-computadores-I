from copy import copy

class Linha:
    def __init__(self, tag : int | None, qnt_acessos: int, palavras: list[str | int]) -> None:
        self.tag = tag
        self.qnt_acessos = qnt_acessos
        self.palavras = palavras

    def __repr__(self) -> str:
        return str(self.palavras)
    
class Cache:
    def __init__(self, palavras_por_linha : int,
                  linhas_por_conjunto: int,
                  num_conjuntos: int) -> None:
        conjunto = []
        for i in range(linhas_por_conjunto):
            conjunto.append(Linha(None, 0, [0] * palavras_por_linha))
        self.enderecos = []
        for i in range(num_conjuntos):
            self.enderecos.append(conjunto.copy())
        self.tam_linha = palavras_por_linha
        self.num_conjuntos = num_conjuntos

    def busca(self, endereco: int, num_bloco: int, num_conjunto: int) -> tuple[bool, str]:
        '''
        Busca e retorna o valor armazenado no endereço na cache
        Caso o endereço esteja na cache, retorna True
        '''
        for linha in self.enderecos[num_conjunto]:
            if linha.tag == num_bloco:
                linha.qnt_acessos += 1
                return (True, str(linha.palavras[endereco % self.tam_linha]))
        return (False, '')
    
    def insere(self, bloco: list[str | int], num_bloco: int, num_conjunto: int):
        '''
        Insere um *bloco* na cache, dependendo do conjunto no qual
        ele faria parte
        A inserção segue a política de substituição LFU, ou seja, a linha do conjunto
        substituída é aquela que possui menos acessos
        '''
        menor_qnt_acessos = self.enderecos[num_conjunto][0].qnt_acessos
        pos_linha = 0
        for i, linha in enumerate(self.enderecos[num_conjunto]):
            if linha.qnt_acessos < menor_qnt_acessos:
                menor_qnt_acessos = linha.qnt_acessos
                pos_linha = i
        self.enderecos[num_conjunto][pos_linha] = Linha(num_bloco, 1, bloco)

    def __repr__(self) -> str:
        buffer = ''
        num_linha = 0
        for num_conjunto in range(self.num_conjuntos):
            buffer += 'Conjunto ' + str(num_conjunto) + '\n'
            for linha in self.enderecos[num_conjunto]:
                buffer += '     {:<12}{}\n'.format('Linha ' + str(num_linha) + ' ->', linha)
                num_linha += 1
        return buffer
