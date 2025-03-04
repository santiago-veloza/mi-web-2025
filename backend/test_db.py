#test_db.py
import mariadb

# Configuración de la conexión
config = {
    "host": "localhost",  # Cambia esto si MariaDB está en otro servidor
    "user": "root",  # Reemplaza con tu usuario de MariaDB
    "password": "ucc2025",  # Reemplaza con tu contraseña de MariaDB
    "database": "eventosagg"  # Reemplaza con el nombre de tu base de datos
}

def insertar_evento(nombre, fecha, tiquetes, precio):
    try:
        conexion = mariadb.connect(**config)
        cursor = conexion.cursor()
        query = "INSERT INTO eventos (nombre, fecha, tiquetes, precio) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (nombre, fecha, tiquetes, precio))
        conexion.commit()
        print("✅ Evento guardado correctamente")
    except mariadb.Error as e:
        print(f"❌ Error al guardar evento: {e}")
    finally:
        if conexion:
            conexion.close()
