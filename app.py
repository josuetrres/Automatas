from flask import Flask, render_template, request, jsonify
from cerradura import CerraduraInteligente
from e_commerce import AnalizadorEcommerce
from telemetria import ValidadorAFND
from adn import validar_adn
from transaccion import validar_transaccion
from tcp import validar_conexion
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cerradura')
def cerradura_page():
    return render_template('cerradura.html')


@app.route('/ecommerce')
def ecommerce_page():
    return render_template('ecommerce.html')


@app.route('/telemetria')
def telemetria_page():
    return render_template('telemetria.html')


@app.route('/transaccion')
def transaccion_page():
    return render_template('transaccion.html')


@app.route('/tcp')
def tcp_page():
    return render_template('tcp.html')


@app.route('/adn')
def adn_page():
    return render_template('adn.html')


@app.route('/api/cerradura', methods=['POST'])
def api_cerradura():
    data = request.get_json()
    secuencia = data.get('secuencia', '')
    cerradura = CerraduraInteligente()
    resultado = cerradura.procesar_secuencia(secuencia)
    return jsonify(resultado)


@app.route('/api/ecommerce', methods=['POST'])
def api_ecommerce():
    data = request.get_json()
    secuencia_str = data.get('secuencia', '')
    limpia = secuencia_str.replace('[', '').replace(']', '').replace(' ', '')
    arreglo = [x for x in limpia.split(',') if x]
    analizador = AnalizadorEcommerce()

    indice = 0
    total_datos = len(arreglo)
    while indice < total_datos:
        dato = arreglo[indice].lower()
        if dato not in ['h', 's', 'c']:
            return jsonify({"status": "error", "message": f"Carácter inválido '{dato}'. Usa h, s o c."})
        siguientes_estados = set()
        for estado in analizador.estados_actuales:
            if estado == 'q0':
                siguientes_estados.add('q0')
                if dato == 'h':
                    siguientes_estados.add('q1')
            elif estado == 'q1':
                if dato == 's':
                    siguientes_estados.add('q2')
            elif estado == 'q2':
                if dato == 's':
                    siguientes_estados.add('q2')
                elif dato == 'c':
                    siguientes_estados.add('q3')
        analizador.estados_actuales = siguientes_estados
        if not analizador.estados_actuales:
            break
        indice += 1

    estados_finales = sorted(analizador.estados_actuales)
    if 'q3' in analizador.estados_actuales:
        return jsonify({
            "status": "aceptado",
            "message": "Usuario clasificado como Comprador Potencial.",
            "estado_final": "q3",
            "estados_activos": estados_finales,
        })
    else:
        return jsonify({
            "status": "fallo",
            "message": "El usuario no cumplió el patrón de compra.",
            "estados_activos": estados_finales,
        })


@app.route('/api/telemetria', methods=['POST'])
def api_telemetria():
    data = request.get_json()
    secuencia_str = data.get('secuencia', '')
    limpia = secuencia_str.replace('[', '').replace(']', '').replace(' ', '')
    arreglo = [x for x in limpia.split(',') if x]
    validador = ValidadorAFND()

    for letra in arreglo:
        if letra.lower() not in ['r', 't', 'h', 'c']:
            return jsonify({"status": "error", "message": f"Carácter inválido '{letra}'. Usa r, t, h o c."})

    indice = 0
    total_datos = len(arreglo)
    while indice < total_datos:
        dato = arreglo[indice].lower()
        validador.estados_actuales = validador.paso_epsilon(validador.estados_actuales)
        siguientes_estados = set()
        for estado in validador.estados_actuales:
            if estado == 'q0' and dato == 'r':
                siguientes_estados.add('q1')
            elif estado == 'q2' and dato in ['t', 'h']:
                siguientes_estados.add('q3')
            elif estado in ['q3', 'q4'] and dato == 'c':
                siguientes_estados.add('q5')
        validador.estados_actuales = siguientes_estados
        if not validador.estados_actuales:
            break
        indice += 1

    validador.estados_actuales = validador.paso_epsilon(validador.estados_actuales)
    estados_finales = sorted(validador.estados_actuales)

    if 'q5' in validador.estados_actuales:
        return jsonify({
            "status": "aceptado",
            "message": "Paquete IoT válido.",
            "estados_activos": estados_finales,
        })
    else:
        return jsonify({
            "status": "fallo",
            "message": "Paquete IoT inválido.",
            "estados_activos": estados_finales,
        })

@app.route('/api/transaccion', methods=['POST'])
def api_transaccion():
    data = request.get_json()
    secuencia_str = data.get('secuencia', '')
    validador = validar_transaccion(secuencia_str)
    if validador:
        return jsonify({
            "status": "aceptado",
            "message": "Transacción válida.",
            "estado_final": "q3",
            "estados_activos": ["q3"],
        })
    else:
        return jsonify({
            "status": "fallo",
            "message": "Transacción inválida.",
            "estado_final": "q4",
            "estados_activos": ["q4"],
        })

@app.route('/api/tcp', methods=['POST'])
def api_tcp():
    data = request.get_json()
    secuencia_str = data.get('secuencia', '')
    validador = validar_conexion(secuencia_str)
    if validador:
        return jsonify({
            "status": "aceptado",
            "message": "Conexión válida.",
            "estado_final": "q3",
            "estados_activos": ["q3"],
        })
    else:
        return jsonify({
            "status": "fallo",
            "message": "Conexión inválida.",
            "estado_final": "q4",
            "estados_activos": ["q4"],
        })
    
@app.route('/api/adn', methods=['POST'])
def api_adn():
    data = request.get_json()
    secuencia_str = data.get('secuencia', '')
    validador, estados_finales = validar_adn(secuencia_str)
    if validador:
        return jsonify({
            "status": "aceptado",
            "message": "ADN válido.",
            "estado_final": "q3",
            "estados_activos": estados_finales,
        })
    else:
        return jsonify({
            "status": "fallo",
            "message": "ADN inválido.",
            "estado_final": "q4",
            "estados_activos": estados_finales,
        })

    


if __name__ == '__main__':
    app.run(debug=True)
