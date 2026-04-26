def validar_transaccion(cadena):
    estado = 'q0'
    for c in cadena:
        if estado == 'q0':
            if c == 'a':
                estado = 'q1'
            else:
                estado = 'q4'
        elif estado == 'q1':
            if c == 'c':
                estado = 'q2'
            else:
                estado = 'q4'
        elif estado == 'q2':
            if c == 'l':
                estado = 'q3'
            else:
                estado = 'q4'
        else: # q3 o q4
            estado = 'q4'
    
    return estado == 'q3'
                
if __name__ == "__main__":
    print(validar_transaccion("acld"))
    print(validar_transaccion("acl"))
    print(validar_transaccion("a"))
    