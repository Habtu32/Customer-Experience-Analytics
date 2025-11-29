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