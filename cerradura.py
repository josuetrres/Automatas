class CerraduraInteligente:
    def __init__(self):
        self.estado_actual = 'q0'

    def procesar_secuencia(self, secuencia: str) -> dict:
        secuencia_limpia = secuencia.replace('[', '').replace(']', '').replace(' ', '')
        intentos = secuencia_limpia.split(',')
        recorrido_estados = ['q0']

        indice = 0
        total_intentos = len(intentos)

        while indice < total_intentos:
            intento = intentos[indice].lower()

            if intento not in ['c', 'f']:
                return {
                    "status": "error",
                    "message": f"Carácter inválido '{intento}' en la secuencia. Usa 'c' o 'f'."
                }

            if self.estado_actual == 'q3':
                break   #bloqueado

            if self.estado_actual == 'q0':
                if intento == 'c':
                    self.estado_actual = 'q4'
                elif intento == 'f':
                    self.estado_actual = 'q1'

            elif self.estado_actual == 'q1':
                if intento == 'c':
                    self.estado_actual = 'q4'
                elif intento == 'f':
                    self.estado_actual = 'q2'

            elif self.estado_actual == 'q2':
                if intento == 'c':
                    self.estado_actual = 'q4'
                elif intento == 'f':
                    self.estado_actual = 'q3' 

            elif self.estado_actual == 'q4':
                pass  # contra correcta

            recorrido_estados.append(self.estado_actual)
            indice += 1

        if self.estado_actual == 'q4':
            return {
                "status": "aceptado", 
                "message": "Acceso concedido.", 
                "estado_final": self.estado_actual,
                "recorrido": recorrido_estados
            }
        elif self.estado_actual == 'q3':
            return {
                "status": "bloqueado", 
                "message": "Alerta: Cerradura bloqueada por seguridad tras 3 fallos.", 
                "estado_final": self.estado_actual,
                "recorrido": recorrido_estados
            }
        else:
            intentos_restantes = 3 - int(self.estado_actual[1])
            return {
                "status": "fallo", 
                "message": f"Secuencia terminada sin éxito. Quedan {intentos_restantes} intentos.", 
                "estado_final": self.estado_actual,
                "recorrido": recorrido_estados
            }


if __name__ == "__main__":
    cerradura1 = CerraduraInteligente()
    print("Prueba 1:", cerradura1.procesar_secuencia("[f, f, f]"))

    cerradura2 = CerraduraInteligente()
    print("Prueba 2:", cerradura2.procesar_secuencia("f, f, c"))

    cerradura3 = CerraduraInteligente()
    print("Prueba 3:", cerradura3.procesar_secuencia("[c, f, c, c, f, c]"))