class memoria:

    enderecos: list[int | str]
    
    def __init__(self, num_palavras : int) -> None:
        self.enderecos = [0] * num_palavras
        self.qnt_instrucoes = 0
        self.qnt_dados = 0
    
    def __repr__(self) -> str:
        return str(self.enderecos)