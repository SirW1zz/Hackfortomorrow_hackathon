import psycopg2

try:
    # Using IPv6 address directly
    conn = psycopg2.connect("postgresql://postgres:hLl3PZfEXJPua1WG@[2406:da1c:f42:ae0a:7c17:ff02:4ca7:2fcf]:5432/postgres")
    cur = conn.cursor()
    
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    
    tables = cur.fetchall()
    print("Tables found:")
    for table in tables:
        print(f"- {table[0]}")
        cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table[0]}'")
        columns = cur.fetchall()
        print(f"  Columns: {[col[0] for col in columns]}")

    cur.close()
    conn.close()

except Exception as e:
    print(f"Error: {e}")
