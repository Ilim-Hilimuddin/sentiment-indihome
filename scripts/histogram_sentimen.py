import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Pastikan NLTK sudah terinstal dan unduh dataset yang diperlukan
try:
    import nltk
    nltk.download('stopwords')
    nltk.download('punkt')  # Unduh dataset Punkt untuk tokenisasi
except ModuleNotFoundError:
    print("Library NLTK belum terinstal. Silakan instal menggunakan 'pip install nltk'.")
    exit()

# Pastikan Sastrawi sudah terinstal
try:
    from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
except ModuleNotFoundError:
    print("Library Sastrawi belum terinstal. Silakan instal menggunakan 'pip install sastrawi'.")
    exit()

# Load data
df = pd.read_csv("tweets_baru.csv")

# Daftar kata negatif yang ingin dicari
negative_words = ["lemot", "error", "lambat", "gangguan", "benerin", "kesel", "buruk", "parah", "mahal", "gajelas", "rugi", "los", "diskonek", "perbaiki", "lelet","mati"]

# Daftar kata positif yang ingin dicari
positive_words = ["lancar", "bagus", "puas", "andal", "memuaskan"]

# Metode 2: Pra-Pemrosesan Data
def preprocess_text(text):
    # Case Folding: Ubah teks menjadi huruf kecil
    text = str(text).lower()
    
    # Hapus karakter non-alfanumerik (emoji, simbol, dll.)
    text = re.sub(r"[^\w\s-]", "", text)  # Pertahankan tanda hubung (-)
    
    # Tokenisasi: Pisahkan teks menjadi token
    tokens = word_tokenize(text)  # Gunakan dataset Punkt untuk tokenisasi
    
    # Stopword Removal: Hapus kata-kata umum seperti "dan", "yang", dll.
    custom_stopwords = set(stopwords.words("indonesian")) - {"gak", "nggak", "tidak"}
    tokens = [word for word in tokens if word not in custom_stopwords]
    
    # Stemming: Sederhanakan kata menjadi bentuk dasar
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    tokens = [stemmer.stem(word) for word in tokens]
    
    return " ".join(tokens)

# Stemming daftar kata negatif
factory = StemmerFactory()
stemmer = factory.create_stemmer()
negative_words = [stemmer.stem(word) for word in negative_words]

# Terapkan pra-pemrosesan pada kolom teks
df["cleaned_text"] = df["text"].apply(preprocess_text)

# Fungsi untuk menghitung frekuensi kata
def calculate_word_frequencies(df, word_list, column_name="cleaned_text"):
    word_counts = Counter()
    for text in df[column_name]:
        for word in word_list:
            # Gunakan regex untuk mendeteksi frasa multi-kata
            if re.search(rf"\b{re.escape(word)}\b", text):
                word_counts[word] += 1
    return pd.DataFrame(word_counts.items(), columns=["Kata", "Frekuensi"])

# Hitung frekuensi kata negatif
df_negative_word_counts = calculate_word_frequencies(df, negative_words)

# Hitung frekuensi kata positif
df_positive_word_counts = calculate_word_frequencies(df, positive_words)

# Metode 3: Analisis Sentimen
# Misalnya, menggunakan pendekatan lexicon-based sederhana
positive_lexicon = positive_words
negative_lexicon = negative_words

def analyze_sentiment(text):
    positive_score = sum([1 for word in positive_lexicon if re.search(rf"\b{re.escape(word)}\b", text)])
    negative_score = sum([1 for word in negative_lexicon if re.search(rf"\b{re.escape(word)}\b", text)])
    
    if positive_score > negative_score:
        return "positif"
    elif negative_score > positive_score:
        return "negatif"
    else:
        return "netral"

# Tambahkan kolom sentimen ke DataFrame
df["sentimen"] = df["cleaned_text"].apply(analyze_sentiment)

# Hitung distribusi sentimen
sentiment_distribution = df["sentimen"].value_counts()

# Metode 4: Visualisasi Data
# Plot pie chart distribusi sentimen
plt.figure(figsize=(8, 8))
sentiment_distribution.plot.pie(autopct='%1.1f%%', colors=["lightgreen", "lightcoral", "lightblue"], startangle=90)
plt.title("Distribusi Sentimen Tweet IndiHome", fontsize=14)
plt.ylabel("")
plt.show()

# Plot histogram frekuensi kata negatif
if not df_negative_word_counts.empty:
    plt.figure(figsize=(10, 5))
    sns.barplot(x="Kata", y="Frekuensi", data=df_negative_word_counts, palette="Reds_r")
    plt.title("Frekuensi Kata Negatif dalam Tweet IndiHome", fontsize=14)
    plt.xlabel("Kata Negatif")
    plt.ylabel("Jumlah Kemunculan")
    plt.xticks(rotation=45)
    plt.show()
else:
    print("Tidak ada kata negatif yang ditemukan.")

# Plot histogram frekuensi kata positif
if not df_positive_word_counts.empty:
    plt.figure(figsize=(10, 5))
    sns.barplot(x="Kata", y="Frekuensi", data=df_positive_word_counts, palette="Greens_r")
    plt.title("Frekuensi Kata Positif dalam Tweet IndiHome", fontsize=14)
    plt.xlabel("Kata Positif")
    plt.ylabel("Jumlah Kemunculan")
    plt.xticks(rotation=45)
    plt.show()
else:
    print("Tidak ada kata positif yang ditemukan.")

# Plot time series analisis sentimen (jika ada kolom waktu)
if "created_at" in df.columns:
    df["created_at"] = pd.to_datetime(df["created_at"])
    df.set_index("created_at", inplace=True)
    sentiment_trend = df.resample("D")["sentimen"].apply(lambda x: (x == "negatif").sum())
    
    if not sentiment_trend.empty:
        plt.figure(figsize=(10, 5))
        sentiment_trend.plot(kind="line", color="red")
        plt.title("Tren Sentimen Negatif Harian", fontsize=14)
        plt.xlabel("Tanggal")
        plt.ylabel("Jumlah Tweet Negatif")
        plt.show()
    else:
        print("Tidak ada data tren sentimen negatif.")