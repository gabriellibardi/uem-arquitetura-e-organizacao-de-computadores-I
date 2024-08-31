class cache:
    def __init__(self, palavras_por_linha : int,
                  linhas_por_conjunto: int,
                  num_conjuntos: int) -> None:
        linha = [0] * palavras_por_linha
        conjunto = [linha] * linhas_por_conjunto
        enderecos = [conjunto] * num_conjuntos * 2
        self.dados = enderecos[:len(enderecos)//2]
        self.instrucoes = enderecos[len(enderecos)//2:]

    def __repr__(self) -> str:
        dados = ''
        instrucoes = ''
        for c in self.dados:
            dados += '\n' + str(c)
        for c in self.instrucoes:
            instrucoes += '\n' + str(c)
        return 'dados: ' + dados + \
            '\n\ninstrucoes: ' + instrucoes
