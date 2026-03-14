import joblib
import numpy as np

model = joblib.load("models/fraud_model.pkl")

transaction = np.array([[50000, 1.2, -0.5, 0.8, 0.3, -1.1]])

prediction = model.predict(transaction)

if prediction[0] == 1:
    print("Fraudulent Transaction Detected")
else:
    print("Normal Transaction")