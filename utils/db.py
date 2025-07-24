import psycopg2 

def get_connection():
    return psycopg2.connect(
        dbname="users",
        user="postgres",
        password="darkata123",
        host="localhost",
        port=5432,
    )

def execute_query(query,params=None,fetchone=False,fetchall=False):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(query,params)
                if fetchone:
                    return cur.fetchone()
                if fetchall:
                    return cur.fetchall()
    finally:
        conn.close()