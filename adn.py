def validar_adn(cadena):
    estado = 'q0'   
    estados_actuales = ['q0']
    for c in cadena:
        nuevos_estados = set()
        for estado in estados_actuales:
            if estado == 'q0':
                if c == 'K':
                    nuevos_estados.add('q1')
                    nuevos_estados.add('q0')
                else:
                    nuevos_estados.add('q0')
            elif estado == 'q1':
                if c == 'G':
                    nuevos_estados.add('q2')
            elif estado == 'q2':
                if c == 'X':
                    nuevos_estados.add('q2')
                elif c == 'F':
                    nuevos_estados.add('q3')
            elif estado == 'q3':
                break
        estados_actuales = list(nuevos_estados)
        if 'q3' in estados_actuales:
            return True, estados_actuales
    return False, estados_actuales

if __name__ == "__main__":
    print(validar_adn("KGF"))          # True
    print(validar_adn("KGXF"))         # True
    print(validar_adn("KGXXF"))        # True
    print(validar_adn("AAAKGF"))       # True
    print(validar_adn("KKGF"))         # True
    print(validar_adn("FKGF"))         # True
    print(validar_adn("KGFFFFFFFF"))   # True
    print(validar_adn("ABCKGXFDEF"))   # True

    print(validar_adn("KF"))           # False
    print(validar_adn("KXF"))          # False
    print(validar_adn("GGGF"))         # False
    print(validar_adn("KG"))           # False
    print(validar_adn("KGX"))          # False
    print(validar_adn("XYZ"))          # False
    print(validar_adn("FGK"))          # False
    print(validar_adn("KGG"))      
     
            
                                    
                    
                    
                    
            
                
    