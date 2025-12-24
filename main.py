from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ==================================================
# STREAM → COURSES
# (Used by: GET /api/courses/<stream>)
# ==================================================

STREAM_COURSES = {
    "science": ["BTech", "BSc", "BCA", "MBBS", "BDS", "BAMS", "BHMS"],
    "commerce": ["BBA", "BCom", "MBA"],
    "arts": ["BA", "MA"]
}

# ==================================================
# COURSE → COLLEGES (NORMALIZED KEYS)
# Keys MUST be uppercase with NO spaces or dots
# ==================================================

COLLEGE_DATA = {

    "BTECH": {
        "70_90": [
            {"college": "VIT Vellore", "fees": 60, "infra": 80, "placement": 75},
            {"college": "SRM University", "fees": 65, "infra": 75, "placement": 70}
        ],
        "ABOVE_90": [
            {"college": "IIT Bombay", "fees": 30, "infra": 95, "placement": 95},
            {"college": "IIT Delhi", "fees": 28, "infra": 94, "placement": 96}
        ]
    },

    "BSC": {
        "70_90": [
            {"college": "Christ University", "fees": 40, "infra": 70, "placement": 65}
        ],
        "ABOVE_90": [
            {"college": "IISc Bangalore", "fees": 20, "infra": 98, "placement": 90}
        ]
    },

    "BCA": {
        "70_90": [
            {"college": "Medicaps University", "fees": 45, "infra": 70, "placement": 65}
        ],
        "ABOVE_90": [
            {"college": "NIT Trichy", "fees": 30, "infra": 90, "placement": 85}
        ]
    },

    "MBBS": {
        "70_90": [
            {"college": "AFMC Pune", "fees": 25, "infra": 90, "placement": 85},
            {"college": "KMC Manipal", "fees": 65, "infra": 85, "placement": 80}
        ],
        "ABOVE_90": [
            {"college": "AIIMS Delhi", "fees": 10, "infra": 98, "placement": 95},
            {"college": "CMC Vellore", "fees": 15, "infra": 95, "placement": 92}
        ]
    },

    "BDS": {
        "70_90": [
            {"college": "Manipal Dental College", "fees": 55, "infra": 80, "placement": 70}
        ],
        "ABOVE_90": [
            {"college": "Maulana Azad Dental College", "fees": 20, "infra": 92, "placement": 88}
        ]
    },

    "BAMS": {
        "70_90": [
            {"college": "Govt Ayurvedic College", "fees": 30, "infra": 65, "placement": 60}
        ],
        "ABOVE_90": [
            {"college": "National Institute of Ayurveda", "fees": 20, "infra": 80, "placement": 75}
        ]
    },

    "BHMS": {
        "70_90": [
            {"college": "Govt Homeopathic Medical College", "fees": 25, "infra": 60, "placement": 55}
        ],
        "ABOVE_90": [
            {"college": "National Institute of Homoeopathy", "fees": 20, "infra": 75, "placement": 70}
        ]
    },

    "BBA": {
        "70_90": [
            {"college": "NMIMS Mumbai", "fees": 55, "infra": 80, "placement": 70}
        ]
    },

    "MBA": {
        "ABOVE_90": [
            {"college": "IIM Ahmedabad", "fees": 35, "infra": 95, "placement": 98},
            {"college": "IIM Bangalore", "fees": 34, "infra": 94, "placement": 97}
        ]
    }
}

# ==================================================
# ROUTES
# ==================================================

@app.route("/")
def service_page():
    return render_template("service.html")


@app.route("/result")
def result_page():
    return render_template("result.html")


# ---------- GET COURSES BASED ON STREAM ----------
@app.route("/api/courses/<stream>")
def get_courses(stream):
    return jsonify(STREAM_COURSES.get(stream.lower(), []))


# ---------- RECOMMEND COLLEGES (FOR Chart.js) ----------
@app.route("/api/recommend", methods=["POST"])
def recommend_colleges():
    data = request.get_json()

    # 🔥 NORMALIZE COURSE NAME (CRITICAL FIX)
    raw_course = data.get("course", "")
    course = (
        raw_course
        .replace(".", "")
        .replace(" ", "")
        .upper()
    )

    percentage = float(data.get("percentage", 0))

    # Percentage slab logic
    if percentage >= 90:
        slab = "ABOVE_90"
    elif percentage >= 70:
        slab = "70_90"
    else:
        slab = "70_90"  # fallback

    colleges = COLLEGE_DATA.get(course, {}).get(slab, [])

    return jsonify(colleges)


# ==================================================
# RUN SERVER
# ==================================================

if __name__ == "__main__":
    app.run(debug=True)
