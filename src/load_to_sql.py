import os
import configparser
import pandas as pd
from sqlalchemy import create_engine, text
 
def to_sql():
    # Load config using relative path from project root
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.ini")
    config.read(config_path)
 
    # Optional: Print to verify config is loaded correctly
    print("CONFIG SECTIONS FOUND:", config.sections())
 
    # Read SQL config values
    server = config["Sql"]["server"]
    database = config["Sql"]["database"]
    username = config["Sql"]["username"]
    password = config["Sql"]["password"]
 
    # Set up SQLAlchemy engine for SQL Server
    engine = create_engine(
        f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server",
        fast_executemany=True
    )
 
    # Create table if not already exists
    with engine.begin() as conn:
        conn.execute(text("""
            IF NOT EXISTS (
                SELECT * FROM sysobjects WHERE name='twitter_sentiment' AND xtype='U'
            )
            CREATE TABLE twitter_sentiment (
                tweet_id BIGINT PRIMARY KEY,
                tweet_text NVARCHAR(MAX),
                created_at DATETIME,
                author_id BIGINT,
                sentiment_score FLOAT,
                sentiment_label VARCHAR(10)
            )
        """))
 
    # Load and clean CSV
    df = pd.read_csv("tweet_data.csv")
    df = df.drop_duplicates(subset="tweet_id")
    # Convert datetime and remove timezone info
    df["created_at"] = pd.to_datetime(df["created_at"], errors='coerce').dt.tz_localize(None)
 
    # Load data into SQL Server
    try:
        df.to_sql("twitter_sentiment", engine, if_exists="append", index=False, method="multi")
        print("✅ Data loaded to SQL Server successfully!")
    except Exception as e:
        print(f"❌ Error inserting data: {e}")