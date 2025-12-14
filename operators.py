from db import get_connection

def fetch_operators():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name FROM operators ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_or_create_operator(name):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT id FROM operators WHERE name = ?", (name,))
    row = cur.fetchone()

    if row:
        conn.close()
        return row["id"]

    cur.execute("INSERT INTO operators (name) VALUES (?)", (name,))
    conn.commit()
    operator_id = cur.lastrowid
    conn.close()
    return operator_id