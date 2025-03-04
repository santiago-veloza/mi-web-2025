#test_db.py
from db import conectar_db

print("Intentando conectar a la base de datos...")

conn = conectar_db()
if conn:
    print("✅ Conexión exitosa a MariaDB")
    conn.close()
else:
    print("❌ No se pudo conectar a la base de datos")

