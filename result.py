def get_courses_by_stream(stream):
    stream = stream.lower()

    courses = {
        "science": [
            "BTech", "BSc", "BCA", "BPharma", "BArch"
        ],
        "commerce": [
            "BCom", "BBA", "CA", "CS"
        ],
        "arts": [
            "BA", "BFA", "BJMC", "BSW"
        ]
    }

    return courses.get(stream, [])


def recommend_colleges(stream, course, percentage):
    result = []

    if percentage < 55:
        result = [
            "Private Institute of Technology",
            "Regional Degree College",
            "Local Professional College"
        ]

    elif 55 <= percentage < 70:
        result = [
            "State Government College",
            "Autonomous College",
            "Reputed Private University"
        ]

    elif 70 <= percentage < 90:
        result = [
            "Top State University",
            "National Institute of Technology",
            "Premier Private University"
        ]

    else:
        result = [
            "IIT / IISc Level University",
            "Top Central University",
            "International Collaboration Institute"
        ]

    return result
