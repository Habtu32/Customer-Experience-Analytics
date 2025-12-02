import pandas as pd
import psycopg2
from psycopg2 import sql

# 1. Load the CSV
df = pd.read_csv("../../data/processed/postgres_ready_reviews.csv")

# 2. PostgreSQL connection parameter
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "bank_reviews"
DB_USER = "postgres"     # your PostgreSQL username
DB_PASS = "Pass00.."     # your password

# 3. Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()
    print("✅ Connected to PostgreSQL successfully")
except Exception as e:
    print("❌ Connection failed:", e)
    exit()

# 4. Insert data into reviews table
insert_query = """
INSERT INTO reviews
(bank_id, review_text, cleaned_review, rating, review_date, sentiment_label, sentiment_score, source)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

for idx, row in df.iterrows():
    cursor.execute(insert_query, (
        int(row["bank_id"]),
        row["review_text"],
        row["cleaned_review"],
        int(row["rating"]),
        row["review_date"],
        row["sentiment_label"],
        float(row["sentiment_score"]),
        row["source"]
    ))

# 5. Commit changes and close
conn.commit()
cursor.close()
conn.close()
print("✅ Data inserted successfully into PostgreSQL")