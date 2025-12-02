# Customer Experience Analytics - Task 1: Data Collection & Preprocessing

## Project Overview
This project analyzes user reviews from mobile banking apps of three Ethiopian banks (CBE, BOA, Dashen) to identify customer satisfaction drivers and pain points.

## Task 1 Objective
- Scrape user reviews from Google Play Store
- Preprocess and clean the dataset for analysis
- Manage code and dataset using GitHub

## Data Source
- Google Play Store reviews
- Apps:
  - Commercial Bank of Ethiopia (CBE)
  - Bank of Abyssinia (BOA)
  - Dashen Bank

## Preprocessing Steps
1. **Downloaded reviews**: ~1500 reviews in total (500 per bank)  
2. **Handled missing data**: Checked for empty or NaN reviews → none found  
3. **Removed duplicates**: 552 duplicate reviews removed across all banks  
4. **Normalized dates**: Converted all review dates to `YYYY-MM-DD` format  
5. **Handled unexpected characters**: 205 reviews contained Amharic characters or emojis — retained for analysis  
6. **Saved cleaned dataset**: `data/preprocessed/clean_reviews.csv`

## Dataset Summary
- Total reviews after cleaning: 2211  
- Reviews per bank:
  - CBE: 773  
  - BOA: 820  
  - Dashen: 618  
- Columns: `review`, `rating`, `date`, `bank`, `source`

## Usage / Next Steps
- `clean_reviews_final.csv` will be used for **Task-2 Sentiment & Thematic Analysis**
- Ensure you load it in your analysis scripts for NLP processing

## 📊 Task 3 – Database Setup (PostgreSQL)

### 1. Database Schema

The project uses two tables:

### **banks**
Stores metadata for each bank.
| Column | Type | Description |
|--------|------|-------------|
| bank_id | SERIAL PK | Unique ID for each bank |
| bank_name | VARCHAR | Name of the bank |
| app_name | VARCHAR | Name of the mobile app |

### **reviews**
Stores all cleaned and processed review data.
| Column | Type | Description |
|--------|------|-------------|
| review_id | SERIAL PK | Unique review ID |
| bank_id | INT FK | Links to banks table |
| review_text | TEXT | Original review text |
| rating | INT | Star rating |
| review_date | DATE | Review date |
| sentiment_label | VARCHAR | Positive/Negative/Neutral |
| sentiment_score | FLOAT | Model score |
| source | VARCHAR | App store source |
| cleaned_review | TEXT | Cleaned version |
| lemmatized | TEXT | Lemmatized version |
| topic | INT | LDA topic label |
| theme | VARCHAR | Final manual theme |

The full schema is stored in `database/schema.sql`.

---

### 2. Insert Script

A Python script (`database/insert_data.py`) loads cleaned CSV data and inserts it using psycopg2.

### 3. Verification Queries

Examples used to validate data integrity:

```sql
-- Count reviews
SELECT COUNT(*) FROM reviews;

-- Reviews per bank
SELECT bank_id, COUNT(*) 
FROM reviews 
GROUP BY bank_id;

-- Average rating per bank
SELECT bank_id, AVG(rating)
FROM reviews
GROUP BY bank_id;