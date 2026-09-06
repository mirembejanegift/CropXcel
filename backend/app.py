from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
import os
from services.soil_service import get_isda_token
from services.farm_profile_service import get_farm_profile
from services.model_service import predict_top_crops
from flask import request
from flask import session
from services.auth_service import register_user, authenticate_user
from services.farm_plan_service import generate_farm_plan


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5500", "http://localhost:5500"])

app.secret_key = "temporary-dev-secret-change-this-later" 

@app.route("/api/generate-plan", methods=["POST"])
def generate_plan():
    try:
        data = request.get_json()

        crop = data.get("crop")
        farm_profile = data.get("farm_profile")

        if not crop or not farm_profile:
            return jsonify({
                "success": False,
                "error": "Request must include 'crop' and 'farm_profile'"
            }), 400

        plan = generate_farm_plan(crop, farm_profile)

        return jsonify({
            "success": True,
            "farm_plan": plan
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
        

@app.route("/api/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        name = data.get("fullname") or data.get("name")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "farmer")
        location = data.get("location")

        if not name or not email or not password:
            return jsonify({"success": False, "error": "name, email, and password are required"}), 400

        user = register_user(name, email, password, role, location)

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]

        return jsonify({"success": True, "user": user})

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"success": False, "error": "email and password are required"}), 400

        user = authenticate_user(email, password)

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]

        return jsonify({"success": True, "user": user})
    

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 401
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True})


@app.route("/api/current-user")
def current_user():
    if "user_id" not in session:
        return jsonify({"success": False, "error": "Not logged in"}), 401

    return jsonify({
        "success": True,
        "user": {
            "id": session["user_id"],
            "name": session.get("user_name")
        }
    })

@app.route("/api/analyse-farm", methods=["POST"])
def analyse_farm():
    try:
        data = request.get_json()

        if not data or "latitude" not in data or "longitude" not in data:
            return jsonify({
                "success": False,
                "error": "Request must include 'latitude' and 'longitude'"
            }), 400

        latitude = data["latitude"]
        longitude = data["longitude"]

        # Basic validation
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            return jsonify({
                "success": False,
                "error": "Invalid latitude or longitude values"
            }), 400

        profile = get_farm_profile(latitude, longitude)
        top_crops = predict_top_crops(profile)

        return jsonify({
            "success": True,
            "farm_profile": profile,
            "top_crops": top_crops
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/test-prediction")
def test_prediction():
    try:
        latitude = 0.3476
        longitude = 32.5825

        profile = get_farm_profile(latitude, longitude)
        top_crops = predict_top_crops(profile)

        return jsonify({
            "success": True,
            "farm_profile": profile,
            "top_crops": top_crops
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
        

@app.route("/api/test-farm-profile")
def test_farm_profile():
    try:
        latitude = 0.3476
        longitude = 32.5825

        profile = get_farm_profile(latitude, longitude)

        return jsonify({
            "success": True,
            "farm_profile": profile
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    try:
        latitude = 0.3476
        longitude = 32.5825

        profile = get_weather_profile(latitude, longitude)

        return jsonify({
            "success": True,
            "latitude": latitude,
            "longitude": longitude,
            "weather_profile": profile
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/check-env")
def check_env():
    username = os.getenv("ISDA_USERNAME")
    return jsonify({
        "isda_username_loaded": username is not None,
        "username_preview": username[:3] + "***" if username else None
    })

@app.route("/api/test-isda-login")
def test_isda_login():
    try:
        token = get_isda_token()
        return jsonify({
            "login_success": True,
            "token_preview": token[:10] + "..." if token else None
        })
    except Exception as e:
        return jsonify({
            "login_success": False,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)