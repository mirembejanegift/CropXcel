from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
import os
from services.soil_service import get_isda_token
from services.farm_profile_service import get_farm_profile
from services.model_service import predict_top_crops
from flask import request


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

app = Flask(__name__)
CORS(app)


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


# @app.route("/api/test-weather-raw")
# def test_weather_raw():
#     try:
#         latitude = 0.3476
#         longitude = 32.5825

#         data = get_current_weather_raw(latitude, longitude)

#         return jsonify({
#             "success": True,
#             "raw_data": data
#         })
#     except Exception as e:
#         return jsonify({
#             "success": False,
#             "error": str(e)
#         }), 500

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