class Memoria:

    enderecos: list[int | str]
    
    def __init__(self, num_palavras : int, tam_bloco: int) -> None:
        self.tamanho = num_palavras
        self.tam_bloco = tam_bloco
        self.enderecos = [0] * num_palavras
        self.enderecos_dados_ocupados : list[int] = list()
        self.qnt_instrucoes = 0
        self.qnt_enderecos_retorno = 0
    
    def busca_endereco(self, endereco: int) -> str | int:
        '''
        Busca e retorna o valor armazenado no endereço
        '''
        return self.enderecos[endereco]
    
    def busca_bloco(self, endereco: int) -> list[int | str]:
        '''
        Busca e retorna o bloco que contenha o *endereco*
        '''
        num_bloco = endereco // self.tam_bloco
        return self.enderecos[num_bloco * self.tam_bloco : (num_bloco + 1) * self.tam_bloco]

    def __repr__(self) -> str:
        buffer = ''
        for i in range(self.qnt_instrucoes):
            buffer += '{:>3} {:<}\n'.format(str(i), str(self.enderecos[i]))
        for endereco in self.enderecos_dados_ocupados:
            buffer += '{:>3} {:<}\n'.format(str(endereco), str(self.enderecos[endereco]))
        for i in range(1, self.qnt_enderecos_retorno + 1):
            buffer += '{:>3} {:<}\n'.format(str(self.tamanho + 1 - i), str(self.enderecos[-i]))
        return buffer
