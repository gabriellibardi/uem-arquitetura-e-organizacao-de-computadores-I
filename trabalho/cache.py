class cache:
    def __init__(self, palavras_por_linha : int,
                  linhas_por_conjunto: int,
                  num_conjuntos: int) -> None:
        linha = [0] * palavras_por_linha
        conjunto = [linha] * linhas_por_conjunto
        self.enderecos = [conjunto] * num_conjuntos
        self.tam_linha = palavras_por_linha
        self.num_conjuntos = num_conjuntos

    def busca(self, endereco: int, bloco: int, conjunto: int) -> tuple[bool, str]:
        '''
        Busca e retorna o valor armazenado no endereço na cache
        Caso o endereço esteja na cache, retorna True
        '''
        # for linha in self.dados[conjunto]:
        #     if linha == bloco:
        #         return (True, self.dados[conjunto][linha][endereco])
        return (False, '')
    
    def __repr__(self) -> str:
        conjuntos = ''
        for c in self.enderecos:
            conjuntos += '\n' + str(c)
        return conjuntos
