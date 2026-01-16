from flask import Blueprint, request, jsonify

penalty_bp = Blueprint("penalty", __name__)

PENALTIES = {
    "cooking_in_hostel": {
        "label": "Cooking food in hostel room / using prohibited appliances",
        "penalties": {
            1: {
                "fine": 1000,
                "action": "Confiscation of equipment",
                "notes": "Parents informed"
            },
            2: {
                "fine": 5000,
                "action": "Non-returnable confiscation + written warning",
                "notes": "Parent undertaking required"
            },
            3: {
                "fine": 10000,
                "action": "Suspension from hostel",
                "notes": "May extend up to full academic tenure"
            }
        }
    },

    "alcohol": {
        "label": "Possession / consumption of alcohol on campus",
        "penalties": {
            1: {
                "fine": 5000,
                "action": "Written warning",
                "notes": "Parents informed"
            },
            2: {
                "fine": 10000,
                "action": "Proctorial warning + counselling",
                "notes": "Parent undertaking required"
            },
            3: {
                "fine": 20000,
                "action": "Suspension up to 1 year OR expulsion",
                "notes": "Scholarship / internship may be withheld"
            }
        }
    }
}


@penalty_bp.route("/calculate", methods=["POST"])
def calculate_penalty():
    data = request.json
    offence_key = data.get("offence")
    count = int(data.get("count", 1))

    if offence_key not in PENALTIES:
        return jsonify({"error": "Invalid offence"}), 400

    offence = PENALTIES[offence_key]
    level = min(count, 3)
    result = offence["penalties"][level]

    return jsonify({
        "offence": offence["label"],
        "occurrence": level,
        "fine": result["fine"],
        "action": result["action"],
        "notes": result["notes"],
        "source": "Bennett University Students’ Discipline & Conduct Rules",
        "disclaimer": "Final decision rests with the University Proctorial Committee."
    })
