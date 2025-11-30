import pandas as pd
import spacy
import gensim.corpora as gensim_corpora
from gensim.models.ldamulticore import LdaMulticore
import re
import string

# --- 1. Load Data ---
# Assuming 'cleaned_reviews_final.csv' is the initial cleaned data source
df = pd.read_csv('/content/cleaned_reviews_final.csv')
print("DataFrame 'df' loaded successfully.")

# --- 2. Load spaCy Model and Define Preprocessing Functions ---
try:
    nlp = spacy.load('en_core_web_sm')
    print("spaCy 'en_core_web_sm' model loaded successfully.")
except OSError:
    print("Downloading spaCy 'en_core_web_sm' model...")
    !python -m spacy download en_core_web_sm
    nlp = spacy.load('en_core_web_sm')
    print("spaCy 'en_core_web_sm' model downloaded and loaded successfully.")

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(f'[{re.escape(string.punctuation)}]', '', text)
    text = re.sub(r'\d+', '', text) # Remove numbers
    text = text.strip() # Remove leading/trailing whitespace
    text = re.sub(r'\s+', ' ', text) # Replace multiple spaces with a single space
    return text

def preprocess_spacy(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc
              if token.is_alpha
              and not token.is_stop]
    return " ".join(tokens)

print("Text cleaning and spaCy preprocessing functions defined.")

# --- 3. Apply Preprocessing ---
df['cleaned_review'] = df['review'].apply(clean_text)
df['lemmatized'] = df['cleaned_review'].apply(preprocess_spacy)
print("Reviews cleaned and lemmatized.")

# --- 4. Prepare Text Data for Topic Modeling ---
df['processed_reviews'] = df['lemmatized'].apply(lambda x: x.split())

# Create a Gensim dictionary from the processed reviews
dictionary = gensim_corpora.Dictionary(df['processed_reviews'])

# Create a Bag-of-Words (BoW) corpus
corpus = [dictionary.doc2bow(review) for review in df['processed_reviews']]
print("Gensim dictionary and Bag-of-Words corpus created.")

# --- 5. Train LDA Topic Model ---
num_topics = 5
passes = 10
random_state = 42

lda_model = LdaMulticore(
    corpus=corpus,
    id2word=dictionary,
    num_topics=num_topics,
    passes=passes,
    random_state=random_state
)
print(f"LDA model trained with {num_topics} topics.")

print("Topics identified by LDA model:")
for idx, topic in lda_model.print_topics():
    print(f"Topic {idx}: {topic}")

# --- 6. Assign Dominant Topics and Create Themes ---
def get_dominant_topic(lda_model, corpus_item):
    topics = lda_model.get_document_topics(corpus_item)
    if topics:
        dominant_topic = max(topics, key=lambda x: x[1])[0]
        return dominant_topic
    return -1 # Default for no topics

dominant_topics = [get_dominant_topic(lda_model, doc) for doc in corpus]
df['dominant_topic'] = dominant_topics

topic_themes = {
    0: 'General Banking Operations',
    1: 'Positive App Features/Experience',
    2: 'App Functionality/Issues',
    3: 'User Experience and Efficiency',
    4: 'App Quality and Services'
}
df['theme'] = df['dominant_topic'].map(topic_themes)
print("Dominant topics assigned and themes created for each review.")

# --- 7. Analyze Theme Distribution per Bank ---
themes_per_bank = df.groupby('bank')['theme'].value_counts(normalize=True).mul(100).unstack(fill_value=0)

print("\nDistribution of Themes per Bank (%):")
display(themes_per_bank)

print("\nHead of DataFrame with new thematic analysis columns:")
display(df[['review', 'cleaned_review', 'lemmatized', 'dominant_topic', 'theme']].head())