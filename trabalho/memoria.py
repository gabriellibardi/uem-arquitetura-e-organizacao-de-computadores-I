class memoria:

    enderecos: list[int | str]
    
    def __init__(self, num_palavras : int) -> None:
        self.tamanho = num_palavras
        self.enderecos = [0] * num_palavras
        self.qnt_instrucoes = 0
        self.qnt_dados = 0
        self.qnt_enderecos_retorno = 0
    
    def __repr__(self) -> str:
        buffer = ''
        for i in range(self.qnt_instrucoes + self.qnt_dados):
            buffer += '{:>3} {:<}\n'.format(str(i), str(self.enderecos[i]))
        for i in range(1, self.qnt_enderecos_retorno + 1):
            buffer += '{:>3} {:<}\n'.format(str(self.tamanho + 1 - i), str(self.enderecos[-i]))
        return buffer
