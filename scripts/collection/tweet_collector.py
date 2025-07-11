import json
import os
import time
import tweepy
import logging
from datetime import datetime
from config.auth_config import get_twitter_client

def collect_tweets(query, start_time, end_time, language="en", max_results=100):
    client = get_twitter_client()
    tweets = []
    next_token = None
    total_collected = 0

    logging.info("Starting tweet collection...")

    while True:
        try:
            response = client.search_recent_tweets(
                query=query,
                start_time=start_time,
                end_time=end_time,
                max_results=max_results,
                tweet_fields=["id", "text", "created_at", "lang"],
                next_token=next_token
            )

            if response.data:
                tweets.extend(response.data)
                total_collected += len(response.data)
                logging.info(f"Collected {len(response.data)} tweets (Total: {total_collected})")
            else:
                logging.info("No more tweets found.")
                break

            next_token = response.meta.get("next_token")
            if not next_token:
                break

            # Optional light delay (can be removed)
            time.sleep(1)

        except tweepy.TooManyRequests as e:
            reset_timestamp = int(e.response.headers.get("x-rate-limit-reset", time.time() + 900))
            wait_time = max(reset_timestamp - int(time.time()), 0)
            reset_time_str = datetime.fromtimestamp(reset_timestamp).strftime('%H:%M:%S')

            logging.warning(f"🚫 Rate limit hit. Will wait {wait_time} seconds (until {reset_time_str})")
            print(f"🚫 Rate limit hit. Waiting {wait_time} seconds (until {reset_time_str})")

            for remaining in range(wait_time, 0, -1):
                print(f"⏳ Waiting... {remaining} sec", end="\r")
                time.sleep(1)

            print("\n Resuming collection...")
            logging.info(" Rate limit reset. Continuing...")

        except tweepy.TweepyException as e:
            logging.error(f"Tweepy error: {str(e)}")
            break
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            break

    # Save tweets to file
    os.makedirs("data", exist_ok=True)
    with open("data/raw_tweets.json", "w", encoding="utf-8") as f:
        json.dump([tweet.data for tweet in tweets], f, ensure_ascii=False, indent=4)

    logging.info(f" Finished collecting tweets. Total: {total_collected}")
    print(f"\n Collected {total_collected} tweets.")
