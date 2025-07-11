import json
from textblob import TextBlob
import os

def analyze_sentiment():
    input_file = "data/filtered_tweets.json"
    output_file = "data/sentiment_tweets.json"

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Missing file: {input_file}")

    with open(input_file, "r", encoding="utf-8") as f:
        tweets = json.load(f)

    for tweet in tweets:
        text = tweet.get("cleaned_text", "")
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        tweet["sentiment"] = sentiment

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(tweets, f, indent=4, ensure_ascii=False)

    print(" Sentiment analysis completed and saved to sentiment_tweets.json")
