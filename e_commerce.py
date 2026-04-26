class AnalizadorEcommerce:
    def __init__(self):
        self.estados_actuales = {'q0'}

    def procesar_secuencia(self, secuencia: str) -> dict:
        secuencia_limpia = secuencia.replace('[', '').replace(']', '').replace(' ', '')
        partes = secuencia_limpia.split(',')

        arreglo = []
        for x in partes:
            if x:
                arreglo.append(x)
        
        indice = 0
        total_datos = len(arreglo)

        while indice < total_datos:
            dato = arreglo[indice].lower()
            if dato not in ['h', 's', 'c']:
                return {"status": "error", "message": f"Carácter inválido '{dato}'. Usa h, s o c."}

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
            return {
                "status": "aceptado",
                "message": "Usuario clasificado como Comprador Potencial."
            }
        else:
            return {
                "status": "fallo",
                "message": "El usuario no cumplió el patrón de compra."
            }



if __name__ == "__main__":
    analizador = AnalizadorEcommerce()
    print("Prueba 1 (Directo: h, s, c):", analizador.procesar_secuencia("[h, s, c]")) 
    print("Prueba 2", analizador.procesar_secuencia("[h, s, s, c]"))
    print("Prueba 3", analizador.procesar_secuencia("[c, s, h, s, s, s]"))
