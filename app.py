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
    analizador = AnalizadorEcommerce()
    resultado = analizador.procesar_secuencia(secuencia_str)
    return jsonify(resultado)


@app.route('/api/telemetria', methods=['POST'])
def api_telemetria():
    data = request.get_json()
    secuencia_str = data.get('secuencia', '')
    validador = ValidadorAFND()
    resultado = validador.procesar_secuencia(secuencia_str)
    return jsonify(resultado)

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
