import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Veer453441@",   # same password you used in Workbench
        database="brainstrom"
    )
