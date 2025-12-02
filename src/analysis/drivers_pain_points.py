import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

"""
Revised insights_recommendations.py
Fixes:
- Handles missing CSV file with a clear error message
- Allows custom CSV path
- Includes basic tests inside __main__ guard
"""

# --------------------------------------------------------
# Load Data
# --------------------------------------------------------
def load_data(csv_path="../../processed_reviews.csv"):
    """Load processed reviews dataset safely."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"CSV file not found at '{csv_path}'. Please check the path or upload the file."
        )
    return pd.read_csv(csv_path)

# --------------------------------------------------------
# Generate Insights
# --------------------------------------------------------

def generate_insights(df):
    """Derive drivers and pain points per bank using themes + sentiment."""

    insights = {}
    banks = df["bank"].unique()

    for bank in banks:
        bank_df = df[df["bank"] == bank]
        pos = bank_df[bank_df["sentiment_label"] == "POSITIVE"]
        neg = bank_df[bank_df["sentiment_label"] == "NEGATIVE"]

        pos_counts = pos["theme"].value_counts().to_dict()
        neg_counts = neg["theme"].value_counts().to_dict()

        drivers = sorted(pos_counts, key=pos_counts.get, reverse=True)[:2]
        pain_points = sorted(neg_counts, key=neg_counts.get, reverse=True)[:2]

        insights[bank] = {
            "drivers": drivers,
            "pain_points": pain_points,
        }

    return insights

# --------------------------------------------------------
# Recommendations
# --------------------------------------------------------

def generate_recommendations(insights):
    """Generate actionable improvements per bank."""

    recs = {}
    base_actions = {
        "App Malfunction & Technical Bugs": "Prioritize crash fixes, improve stability, and increase QA testing coverage.",
        "App Performance (Speed & Quality)": "Optimize loading times, reduce background API calls, improve device compatibility.",
        "User Experience, Features & Security": "Improve UI/UX flows, strengthen security messaging, simplify workflows.",
        "Transaction & Service Reliability Issues": "Improve backend reliability, retry logic, and user-facing error messages.",
        "Highly Positive Feedback & Brand Perception": "Amplify strengths in marketing and user education materials."
    }

    for bank, details in insights.items():
        bank_recs = []
        for issue in details["pain_points"]:
            if issue in base_actions:
                bank_recs.append(base_actions[issue])
        recs[bank] = bank_recs

    return recs

# --------------------------------------------------------
# Visualization
# --------------------------------------------------------

def sentiment_distribution(df, save_path="sentiment_distribution.png"):
    plt.figure(figsize=(8, 5))
    df["sentiment_label"].value_counts().plot(kind="bar")
    plt.title("Sentiment Distribution")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(save_path)


def rating_distribution(df, save_path="rating_distribution.png"):
    plt.figure(figsize=(8, 5))
    df["rating"].value_counts().sort_index().plot(kind="bar")
    plt.title("Rating Distribution")
    plt.xlabel("Rating")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(save_path)


def theme_wordcloud(df, save_path_prefix="wordcloud_"):
    banks = df["bank"].unique()

    for bank in banks:
        bank_df = df[df["bank"] == bank]
        text = " ".join(bank_df["lemmatized"].astype(str).tolist())

        wc = WordCloud(width=800, height=400).generate(text)

        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.title(f"Keyword Cloud - {bank}")
        plt.tight_layout()
        plt.savefig(f"{save_path_prefix}{bank}.png")

# --------------------------------------------------------
# Main Execution
# --------------------------------------------------------

def run_pipeline(csv_path="./processed_reviews.csv"):
    df = load_data(csv_path)
    print("✓ Data Loaded")

    insights = generate_insights(df)
    print("\n=== Insights ===")
    print(insights)

    recs = generate_recommendations(insights)
    print("\n=== Recommendations ===")
    print(recs)

    print("\nGenerating visualizations...")
    sentiment_distribution(df)
    rating_distribution(df)
    theme_wordcloud(df)

    print("✓ All visualizations saved.")
    print("\nPipeline complete.")

# --------------------------------------------------------
# Basic Test Cases
# --------------------------------------------------------

def _run_tests():
    print("Running basic tests...")

    # Test 1: missing file should raise FileNotFoundError
    try:
        load_data("./file_does_not_exist.csv")
    except FileNotFoundError:
        print("✓ FileNotFoundError test passed")

    # Test 2: insights generation structure
    sample = pd.DataFrame({
        "bank": ["CBE", "CBE"],
        "sentiment_label": ["POSITIVE", "NEGATIVE"],
        "theme": ["A", "B"],
    })
    out = generate_insights(sample)
    assert "CBE" in out
    assert "drivers" in out["CBE"]
    assert "pain_points" in out["CBE"]
    print("✓ Insights structure test passed")

    print("All tests passed.")


if __name__ == "__main__":
    # Uncomment to run tests
    # _run_tests()

    # Main pipeline run
    try:
        run_pipeline()
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
