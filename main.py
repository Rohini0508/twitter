from src.import_tweets import fetch_tweets
from src.load_to_sql import to_sql
 
df = fetch_tweets()
df.to_csv("tweet_data.csv", index=False)
print("Tweets collected and saved to tweet_data.csv")
 
to_sql()