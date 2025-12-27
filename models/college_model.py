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

def get_colleges(course, percentage):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            colleges.name AS college_name,
            courses.name AS course,
            courses.min_percentage
        FROM courses
        JOIN colleges ON colleges.id = courses.college_id
        WHERE courses.name = %s
        AND courses.min_percentage <= %s
        ORDER BY courses.min_percentage DESC
    """, (course, percentage))

    data = cursor.fetchall()

    cursor.close()
    db.close()
    return data
