class cache:

    def __init__(self, palavras_por_linha : int,
                  linhas_por_conjunto: int,
                  num_conjuntos: int) -> None:
        linha = [0] * palavras_por_linha
        conjunto = [linha] * linhas_por_conjunto
        self.enderecos = [conjunto] * num_conjuntos

    def __repr__(self) -> str:
        return str(self.enderecos)
