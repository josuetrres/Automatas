class ValidadorAFND:
    def __init__(self):
        self.estados_actuales = {'q0'}

    def paso_epsilon(self, estados: set) -> set:
        nuevos_estados = set(estados)
        
        if 'q1' in nuevos_estados:
            nuevos_estados.update(['q2', 'q4'])
        if 'q3' in nuevos_estados:
            nuevos_estados.add('q2')
            
        return nuevos_estados

    def procesar_secuencia(self, secuencia: str) -> dict:
        secuencia_limpia = secuencia.replace('[', '').replace(']', '').replace(' ', '')
        partes = secuencia_limpia.split(',')

        arreglo = []
        for x in partes:
            if x:
                arreglo.append(x)

        for letra in arreglo:
            if letra.lower() not in ['r', 't', 'h', 'c']:
                return {"status": "error", "message": f"Carácter inválido '{letra}'. Usa r, t, h o c."}

        indice = 0
        total_datos = len(arreglo)

        while indice < total_datos:
            dato = arreglo[indice].lower()

            self.estados_actuales = self.paso_epsilon(self.estados_actuales)
            
            siguientes_estados = set()

            for estado in self.estados_actuales:
                
                if estado == 'q0' and dato == 'r':
                    siguientes_estados.add('q1')
                
                elif estado == 'q2' and dato in ['t', 'h']:
                    siguientes_estados.add('q3')
                
                elif estado in ['q3', 'q4'] and dato == 'c':
                    siguientes_estados.add('q5') # Combinación de q3 y q4

            self.estados_actuales = siguientes_estados

            if not self.estados_actuales:
                break

            indice += 1

        self.estados_actuales = self.paso_epsilon(self.estados_actuales)
        estados_finales = sorted(self.estados_actuales)

        if 'q5' in self.estados_actuales:
            return {
                "status": "aceptado",
                "message": "Paquete IoT válido.",
            }
        else:
            return {
                "status": "fallo",
                "message": "Paquete IoT inválido.",
            }


if __name__ == "__main__":
    validador1 = ValidadorAFND()
    print("Prueba 1 (r, c):", validador1.procesar_secuencia("[r, c]")) 

    validador2 = ValidadorAFND()
    print("Prueba 2 (r, t, h, c):", validador2.procesar_secuencia("[r, t, h, c]")) 

    validador3 = ValidadorAFND()
    print("Prueba 3 (r, t, c, h):", validador3.procesar_secuencia("[r, t, c, h]")) 
    
    validador4 = ValidadorAFND()
    print("Prueba 4 (r, t, h, c):", validador4.procesar_secuencia("[r, t, h, c]"))