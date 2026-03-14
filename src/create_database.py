import pandas as pd
import sqlite3

# Load dataset
df = pd.read_csv("data/creditcard.csv")

# Create database
conn = sqlite3.connect("database/fraud_detection.db")

# Store data into SQL table
df.to_sql("transactions", conn, if_exists="replace", index=False)

print("Database created successfully!")

conn.close()