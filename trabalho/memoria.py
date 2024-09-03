class Memoria:

    enderecos: list[int | str]
    
    def __init__(self, num_palavras : int) -> None:
        self.tamanho = num_palavras
        self.enderecos = [0] * num_palavras
        self.qnt_instrucoes = 0
        self.qnt_dados = 0
        self.qnt_enderecos_retorno = 0
    
    def busca_endereco(self, endereco: int) -> str:
        '''
        Busca e retorna o valor armazenado no endereço
        '''
        return str(self.enderecos[endereco])
    
    def busca_bloco(self, num_bloco: int, tam_bloco: int) -> list[int | str]:
        '''
        Busca e retorna o bloco de *num_bloco* e de *tam_bloco*
        '''
        return self.enderecos[num_bloco * tam_bloco : (num_bloco + 1) * tam_bloco]

    def __repr__(self) -> str:
        buffer = ''
        for i in range(self.qnt_instrucoes + self.qnt_dados):
            buffer += '{:>3} {:<}\n'.format(str(i), str(self.enderecos[i]))
        for i in range(1, self.qnt_enderecos_retorno + 1):
            buffer += '{:>3} {:<}\n'.format(str(self.tamanho + 1 - i), str(self.enderecos[-i]))
        return buffer
