# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import mariadb
from datetime import timedelta

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
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
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"mensaje": "❌ Email y contraseña son obligatorios."}), 400

        conexion = mariadb.connect(**config)
        cursor = conexion.cursor()

        # Verificar si el usuario ya existe
        cursor.execute("SELECT 1 FROM usuarios WHERE email = ?", (email,))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            cursor.close()
            conexion.close()
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
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"mensaje": "❌ Email y contraseña son obligatorios."}), 400

        conexion = mariadb.connect(**config)
        cursor = conexion.cursor(dictionary=True)

        # Verificar si existe el usuario
        cursor.execute("SELECT * FROM usuarios WHERE email = ? AND password = ? LIMIT 1", (email, password))
        usuario = cursor.fetchone()

        cursor.close()
        conexion.close()

        if usuario:
            return jsonify({"mensaje": "✅ Inicio de sesión exitoso"}), 200
        else:
            return jsonify({"mensaje": "❌ No estás registrado"}), 401

    except mariadb.Error as e:
        return jsonify({"error": f"❌ Error en la autenticación: {e}"}), 500

@app.route("/agregar_evento", methods=["POST"])
def agregar_evento():
    try:
        data = request.json
        print("📥 Datos recibidos:", data)  # Ver qué datos se están enviando

        nombre = data.get("nombre")
        fecha = data.get("fecha")
        tiquetes = data.get("tiquetes")
        precio = data.get("precio")
        hora = data.get("hora")

        if not all([nombre, fecha, tiquetes, precio, hora]):
            return jsonify({"mensaje": "❌ Todos los campos son obligatorios."}), 400

        conexion = mariadb.connect(**config)
        cursor = conexion.cursor()
        
        query = "INSERT INTO eventos (nombre, fecha, tiquetes, precio, hora) VALUES (?, ?, ?, ?, ?)"
        print("🛠 Ejecutando consulta SQL:", query)
        print("📦 Valores:", (nombre, fecha, tiquetes, precio, hora))

        cursor.execute(query, (nombre, fecha, tiquetes, precio, hora))
        conexion.commit()
        cursor.close()
        conexion.close()

        return jsonify({"mensaje": "✅ Evento guardado correctamente"}), 200

    except mariadb.Error as e:
        print(f"❌ Error en SQL: {e}")  # Imprime el error exacto
        return jsonify({"error": f"❌ Error al guardar evento: {e}"}), 500
@app.route("/eventos", methods=["GET"])
def obtener_eventos():
    try:
        conexion = mariadb.connect(**config)
        cursor = conexion.cursor()
        
        cursor.execute("SELECT nombre, fecha, tiquetes, precio, hora FROM eventos")
        eventos = []
        
        for evento in cursor.fetchall():
            eventos.append({
                "nombre": evento[0],
                "fecha": str(evento[1]),  # Convertir fecha a string
                "tiquetes": evento[2],
                "precio": float(evento[3]),  # Asegurar tipo numérico
                "hora": str(evento[4])  # Convertir hora a string
            })
        
        cursor.close()
        conexion.close()
        
        return jsonify(eventos), 200
    
    except mariadb.Error as e:
        return jsonify({"error": f"❌ Error al obtener eventos: {str(e)}"}), 500

@app.route("/comprar_boleto", methods=["POST"])
def comprar_boleto():
    try:
        datos = request.json
        id_evento = datos.get("id")

        if not id_evento:
            return jsonify({"mensaje": "❌ Se requiere el ID del evento."}), 400

        conexion = mariadb.connect(**config)
        cursor = conexion.cursor(dictionary=True)

        # Obtener el número de boletos disponibles
        cursor.execute("SELECT tiquetes FROM eventos WHERE id = ?", (id_evento,))
        resultado = cursor.fetchone()

        if not resultado:
            cursor.close()
            conexion.close()
            return jsonify({"mensaje": "❌ Evento no encontrado"}), 404

        tiquetes_disponibles = resultado["tiquetes"]

        if tiquetes_disponibles > 0:
            # Restar un boleto y actualizar la base de datos
            cursor.execute("UPDATE eventos SET tiquetes = tiquetes - 1 WHERE id = ?", (id_evento,))
            conexion.commit()
            cursor.close()
            conexion.close()
            return jsonify({"mensaje": "✅ Compra realizada con éxito"}), 200
        else:
            cursor.close()
            conexion.close()
            return jsonify({"mensaje": "❌ No hay más boletos disponibles"}), 400

    except mariadb.Error as e:
        return jsonify({"error": f"❌ Error en la compra de boletos: {e}"}), 500

def convertir_eventos(eventos):
    eventos_serializables = []
    for evento in eventos:
        if hasattr(evento, '__dict__'):  # Verifica que el objeto tenga __dict__
            evento_dict = evento.__dict__
            for clave, valor in evento_dict.items():
                if isinstance(valor, timedelta):
                    evento_dict[clave] = str(valor)  # Convierte timedelta a string
            eventos_serializables.append(evento_dict)
    return eventos_serializables

if __name__ == "__main__":
    app.run(debug=True, port=5000)
