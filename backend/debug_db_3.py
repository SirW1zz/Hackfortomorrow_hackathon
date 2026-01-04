import psycopg2

try:
    conn = psycopg2.connect("postgresql://postgres.juqlebfjxzmcsctllffq:hLl3PZfEXJPua1WG@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres")
    cur = conn.cursor()
    
    print("Fetching all rows:")
    cur.execute('SELECT "Name", "Hour" FROM "Attendance"')
    rows = cur.fetchall()
    
    for row in rows:
        print(f"Name: '{row[0]}', Hour: {row[1]}")

    cur.close()
    conn.close()

except Exception as e:
    print(f"Error: {e}")
