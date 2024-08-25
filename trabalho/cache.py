class cache:

    def __init__(self, palavras_por_linha : int,
                  linhas_por_conjunto: int,
                  num_conjuntos: int) -> None:
        linha = [0] * palavras_por_linha
        conjunto = [linha] * linhas_por_conjunto
        enderecos = [conjunto] * num_conjuntos
        self.dados = enderecos[:len(enderecos)//2]
        self.instrucoes = enderecos[len(enderecos)//2:]

    def __repr__(self) -> str:
        return 'dados: ' + str(self.dados) + '\ninstrucoes: ' + str(self.instrucoes)
