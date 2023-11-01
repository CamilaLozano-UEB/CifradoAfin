import cifrado_afin
from flask import Flask, render_template, request, jsonify
from flask_limiter import Limiter
from Database import Database

app = Flask(__name__)
app.secret_key = 'DwUi<£_Ma}["JqaE6Vpu676RQ57w:FD?'  # Cambia esto por una clave segura

limiter = Limiter(
    app,
    storage_uri="mysql://root@localhost:3306/seguridaddb"
)


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
@limiter.limit("3 per minute")  # Establece el límite de 3 intentos por minuto
def login():
    data = request.get_json()
    if request.headers.get('Content-Type') == 'application/json':
        # Esta parte maneja las solicitudes JSON
        username = data.get("username")
        password = data.get("password")
    else:
        # Si no es JSON, se asume que es un formulario
        username = data.get("username")
        password = data.get("password")
    # Conecta con la base de datos
    cursor = Database().db.cursor()

    # Realiza una consulta para buscar el usuario en la tabla login
    cursor.execute("SELECT * FROM login WHERE usuario = %s", (username,))
    result = cursor.fetchone()

    # Cierra el cursor
    cursor.close()

    if result:
        # Obtiene la contraseña cifrada almacenada en la base de datos
        stored_password = result[1]

        # Compara la contraseña cifrada del usuario con la almacenada en la base de datos
        if password == stored_password:
            return jsonify({"success": True})
        else:
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({"success": False})
            else:
                return jsonify({"success": False, "message": "Nombre de usuario o contraseña incorrectos"})
    else:
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({"success": False})
        else:
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
