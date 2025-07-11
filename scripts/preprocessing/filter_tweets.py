import json

def filter_cleaned_tweets(keywords):
    with open("data/cleaned_tweets.json", encoding="utf-8") as f:
        tweets = json.load(f)

    filtered = []
    for tweet in tweets:
        if any(kw.lower() in tweet["text"] for kw in keywords):
            filtered.append(tweet)

    with open("data/filtered_tweets.json", "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=4)
