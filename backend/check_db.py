import psycopg2

try:
    conn = psycopg2.connect("postgresql://postgres:hLl3PZfEXJPua1WG@db.juqlebfjxzmcsctllffq.supabase.co:5432/postgres")
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
        
        # Also let's check columns for the table to confirm it has 'name' and 'hour'
        cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table[0]}'")
        columns = cur.fetchall()
        print(f"  Columns: {[col[0] for col in columns]}")

    cur.close()
    conn.close()

except Exception as e:
    print(f"Error: {e}")
