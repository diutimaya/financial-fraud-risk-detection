import pandas as pd
import sqlite3

conn = sqlite3.connect("database/fraud_detection.db")
query = "SELECT * FROM transactions"
df = pd.read_sql(query, conn)

print(df.head())

conn.close()