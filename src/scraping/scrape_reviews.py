# -------------------------------------------------------------
# scrape_reviews.py
# -------------------------------------------------------------
# Purpose:
#   - Scrape Google Play Store reviews for Ethiopian bank apps
#   - Save raw reviews as CSV files (one per bank)
#
# Libraries used:
#   - google-play-scraper : For scraping reviews
#   - pandas : For saving data in CSV format
#
# How to run:
#   python scrape_reviews.py
# -------------------------------------------------------------

from google_play_scraper import Sort, reviews
import pandas as pd


def fetch_reviews(app_id, bank_name, n_reviews=500):
    """
    Fetch reviews for a single bank app.

    app_id: Google Play identifier of the app
    bank_name: Name of the bank (string)
    n_reviews: Number of reviews to scrape (default = 500)
    """

    all_reviews = []

    # Google Play Scraper only fetches 100 at a time
    count = 0
    while count < n_reviews:
        fetched, _ = reviews(
            app_id,
            lang='en',
            country='et',
            sort=Sort.NEWEST,
            count=100
        )

        if not fetched:
            fetched, _ = reviews(
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=100
        )  

        all_reviews.extend(fetched)
        count += 100

    # Convert raw list → DataFrame
    df = pd.DataFrame(all_reviews)
    print(f"Columns returned for {bank_name}: {df.columns}")


    # Keep only important columns
    df = df[['content', 'score', 'at']]
    df.rename(columns={
        'content': 'review',
        'score': 'rating',
        'at': 'date'
    }, inplace=True)

    # Add bank and source columns
    df['bank'] = bank_name
    df['source'] = 'Google Play'

    return df


def main():
    print("📌 Starting Google Play review scraping...")

    # Ethiopian bank app IDs
    apps = {
        "CBE": "com.combanketh.mobilebanking",
        "BOA": "com.boa.boaMobileBanking",
        "Dashen": "com.dashen.dashensuperapp",
    }

    final_df_list = []

    for bank, app_id in apps.items():
        print(f"➡ Scraping {bank} reviews...")
        df = fetch_reviews(app_id, bank)
        final_df_list.append(df)

    # Combine all banks
    full_df = pd.concat(final_df_list, ignore_index=True)

    # Save raw combined data
    full_df.to_csv("data/raw/raw_reviews.csv", index=False)

    print("🎉 Scraping completed!")
    print("📁 Saved file: data/raw/raw_reviews.csv")


if __name__ == "__main__":
    main()
