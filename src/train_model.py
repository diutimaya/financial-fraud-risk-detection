import pandas as pd
import sqlite3
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# Connect to database
conn = sqlite3.connect("database/fraud_detection.db")

# Load data
df = pd.read_sql("SELECT * FROM transactions", conn)

conn.close()

# Split features and label
X = df.drop("Class", axis=1)
y = df["Class"]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train model
model = LogisticRegression(max_iter=2000)

model.fit(X_train, y_train)

# Save model
joblib.dump(model, "models/fraud_model.pkl")

print("Model trained and saved successfully!")