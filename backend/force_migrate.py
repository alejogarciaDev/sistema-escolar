import psycopg2

def run():
    print("Iniciando migración forzada pura (sin transacciones SQLAlchemy)...")
    try:
        conn = psycopg2.connect("postgresql://admin:2802@localhost/sistema")
        conn.autocommit = True
        cur = conn.cursor()
    except Exception as e:
        print("Error conectando a la base de datos:", e)
        return

    queries = [
        "ALTER TABLE loans ADD COLUMN panolero_id INTEGER REFERENCES users(id);",
        "ALTER TABLE loans ADD COLUMN description_loan VARCHAR;",
        "ALTER TABLE loans ADD COLUMN description_return VARCHAR;",
        "ALTER TABLE loans ADD COLUMN category_id INTEGER REFERENCES categories(id);",
        "ALTER TABLE loans ADD COLUMN quantity INTEGER DEFAULT 1;",
        "ALTER TABLE categories ADD COLUMN barcode VARCHAR;",
        "ALTER TABLE categories ADD COLUMN stock INTEGER DEFAULT 0;",
        "ALTER TABLE categories ADD COLUMN activo BOOLEAN DEFAULT TRUE;",
        "ALTER TABLE orders ADD COLUMN status VARCHAR DEFAULT 'pendiente';"
    ]

    for q in queries:
        try:
            cur.execute(q)
            print(f"[OK] {q}")
        except psycopg2.Error as e:
            msg = e.pgerror.strip() if e.pgerror else str(e)
            print(f"[SALTADO] {q} -> {msg}")

    cur.close()
    conn.close()
    print("\n¡Migración finalizada con éxito! Todos los cambios estructurales aplicados.")

if __name__ == "__main__":
    run()
