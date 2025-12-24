from db import get_db

def get_colleges(course, percentage):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT name AS college, fees, infra, placement
        FROM colleges
        WHERE course=%s
        AND %s BETWEEN min_percentage AND max_percentage
    """, (course, percentage))

    colleges = cursor.fetchall()
    db.close()
    return colleges
