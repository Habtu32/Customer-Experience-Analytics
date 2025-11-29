import pandas as pd
from transformers import pipeline

## Import cleaned file
df_cleaned = pd.read_csv('../../data/processed/cleaned_reviews_final.csv')

# Initialize sentiment analyzer
sentiment_analyzer = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

def analyze_sentiment(review_text):
    # Ensure review_text is a string, as some entries might be non-string
    if not isinstance(review_text, str):
        return {'label': 'UNKNOWN', 'score': 0.0} # Handle non-string entries
    # The pipeline returns a list of dictionaries, we want the first (and only) element
    result = sentiment_analyzer(review_text)[0]

    # Classify as 'NEUTRAL' if the score is below 0.6
    if result['score'] < 0.6:
        result['label'] = 'NEUTRAL'

    return result

# Apply the function to the 'review' column and store the results in a new column
df_cleaned['sentiment_results'] = df_cleaned['review'].apply(analyze_sentiment)

# Extract 'label' and 'score' into separate columns
df_cleaned['sentiment_label'] = df_cleaned['sentiment_results'].apply(lambda x: x['label'])
df_cleaned['sentiment_score'] = df_cleaned['sentiment_results'].apply(lambda x: x['score'])

# Remove the intermediate 'sentiment_results' column
df_cleaned = df_cleaned.drop(columns=['sentiment_results'])

# Calculate sentiment distribution per bank, now including neutral
sentiment_by_bank = df_cleaned.groupby('bank').agg(
    total_reviews=('review', 'count'),
    positive_count=('sentiment_label', lambda x: (x == 'POSITIVE').sum()),
    negative_count=('sentiment_label', lambda x: (x == 'NEGATIVE').sum()),
    neutral_count=('sentiment_label', lambda x: (x == 'NEUTRAL').sum()),
    average_sentiment_score=('sentiment_score', 'mean')
)

sentiment_by_bank['positive_percentage'] = (sentiment_by_bank['positive_count'] / sentiment_by_bank['total_reviews']) * 100
sentiment_by_bank['negative_percentage'] = (sentiment_by_bank['negative_count'] / sentiment_by_bank['total_reviews']) * 100
sentiment_by_bank['neutral_percentage'] = (sentiment_by_bank['neutral_count'] / sentiment_by_bank['total_reviews']) * 100

# Display the final sentiment by bank results
print(sentiment_by_bank)

# Save the DataFrame with sentiment results to a CSV file
df_cleaned.to_csv('../../data/processed/reviews_with_sentiment.csv', index=False)
print("DataFrame with sentiment results saved to 'reviews_with_sentiment.csv'")

# Display the head of the final df_cleaned DataFrame
print(df_cleaned.head())