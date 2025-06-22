import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import Counter

# Load data
df = pd.read_csv("data_tweets_preprocessed.csv")

# Daftar kata negatif
negative_words = ["lemot", "error", "lambat", "gangguan", "benerin", "kesel", 
                  "buruk", "parah", "mahal", "gajelas", "rugi", "los", "diskonek", 
                  "lelet", "mati","jelek","jahat","kendala","susah","ribet"]

# Daftar kata positif
positive_words = ["lancar", "bagus", "puas", "andal", "senang", "murah", 
                  "mantap", "cepat", "baik", "oke", "sukses", "hebat", 
                  "canggih", "inovatif"]

# Daftar kata negasi
negation_words = ["tidak", "gak", "ga", "nggak", "bukan", "tak", "tdk"]

# Fungsi untuk analisis sentimen dengan mempertimbangkan konteks negasi
def analyze_sentiment_with_negation(text):
    text = str(text).lower()
    words = re.findall(r'\w+', text)
    
    score = 0
    i = 0
    while i < len(words):
        word = words[i]
        prev_word = words[i - 1] if i > 0 else ""

        if word in positive_words:
            if prev_word in negation_words:
                score -= 1  # Positif tapi dibalik oleh negasi
            else:
                score += 1
        elif word in negative_words:
            if prev_word in negation_words:
                score += 1  # Negatif tapi dibalik oleh negasi
            else:
                score -= 1
        i += 1

    if score > 0:
        return "positif", score
    elif score < 0:
        return "negatif", score
    else:
        return "netral", score

# Terapkan fungsi analisis ke kolom 'text_clean'
df[["label_sentimen", "skor_sentimen"]] = df["text_clean"].apply(lambda x: pd.Series(analyze_sentiment_with_negation(x)))

# Simpan hasil ke CSV
df.to_csv("hasil_sentimen.csv", index=False)

# Fungsi menghitung frekuensi kata (tanpa stemming)
def calculate_word_frequencies(df, word_list, column_name="text"):
    word_counts = Counter()
    for text in df[column_name]:
        text = str(text).lower()
        for word in word_list:
            if re.search(rf"\b{re.escape(word)}\b", text):
                word_counts[word] += 1
    return pd.DataFrame(word_counts.items(), columns=["Kata", "Frekuensi"])

# Hitung distribusi sentimen
sentiment_distribution = df["label_sentimen"].value_counts()

# Hitung frekuensi kata negatif dan positif
df_negative_word_counts = calculate_word_frequencies(df, negative_words)
df_positive_word_counts = calculate_word_frequencies(df, positive_words)

# --- Visualisasi ---
# Pie chart distribusi sentimen
plt.figure(figsize=(8, 8))
sentiment_distribution.plot.pie(autopct='%1.1f%%', colors=["lightgreen", "lightcoral", "lightblue"], startangle=90)
plt.title("Distribusi Sentimen Tweet IndiHome", fontsize=14)
plt.ylabel("")
plt.show()
# Bar chart kata negatif
if not df_negative_word_counts.empty:
    plt.figure(figsize=(10, 5))
    sns.barplot(x="Kata", y="Frekuensi", hue="Kata", data=df_negative_word_counts, palette="Reds_r", legend=False)
    plt.title("Frekuensi Kata Negatif dalam Tweet IndiHome", fontsize=14)
    plt.xlabel("Kata Negatif")
    plt.ylabel("Jumlah Kemunculan")
    plt.xticks(rotation=45)
    plt.show()
else:
    print("Tidak ada kata negatif yang ditemukan.")
# Bar chart kata positif
if not df_positive_word_counts.empty:
    plt.figure(figsize=(10, 5))
    sns.barplot(x="Kata", y="Frekuensi", hue="Kata", data=df_positive_word_counts, palette="Greens_r", legend=False)
    plt.title("Frekuensi Kata Positif dalam Tweet IndiHome", fontsize=14)
    plt.xlabel("Kata Positif")
    plt.ylabel("Jumlah Kemunculan")
    plt.xticks(rotation=45)
    plt.show()
else:
    print("Tidak ada kata positif yang ditemukan.")