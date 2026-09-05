import os
import joblib
import pandas as pd

MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "ml", "agrisense_crop_model.pkl"
)

# Load the model once, when this module is first imported
model = joblib.load(MODEL_PATH)


def predict_top_crops(farm_profile, top_n=3):
    """
    Takes a farm_profile dictionary (from farm_profile_service) and returns
    the top N recommended crops with their confidence scores.
    """
    features = pd.DataFrame([{
        "temperature": farm_profile["weather"]["temperature"],
        "humidity": farm_profile["weather"]["humidity"],
        "ph": farm_profile["soil"]["ph"],
        "rainfall": farm_profile["weather"]["rainfall_last_30_days"]
    }])

    probabilities = model.predict_proba(features)[0]
    classes = model.classes_

    crop_scores = sorted(
        zip(classes, probabilities),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        {"crop": crop, "score": round(float(score), 3)}
        for crop, score in crop_scores[:top_n]
    ]