regs = {
    'pc' : 0,
    'rsp' : 0,
    'ra' : 0,
    'of' : 0
}

def imprime_registradores():
    '''
    Imprime na tela todos os registradores
    '''
    for v, k in regs.items():
        print(v + ': ' + str(k))