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
