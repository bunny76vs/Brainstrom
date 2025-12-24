from flask import Flask, render_template, request, jsonify, redirect, session
import mysql.connector
import re   # ✅ added for password validation

from models.course_model import get_courses_by_stream
from models.college_model import get_colleges

app = Flask(__name__)
app.secret_key = "brainstorm_secret_key"


# ---------------- DATABASE ----------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Veer453441@",   # your password
        database="brainstrom"
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
        try:
            print("FORM DATA:", request.form)

            username = request.form["username"]
            password = request.form["password"]
            confirm_password = request.form["confirm_password"]

            # confirm password check
            if password != confirm_password:
                return "Passwords do not match"

            # 🔐 password validation (ONLY NEW LOGIC)
            is_valid, message = is_valid_password(password)
            if not is_valid:
                return message

            db = get_db()
            cursor = db.cursor(dictionary=True)

            # username uniqueness (UNCHANGED)
            cursor.execute(
                "SELECT * FROM users WHERE username=%s",
                (username,)
            )
            existing_user = cursor.fetchone()

            if existing_user:
                db.close()
                return "Username already exists"

            # insert user
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, password)
            )
            db.commit()
            db.close()

            print("✅ USER INSERTED SUCCESSFULLY")
            return redirect("/login")

        except Exception as e:
            print("❌ SIGNUP ERROR:", e)
            return "Signup failed. Check server logs."

    return render_template("regis.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            print("LOGIN DATA:", request.form)

            username = request.form["username"]
            password = request.form["password"]

            db = get_db()
            cursor = db.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (username, password)
            )
            user = cursor.fetchone()
            db.close()

            if user:
                session["user"] = username
                print("✅ LOGIN SUCCESS")
                return redirect("/")
            else:
                print("❌ LOGIN FAILED")
                return "Invalid username or password"

        except Exception as e:
            print("❌ LOGIN ERROR:", e)
            return "Login failed. Check server logs."

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


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
