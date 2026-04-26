def validar_conexion(cadena):
    estado = 'q0'
    for c in cadena:
        if estado == 'q0':
            if c == 's':
                estado = 'q1'
            else:
                estado = 'q4'
        elif estado == 'q1':
            if c == 'n':
                estado = 'q2'
            else:
                estado = 'q4'
        elif estado == 'q2':
            if c == 'a':
                estado = 'q3'
            else:
                estado = 'q4'
        else: # q3 o q4
            estado = 'q4'
    
    return estado == 'q3'

if __name__ == "__main__":
    print(validar_conexion("sna"))
    print(validar_conexion("snac"))
    