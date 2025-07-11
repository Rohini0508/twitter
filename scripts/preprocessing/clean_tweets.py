import os
import json
import re

def clean_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r"[^A-Za-z0-9\s]", "", text)
    return text.strip()

def clean_raw_tweets(input_folder="data/raw", output_folder="data/cleaned"):
    os.makedirs(output_folder, exist_ok=True)
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".json"):
            with open(os.path.join(input_folder, file_name), "r") as infile:
                tweets = json.load(infile)

            cleaned = [{"id": t["id"], "text": clean_text(t["text"])} for t in tweets]

            out_file = os.path.join(output_folder, f"cleaned_{file_name}")
            with open(out_file, "w") as outfile:
                json.dump(cleaned, outfile, indent=2)

if __name__ == "__main__":
    clean_raw_tweets()
