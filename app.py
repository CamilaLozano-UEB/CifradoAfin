import cifrado_afin
from flask import Flask, render_template, request, jsonify, session
from Database import Database

app = Flask(__name__)
app.secret_key = 'DwUi<£_Ma}["JqaE6Vpu676RQ57w:FD?'  # clave segura
app.config['PERMANENT_SESSION_LIFETIME'] = 60  # Tiempo


def init_session():
    session['login_attempts'] = 0
    session['block_time'] = 0


@app.route('/')
def index():
    session['login_attempts'] = 0
    session['block_time'] = 0
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if session['block_time'] > 0:
            return jsonify('Usuario bloqueado, vuelva a intentarlo en {} segundos'.format(session['block_time']))

        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        cursor = Database().db.cursor()

        # Realiza una consulta para buscar el usuario en la tabla login
        cursor.execute("SELECT * FROM login WHERE usuario = %s", (username,))
        result = cursor.fetchone()
        # Cierra el cursor
        cursor.close()

        # Obtiene la contraseña cifrada almacenada en la base de datos
        stored_password = result[1]
        # Compara la contraseña cifrada del usuario con la almacenada en la base de datos
        if password == stored_password:
            return jsonify({"success": True})
        else:
            session['login_attempts'] += 1
            return jsonify({"success": False, "message": "Nombre de usuario o contraseña incorrectos"})


@app.route('/index')
def index2():
    return render_template("index.html")


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


@app.errorhandler(429)
def ratelimit_error(e):
    return "Demasiados intentos. Por favor, espere un momento antes de intentar nuevamente.", 429


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)