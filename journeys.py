from db import get_connection

def insert_journey(data):
    """
    data: dict containing mandatory and optional fields
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO journeys (
            operator,
            originStation,
            destinationStation,
            journeyDate,
            trainNumber,
            locomotiveType,
            locomotiveNumber,
            carType,
            carNumber,
            gpxPath,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["operator"],
        data["originStation"],
        data["destinationStation"],
        data["journeyDate"],
        data.get("trainNumber"),
        data.get("locomotiveType"),
        data.get("locomotiveNumber"),
        data.get("carType"),
        data.get("carNumber"),
        data.get("gpxPath"),
        data.get("notes"),
    ))

    journeyID = cur.lastrowid

    # Insert intermediate stops if provided
    for order, stationID in enumerate(data.get("stops", []), start=1):
        cur.execute("""
            INSERT INTO journey_stops (journeyID, stationID, stopOrder)
            VALUES (?, ?, ?)
        """, (journeyID, stationID, order))

    conn.commit()
    conn.close()


def fetch_all_journeys():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT
            j.journeyDate,
            o.name AS operator,
            s1.name AS originStation,
            s2.name AS destinationStation,
            j.trainNumber,
            j.locomotiveType,
            j.locomotiveNumber,
            j.carType,
            j.carNumber,
            j.gpxPath,
            j.notes,
            GROUP_CONCAT(
                s_stop.name
                ORDER BY js.stopOrder
                SEPARATOR ' → '
            ) AS intermediateStops
        FROM journeys j
        JOIN operators o ON j.operator = o.id
        JOIN stations s1 ON j.originStation = s1.id
        JOIN stations s2 ON j.destinationStation = s2.id
        LEFT JOIN journey_stops js ON j.id = js.journeyID
        LEFT JOIN stations s_stop ON js.stationID = s_stop.id
        GROUP BY j.id
        ORDER BY j.journeyDate DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows