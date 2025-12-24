from db import get_db

def get_courses_by_stream(stream):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT name FROM courses WHERE stream=%s",
        (stream,)
    )

    courses = [row["name"] for row in cursor.fetchall()]
    db.close()
    return courses
