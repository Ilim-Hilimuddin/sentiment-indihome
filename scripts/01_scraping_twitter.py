import tweepy
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables dari file .env
load_dotenv()

# Ambil API Key, API Secret, dan Bearer Token dari environment variables
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")

# Autentikasi ke Twitter API
client = tweepy.Client(bearer_token=bearer_token)

# Mencari tweet tentang Indihome (dalam 7 hari terakhir)
query = "Indihome -is:retweet lang:id"  # Hanya tweet dalam Bahasa Indonesia
tweets = client.search_recent_tweets(query=query, max_results=80)

# Simpan tweet ke dalam list
tweet_list = [{"id": tweet.id, "text": tweet.text} for tweet in tweets.data]

# Buat DataFrame dengan Pandas
df = pd.DataFrame(tweet_list)

# Simpan ke file CSV
df.to_csv("tweets_4.csv", index=False)

print("✅ Data berhasil disimpan ke tweets.csv")