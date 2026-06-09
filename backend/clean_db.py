import psycopg2
import sys
import os

# Agregamos la ruta del backend para poder importar modulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import DATABASE_URL

print("Conectando a la base de datos para limpieza profunda...")
try:
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cursor = conn.cursor()

    print("Vaciando tablas loans, order_items, orders, categories (y tools si existe)...")
    cursor.execute("TRUNCATE TABLE loans, order_items, orders, categories CASCADE;")
    
    try:
        cursor.execute("TRUNCATE TABLE tools CASCADE;")
        print("Tabla tools eliminada exitosamente.")
    except Exception as e:
        print("La tabla tools no existe o ya estaba limpia.")

    print("Limpieza completada. La base de datos esta lista para produccion.")

except Exception as e:
    print(f"Error fatal: {e}")
finally:
    if 'conn' in locals() and conn:
        cursor.close()
        conn.close()
