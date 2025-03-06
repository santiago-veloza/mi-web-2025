#db.py
import mariadb
import sys

def conectar_db():
    try:
        conn = mariadb.connect(
            host="localhost",  # O la IP del servidor
            user="root",  # Cambia esto por tu usuario
            password="ucc2025",  # Si tu usuario tiene contraseña, ponla aquí
            database="eventosagg",  # Nombre de tu base de datos
            port=3306  # Puerto de MariaDB
        )
        print("✅ Conexión establecida")
        return conn
    except mariadb.Error as e:
        print(f"❌ Error al conectar con MariaDB: {e}")
        sys.exit(1)
