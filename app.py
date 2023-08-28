from flask import Flask, render_template, request, jsonify

import cifrado_afin

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cifrar', methods=['POST'])
def cifrar():
    a = int(request.form['a'])
    b = int(request.form['b'])
    mensaje = request.form['mensaje']

    # Realizar el cifrado afín con a y b
    mensaje_cifrado = cifrado_afin.affine_encryption(mensaje, a, b)

    return jsonify({'mensaje_cifrado': mensaje_cifrado})


@app.route('/descifrar', methods=['POST'])
def descifrar():
    mensaje = request.form['mensajeCifrado']

    # Realizar el cifrado afín con a y b
    mensaje_descifrado = cifrado_afin.returnData(mensaje)

    return jsonify(mensaje_descifrado)


@app.route('/get_letter_frequencies')
def get_letter_frequencies():
    text = request.args.get('text')  # Obtén el texto para calcular las frecuencias
    top_letters = cifrado_afin.returnChart(text)
    return jsonify(top_letters)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
