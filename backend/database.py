import psycopg2

# Connection string
DB_URL = "postgresql://postgres.juqlebfjxzmcsctllffq:hLl3PZfEXJPua1WG@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres"

def get_db_connection():
    return psycopg2.connect(DB_URL)

def get_all_students():
    """
    Returns a list of all student names from the Attendance table.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT "Name" FROM "Attendance"')
        rows = cur.fetchall()
        students = [row[0] for row in rows]
        cur.close()
        conn.close()
        return students
    except Exception as e:
        print(f"Error fetching students: {e}")
        return []

def update_attendance(name, status):
    """
    Updates the attendance for the given user.
    status: 1 for Present, 0 for Absent
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('UPDATE "Attendance" SET "Hour" = %s WHERE "Name" = %s', (status, name))
        rows_updated = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        
        if rows_updated > 0:
            status_str = "Present" if status == 1 else "Absent"
            print(f"Marked {name} as {status_str}.")
            return True
        else:
            print(f"Warning: User {name} not found in 'Attendance' table.")
            return False
            
    except Exception as e:
        print(f"Error updating database for {name}: {e}")
        return False

def clean_database_names():
    """
    General utility to clean ALL names in the database.
    Removes leading/trailing whitespace and newlines.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        print("Cleaning database names (trimming whitespace/newlines)...")
        # Trim whitespace
        cur.execute('UPDATE "Attendance" SET "Name" = TRIM(BOTH FROM "Name")')
        # Remove newlines/carriage returns
        cur.execute('UPDATE "Attendance" SET "Name" = REGEXP_REPLACE("Name", E\'[\\n\\r]+\', \'\', \'g\')')
        
        rows_affected = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        print(f"Database cleaning complete. Rows affected: {rows_affected}")
        return True
    except Exception as e:
        print(f"Error cleaning database: {e}")
        return False

def reset_attendance():
    """
    Optional: Reset everyone to 0 (Absent) before a new day/scan block?
    For now, we just use update_attendance to set 0 or 1.
    """
    pass
