# CropXcel

**Smarter Decisions. Stronger Harvests.**

CropXcel is an AI-powered farm planning and market-linkage platform built for Uganda. It helps farmers identify their farm on a map, automatically retrieve soil and weather data for that location, get AI-generated crop recommendations, and receive a simple, actionable farm plan — from planting through to expected harvest.

> Built as a hackathon MVP. This README documents what's implemented so far, milestone by milestone.

---

## Core Idea

```
FARM LOCATION
    ↓
SOIL + WEATHER DATA
    ↓
CROP RECOMMENDATION
    ↓
FARM PLAN
    ↓
EXPECTED HARVEST
    ↓
MARKETPLACE (planned)
```

Product philosophy: **PREDICT → PLAN → PRODUCE → CONNECT**

---

## Features Implemented So Far

 **User authentication** — registration and login with hashed passwords, session-based auth, and protected pages
**Interactive map** — Leaflet.js map centered on Uganda with location search (restricted to Uganda via Nominatim)
**Automatic farm boundary** — searching a location automatically draws a representative farm boundary and calculates its centroid
**Real soil data** — pH, Total Nitrogen, Extractable Phosphorus, and Extractable Potassium fetched live from the [iSDAsoil API](https://api.isda-africa.com/isdasoil/v2/docs)
**Real weather data** — current temperature and humidity, plus a 30-day accumulated rainfall figure, from the [Open-Meteo API](https://open-meteo.com/en/docs)
**AI crop recommendation** — a `RandomForestClassifier` trained on `temperature`, `humidity`, `ph`, and `rainfall`, returning the top 3 suitable crops with confidence scores
**Farm plan generation** — rule-based planting guidance (based on recent rainfall) and an indicative expected harvest date range (based on typical crop maturity periods)
**Session-protected map page** with logout functionality

### Planned (not yet implemented)
- Indicative yield estimate
- SQLite-backed marketplace for upcoming harvest listings
- Buyer browsing/filtering of listings

---

## Key Engineering Decisions

**Why doesn't the ML model use Nitrogen, Phosphorus, and Potassium?**
The training dataset's N/P/K values have no documented units, while iSDAsoil returns real values in specific units (e.g. g/kg, ppm). Feeding incompatible scales into the model would produce confident-looking but wrong predictions. Instead, N/P/K are fetched from iSDAsoil and **displayed** to the farmer as part of the soil profile, but are not fed into the prediction model. Only `temperature`, `humidity`, `ph`, and `rainfall` — which are safely comparable in scale and units — are used for prediction.

**Why "rainfall over the last 30 days" instead of live or annual rainfall?**
Live/instantaneous rainfall (e.g. "0.0mm right now") would misrepresent a location's real climate. Annual rainfall totals for Uganda (1,200–1,900mm) are far larger than the training dataset's rainfall range (roughly 20–300mm). A 30-day accumulated total lines up much better in scale with the training data, so it's used as the most defensible, non-fabricated approximation.

**Why rule-based farm plans instead of another ML model?**
Per the project's original scope, planting/harvest guidance uses simple, transparent logic based on recent rainfall and documented crop maturity periods — not another trained model. This keeps the reasoning explainable to a farmer and avoids inventing unverified Ugandan crop calendars.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript, Leaflet.js, OpenStreetMap, Nominatim |
| Backend | Python, Flask, Flask-CORS |
| Machine Learning | scikit-learn (RandomForestClassifier), pandas, joblib |
| Soil Data | iSDAsoil API |
| Weather Data | Open-Meteo API (forecast + historical archive) |
| Database | SQLite |
| Auth | Flask sessions, Werkzeug password hashing |

---

## Project Structure

```
CropXcel/
│
├── backend/
│   ├── app.py                     # Flask app & all API routes
│   ├── .env                       # iSDAsoil credentials (not committed)
│   ├── .venv/                     # Python virtual environment (not committed)
│   ├── requirements.txt
│   │
│   ├── services/
│   │   ├── soil_service.py        # iSDAsoil auth + soil profile fetching
│   │   ├── weather_service.py     # Open-Meteo current + historical rainfall
│   │   ├── farm_profile_service.py# Combines soil + weather into one profile
│   │   ├── model_service.py       # Loads ML model, returns top-3 crop predictions
│   │   ├── farm_plan_service.py   # Rule-based planting guidance + harvest estimate
│   │   └── auth_service.py        # User registration & login (SQLite + password hashing)
│   │
│   ├── models/
│   │   └── agrisense_crop_model.pkl
│   │
│   └── database/
│       ├── db_setup.py           
│       └── agrisense.db
│
├── ML/
│   ├── Crop_recommendation.csv
│   ├── inspect_data.py
│   ├── train_model.py
│   ├── test_prediction.py
│   └── agrisense_crop_model.pkl
│
└── frontend/
    ├── index.html                 
    ├── login.html
    ├── register.html
    ├── map.html                    
    ├── css/
    │   ├── styles.css             
    │   └── map.css                
    └── js/
        ├── auth.js                
        └── map.js                  
```

---

## Setup & Installation

### Prerequisites
- Python 3.x
- A modern web browser
- VS Code (recommended) with the **Live Server** extension
- An [iSDAsoil API account](https://www.isda-africa.com/api/registration/) (username + password)

### 1. Clone the repository
```bash
git clone https://github.com/mirembejanegift/CropXcel.git
cd CropXcel
```

### 2. Backend setup
```bash
cd backend
python -m venv .venv

# Activate the virtual environment
# Git Bash:
source .venv/Scripts/activate
# PowerShell:
.venv\Scripts\activate

pip install -r requirements.txt
```

If `requirements.txt` doesn't exist yet, install manually:
```bash
pip install flask flask-cors python-dotenv requests pandas scikit-learn joblib
```

### 3. Configure environment variables
Create a `.env` file inside `backend/`:
```
ISDA_USERNAME=your_isda_username
ISDA_PASSWORD=your_isda_password
```

### 4. Set up the database
```bash
python database/db_setup.py
```

### 5. Train the ML model (if not already trained)
```bash
cd ../ML
python train_model.py
```
This saves `agrisense_crop_model.pkl` — copy it into `backend/models/`.

### 6. Run the backend
```bash
cd ../backend
python app.py
```
The API will be available at `http://127.0.0.1:5000`.

### 7. Run the frontend
Open `frontend/login.html` with VS Code's Live Server extension (or serve the `frontend/` folder with any static file server). By default this runs at `http://127.0.0.1:5500`.

> **CORS note:** the backend's CORS configuration allows requests from `http://127.0.0.1:5500` and `http://localhost:5500`. If you serve the frontend on a different port, update the `origins` list in `app.py` accordingly.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/register` | Register a new user |
| POST | `/api/login` | Log in and start a session |
| POST | `/api/logout` | Clear the current session |
| GET | `/api/current-user` | Get the logged-in user's info |
| POST | `/api/analyse-farm` | Given `{latitude, longitude}`, returns soil + weather profile and top 3 crop recommendations |
| POST | `/api/generate-plan` | Given `{crop, farm_profile}`, returns planting guidance and an expected harvest window |

### Example: Analyse a farm
```bash
curl -X POST http://127.0.0.1:5000/api/analyse-farm \
  -H "Content-Type: application/json" \
  -d '{"latitude": 0.3476, "longitude": 32.5825}'
```

---

##  Machine Learning Model

- **Algorithm:** Random Forest Classifier (scikit-learn)
- **Features used:** `temperature`, `humidity`, `ph`, `rainfall`
- **Target:** `label` (crop name)
- **Accuracy:** 96.6% on held-out test data
- **Output:** Top 3 crop predictions with confidence scores, using `predict_proba()`

Feature order at prediction time **must** match training order exactly: `temperature, humidity, ph, rainfall`.

---

## Coverage Notes

- **iSDAsoil** only covers the African continent — coordinates outside Africa will return an error.
- **Location search** is restricted to Uganda (`countrycodes=ug` in the Nominatim query).
- **Rainfall figure** reflects the last 30 days, not a live or annual reading — this is a deliberate scale-compatibility choice (see Key Engineering Decisions above).


##  Acknowledgements

[iSDAsoil](https://www.isda-africa.com/) for mapped soil property estimates across Africa
[Open-Meteo](https://open-meteo.com/) for free, no-key weather and historical climate data
[OpenStreetMap](https://www.openstreetmap.org/) contributors and [Nominatim](https://nominatim.org/) for geocoding
[Leaflet.js](https://leafletjs.com/) for the interactive mapping library
Crop recommendation training data originally from the public Kaggle "Crop Recommendation Dataset"
