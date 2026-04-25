class AnalizadorEcommerce:
    def __init__(self):
        self.estados_actuales = {'q0'}

    def evaluar_secuencia(self, arreglo: list):
        indice = 0
        total_datos = len(arreglo)

        while indice < total_datos:
            dato = arreglo[indice].lower()
            siguientes_estados = set()

            for estado in self.estados_actuales:
                if estado == 'q0':
                    siguientes_estados.add('q0')
                    if dato == 'h': #si ve h va a q1
                        siguientes_estados.add('q1')
                
                elif estado == 'q1':
                    if dato == 's':
                        siguientes_estados.add('q2')
                
                elif estado == 'q2':
                    if dato == 's':
                        siguientes_estados.add('q2')
                    elif dato == 'c':
                        siguientes_estados.add('q3')
                
            self.estados_actuales = siguientes_estados

            if not self.estados_actuales:
                break

            indice += 1

        if 'q3' in self.estados_actuales:
            print("Éxito: Usuario clasificado como Comprador Potencial")
        else:
            print(f"Fallo: El usuario no cumplió el patrón. Estados finales: {self.estados_actuales}")



if __name__ == "__main__":
    
    analizador = AnalizadorEcommerce()
    print("Prueba 1 (Directo: h, s, c):", end=" ")
    analizador.evaluar_secuencia(['h', 's', 'c']) 

    analizador2 = AnalizadorEcommerce()
    print("Prueba 2 (Con distracciones: c, s, h, s, s, s, c):", end=" ")
    analizador2.evaluar_secuencia(['c', 's', 'h', 's', 's', 's', 'c']) 

    analizador3 = AnalizadorEcommerce()
    print("Prueba 3 (Con distracciones: c, s, h, s, s, s, c):", end=" ")
    analizador3.evaluar_secuencia(['c', 's', 'h', 's', 's', 's']) 