import joblib
import pandas as pd

# Load the trained model
model = joblib.load("agrisense_crop_model.pkl")

# Example input — replace with any realistic values
# Order MUST be: temperature, humidity, ph, rainfall
sample_input = pd.DataFrame([{
    "temperature": 24.5,
    "humidity": 78.0,
    "ph": 6.3,
    "rainfall": 180.0
}])

# Single prediction
prediction = model.predict(sample_input)
print("Predicted crop:", prediction[0])

# Top 3 predictions using predict_proba
probabilities = model.predict_proba(sample_input)[0]
classes = model.classes_

# Pair crops with their scores and sort descending
crop_scores = sorted(
    zip(classes, probabilities),
    key=lambda x: x[1],
    reverse=True
)

print("\nTop 3 recommendations:")
for crop, score in crop_scores[:3]:
    print(f"  {crop}: {score:.2f}")