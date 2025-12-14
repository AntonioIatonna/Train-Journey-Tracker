from db import get_connection

def fetch_stations():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name FROM stations ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_or_create_station(name):
    name = name.strip()

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT id FROM stations WHERE name = ?", (name,))
    row = cur.fetchone()

    if row:
        conn.close()
        return row["id"]

    cur.execute("INSERT INTO stations (name) VALUES (?)", (name,))
    conn.commit()
    station_id = cur.lastrowid
    conn.close()
    return station_id