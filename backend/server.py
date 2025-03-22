#server.py 
from flask import Flask, request, jsonify
from flask_cors import CORS
import mariadb

app = Flask(__name__)
CORS(app) 


config = {
    "host": "localhost",
    "user": "root",       
    "password": "ucc2025", 
    "database": "eventosagg"
}

@app.route("/registrar_usuario", methods=["POST"])
def registrar_usuario():
    try:
        data = request.json
        email = data["email"]
        password = data["password"]

        conexion = mariadb.connect(**config)
        cursor = conexion.cursor()

        # Verificar si el usuario ya existe
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            return jsonify({"mensaje": "❌ El usuario ya está registrado."}), 400

        # Insertar nuevo usuario
        cursor.execute("INSERT INTO usuarios (email, password) VALUES (?, ?)", (email, password))
        conexion.commit()
        
        cursor.close()
        conexion.close()
        return jsonify({"mensaje": "✅ Usuario registrado correctamente"}), 200

    except mariadb.Error as e:
        return jsonify({"error": f"❌ Error en el registro: {e}"}), 500

@app.route("/iniciar_sesion", methods=["POST"])
def iniciar_sesion():
    try:
        data = request.json
        email = data["email"]
        password = data["password"]

        conexion = mariadb.connect(**config)
        cursor = conexion.cursor()

        # Verificar si existe el usuario
        cursor.execute("SELECT * FROM usuarios WHERE email = ? AND password = ?", (email, password))
        usuario = cursor.fetchone()

        cursor.close()
        conexion.close()

        if usuario:
            return jsonify({"mensaje": "✅ Inicio de sesión exitoso"}), 200
        else:
            return jsonify({"mensaje": "❌ No estas registrado"}), 401

    except mariadb.Error as e:
        return jsonify({"error": f"❌ Error en la autenticación: {e}"}), 500

@app.route("/agregar_evento", methods=["POST"])
def agregar_evento():
    try:
        data = request.json
        nombre = data["nombre"]
        fecha = data["fecha"]
        tiquetes = data["tiquetes"]
        precio = data["precio"]

        conexion = mariadb.connect(**config)
        cursor = conexion.cursor()
        query = "INSERT INTO eventos (nombre, fecha, tiquetes, precio) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (nombre, fecha, tiquetes, precio))
        conexion.commit()
        cursor.close()
        conexion.close()

        return jsonify({"mensaje": "✅ Evento guardado correctamente"}), 200

    except mariadb.Error as e:
        return jsonify({"error": f"❌ Error al guardar evento: {e}"}), 500
    
# Obtener eventos
@app.route("/eventos", methods=["GET"])
def obtener_eventos():
    try:
        conexion = mariadb.connect(**config)
        cursor = conexion.cursor(dictionary=True)  # Para obtener resultados como diccionarios

        cursor.execute("SELECT * FROM eventos")
        eventos = cursor.fetchall()  # Obtener todos los eventos desde la BD

        cursor.close()
        conexion.close()

        return jsonify(eventos), 200

    except mariadb.Error as e:
        return jsonify({"error": f"❌ Error al obtener eventos: {e}"}), 500

# Comprar un boleto
@app.route("/comprar_boleto", methods=["POST"])
def comprar_boleto():
    try:
        datos = request.json
        id_evento = datos.get("id")

        conexion = mariadb.connect(**config)
        cursor = conexion.cursor()

        # Obtener el número de boletos disponibles
        cursor.execute("SELECT tiquetes FROM eventos WHERE id = ?", (id_evento,))
        resultado = cursor.fetchone()

        if not resultado:
            return jsonify({"mensaje": "Evento no encontrado"}), 404

        tiquetes_disponibles = resultado[0]

        if tiquetes_disponibles > 0:
            # Restar un boleto y actualizar la base de datos
            cursor.execute("UPDATE eventos SET tiquetes = tiquetes - 1 WHERE id = ?", (id_evento,))
            conexion.commit()
            cursor.close()
            conexion.close()
            return jsonify({"mensaje": "Compra realizada con éxito"}), 200
        else:
            cursor.close()
            conexion.close()
            return jsonify({"mensaje": "No hay más boletos disponibles"}), 400

    except mariadb.Error as e:
        return jsonify({"error": f"❌ Error en la compra de boletos: {e}"}), 500




if __name__ == "__main__":
    app.run(debug=True, port=5000)
