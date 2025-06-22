import pandas as pd
import re
from collections import Counter
import psycopg2

# -------------------------------
# Konfigurasi Database
# -------------------------------
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "sentiment_analysis"
DB_USER = "postgres"
DB_PASS = "admin" 

# -------------------------------
# Load hasil_sentimen.csv
# -------------------------------
print("📥 Memuat file hasil_sentimen.csv...")
df = pd.read_csv("hasil_sentimen.csv")

# -------------------------------
# Daftar Kata
# -------------------------------
negative_words = ["lemot", "error", "lambat", "ganggu", "benerin", "kesel",
                  "buruk", "parah", "mahal", "gajelas", "rugi", "los", "diskonek",
                  "lelet", "mati", "jelek", "jahat", "kendala", "susah", "ribet"]

positive_words = ["lancar", "bagus", "puas", "andal", "senang", "murah",
                  "mantap", "cepat", "baik", "oke", "sukses", "hebat",
                  "canggih", "inovatif"]

# -------------------------------
# Fungsi Hitung Frekuensi Kata
# -------------------------------
def calculate_word_frequencies(df, word_list, column_name="text_clean"):
    word_counts = Counter()
    for text in df[column_name]:
        text = str(text).lower()
        for word in word_list:
            if re.search(rf"\b{re.escape(word)}\b", text):
                word_counts[word] += 1
    return pd.DataFrame(word_counts.items(), columns=["kata", "frekuensi"])

# Hitung frekuensi
df_pos = calculate_word_frequencies(df[df["label_sentimen"] == "positif"], positive_words)
df_neg = calculate_word_frequencies(df[df["label_sentimen"] == "negatif"], negative_words)

# -------------------------------
# Simpan ke PostgreSQL
# -------------------------------
try:
    print("🔗 Menghubungkan ke database PostgreSQL...")
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()

    # ---------------------------
    # Tabel kata_positif
    # ---------------------------
    print("📦 Membuat tabel kata_positif...")
    cur.execute("DROP TABLE IF EXISTS kata_positif;")
    cur.execute("""
        CREATE TABLE kata_positif (
            kata TEXT,
            frekuensi INTEGER
        );
    """)
    for _, row in df_pos.iterrows():
        cur.execute("INSERT INTO kata_positif (kata, frekuensi) VALUES (%s, %s);", tuple(row))
    print("✅ Data kata_positif berhasil disimpan.")

    # ---------------------------
    # Tabel kata_negatif
    # ---------------------------
    print("📦 Membuat tabel kata_negatif...")
    cur.execute("DROP TABLE IF EXISTS kata_negatif;")
    cur.execute("""
        CREATE TABLE kata_negatif (
            kata TEXT,
            frekuensi INTEGER
        );
    """)
    for _, row in df_neg.iterrows():
        cur.execute("INSERT INTO kata_negatif (kata, frekuensi) VALUES (%s, %s);", tuple(row))
    print("✅ Data kata_negatif berhasil disimpan.")

    # Simpan ke DB
    conn.commit()
    cur.close()
    conn.close()
    print("🎉 Semua data berhasil dimasukkan ke PostgreSQL.")

except Exception as e:
    print("❌ Terjadi error saat menyimpan ke database:", e)
