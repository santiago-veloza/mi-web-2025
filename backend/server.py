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
    


if __name__ == "__main__":
    app.run(debug=True, port=5000)
