regs = {
    'r0' : 0,
    'r1' : 0,
    'r2' : 0,
    'r3' : 0,
    'r4' : 0,
    'r5' : 0,
    'r6' : 0,
    'r7' : 0,
    'r8' : 0,
    'r9' : 0,
    'r10' : 0,
    'r11' : 0,
    'r12' : 0,
    'r13' : 0,
    'r14' : 0,
    'r15' : 0,
    'r16' : 0,
    'r17' : 0,
    'r18' : 0,
    'r19' : 0,
    'r20' : 0,
    'r21' : 0,
    'r22' : 0,
    'r23' : 0,
    'r24' : 0,
    'r25' : 0,
    'r26' : 0,
    'r27' : 0,
    'r28' : 0,
    'r29' : 0,
    'r30' : 0,
    'r31' : 0,
}

regs_esp = {
    'pc' : 0,
    'rsp' : 0,
    'ra' : 0,
    'of' : 0
}

def imprime_registradores():
    '''
    Imprime na tela todos os registradores
    '''
    print('----- REGISTRADORES DE USO ESPECÍFICO -----\n')
    for k, v in regs_esp.items():
        print('{:>3} = {:<3}| '.format(k.upper(), v), end='')

    print('\n\n' + '-' * 29 + ' REGISTRADORES DE USO GERAL ' + '-' * 29 + '\n')
    c = 0
    for k, v in regs.items():
        print('{:>3} = {:<3}| '.format(k, v), end='')
        c += 1
        if c == 8:    
            print()
            c = 0
