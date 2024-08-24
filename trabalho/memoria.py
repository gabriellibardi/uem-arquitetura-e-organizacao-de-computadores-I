class memoria:

    def __init__(self, num_palavras : int) -> None:
        self.enderecos = [0] * num_palavras
    
    def __repr__(self) -> str:
        return str(self.enderecos)