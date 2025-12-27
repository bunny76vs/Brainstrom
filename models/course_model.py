import mysql.connector
import os

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT", "3306")),
        autocommit=True
    )

def get_courses_by_stream(stream):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM courses WHERE stream=%s",
        (stream,)
    )

    data = cursor.fetchall()

    cursor.close()
    db.close()
    return data
