from flask import Flask, render_template, request, jsonify, redirect, session
import mysql.connector
import re
import os

from models.course_model import get_courses_by_stream
from models.college_model import get_colleges

app = Flask(__name__)

# ---------------- SECRET KEY ----------------
app.secret_key = os.getenv("SECRET_KEY", "brainstorm_secret_key")


# ---------------- DATABASE (RAILWAY - SAFE & STABLE) ----------------
def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT", "3306")),
        autocommit=True
    )


# ---------------- PASSWORD VALIDATION ----------------
def is_valid_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"

    return True, ""


# ---------------- HOME ----------------
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html")


# ---------------- SERVICE ----------------
@app.route("/service")
def service():
    if "user" not in session:
        return redirect("/login")
    return render_template("service.html")


# ---------------- RESULT ----------------
@app.route("/result")
def result():
    if "user" not in session:
        return redirect("/login")
    return render_template("result.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        db = None
        cursor = None
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")

            if not username or not password or not confirm_password:
                return "All fields are required"

            if password != confirm_password:
                return "Passwords do not match"

            is_valid, message = is_valid_password(password)
            if not is_valid:
                return message

            db = get_db()
            cursor = db.cursor(dictionary=True)

            cursor.execute(
                "SELECT id FROM users WHERE username=%s",
                (username,)
            )
            if cursor.fetchone():
                return "Username already exists"

            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, password)
            )

            return redirect("/login")

        # 🔴 SHOW REAL MYSQL ERROR
        except mysql.connector.Error as err:
            print("MYSQL ERROR:", err)
            return f"MySQL Error: {err}"

        except Exception as e:
            print("GENERAL ERROR:", e)
            return f"Unexpected Error: {e}"

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    return render_template("regis.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        db = None
        cursor = None
        try:
            username = request.form.get("username")
            password = request.form.get("password")

            if not username or not password:
                return "All fields are required"

            db = get_db()
            cursor = db.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (username, password)
            )
            user = cursor.fetchone()

            if user:
                session["user"] = username
                return redirect("/")
            else:
                return "Invalid username or password"

        except mysql.connector.Error as err:
            print("MYSQL ERROR:", err)
            return f"MySQL Error: {err}"

        except Exception as e:
            print("LOGIN ERROR:", e)
            return f"Unexpected Error: {e}"

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# ---------------- API: COURSES ----------------
@app.route("/api/courses/<stream>")
def courses(stream):
    return jsonify(get_courses_by_stream(stream))


# ---------------- API: COLLEGES ----------------
@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    return jsonify(
        get_colleges(data["course"], int(data["percentage"]))
    )


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run()
