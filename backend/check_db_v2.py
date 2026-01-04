import psycopg2

try:
    # Using the new IPv4 connection string provided by the user
    conn = psycopg2.connect("postgresql://postgres.juqlebfjxzmcsctllffq:hLl3PZfEXJPua1WG@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres")
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
