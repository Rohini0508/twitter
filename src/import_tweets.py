import os
import configparser
import tweepy
import pandas as pd
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
 
# Download sentiment lexicon for VADER
nltk.download("vader_lexicon")
 
# Load config using relative path from src/
config = configparser.ConfigParser(interpolation=None)
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.ini")
config.read(config_path)
 
# Debug: Show available sections
print("CONFIG SECTIONS FOUND:", config.sections())
 
# Twitter API token
bearer_token = config["TwitterAPI"]["bearer_token"]
client = tweepy.Client(bearer_token=bearer_token)
 
# Sentiment analyzer
analyzer = SentimentIntensityAnalyzer()
 
# Clean tweet text
def clean_text(text):
    text = re.sub(r"http\S+|@\w+|#|[^\w\s]", "", text)
    return text.lower().strip()
 
# Fetch tweets
def fetch_tweets(query="#Nike lang:en -is:retweet", max_results=50):
    response = client.search_recent_tweets(
        query=query,
        max_results=max_results,
        tweet_fields=["id", "created_at", "author_id", "text"]
    )
 
    tweet_data = []
    if response.data:
        for tweet in response.data:
            cleaned = clean_text(tweet.text)
            score = analyzer.polarity_scores(cleaned)['compound']
            label = "positive" if score > 0 else ("negative" if score < 0 else "neutral")
            tweet_data.append([
                tweet.id,
                tweet.text,
                tweet.created_at,
                tweet.author_id,
                score,
                label
            ])
 
    return pd.DataFrame(tweet_data, columns=["tweet_id", "tweet_text", "created_at", "author_id", "sentiment_score", "sentiment_label"])