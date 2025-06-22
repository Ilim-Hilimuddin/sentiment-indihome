import pandas as pd

# Baca file CSV yang berisi tweet
df = pd.read_csv("indihome_tweets.csv")

# Tampilkan 5 baris pertama
print(df.head())
