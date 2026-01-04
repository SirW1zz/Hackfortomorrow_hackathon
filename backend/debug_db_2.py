import psycopg2

try:
    conn = psycopg2.connect("postgresql://postgres.juqlebfjxzmcsctllffq:hLl3PZfEXJPua1WG@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres")
    cur = conn.cursor()
    
    # Check column types
    cur.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'Attendance'
    """)
    columns = cur.fetchall()
    print("Column Types:")
    for col in columns:
        print(col)

    print("\nRows with Name='justin':")
    cur.execute('SELECT * FROM "Attendance" WHERE "Name" = \'justin\'')
    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()

except Exception as e:
    print(f"Error: {e}")
