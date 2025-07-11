import json
import mysql.connector
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def load_to_mysql():
    with open("data/sentiment_tweets.json", "r", encoding="utf-8") as f:
        tweets = json.load(f)

    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tweets (
            id VARCHAR(255) PRIMARY KEY,
            text TEXT,
            cleaned_text TEXT,
            created_at DATETIME,
            sentiment VARCHAR(20)
        )
    """)

    for tweet in tweets:
        cursor.execute("""
            INSERT IGNORE INTO tweets (id, text, cleaned_text, created_at, sentiment)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            tweet["id"],
            tweet["text"],
            tweet["cleaned_text"],
            tweet["created_at"],
            tweet["sentiment"]
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Tweets loaded into MySQL")

def load_to_sql_server():
    with open("data/sentiment_tweets.json", "r", encoding="utf-8") as f:
        tweets = json.load(f)

    conn_str = f"""
        DRIVER={{{os.getenv('MSSQL_DRIVER')}}};
        SERVER={os.getenv('MSSQL_SERVER')};
        DATABASE={os.getenv('MSSQL_DATABASE')};
        UID={os.getenv('MSSQL_UID')};
        PWD={os.getenv('MSSQL_PWD')};
        TrustServerCertificate=yes;
    """
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='tweets' AND xtype='U')
        CREATE TABLE tweets (
            id NVARCHAR(255) PRIMARY KEY,
            text NVARCHAR(MAX),
            cleaned_text NVARCHAR(MAX),
            created_at DATETIME,
            sentiment NVARCHAR(20)
        )
    """)

    for tweet in tweets:
        cursor.execute("""
            IF NOT EXISTS (SELECT 1 FROM tweets WHERE id = ?)
            INSERT INTO tweets (id, text, cleaned_text, created_at, sentiment)
            VALUES (?, ?, ?, ?, ?)
        """, (
            tweet["id"],
            tweet["id"],
            tweet["text"],
            tweet["cleaned_text"],
            tweet["created_at"],
            tweet["sentiment"]
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Tweets loaded into SQL Server (SSMS)")

def load_to_all_databases():
    load_to_mysql()
    load_to_sql_server()
