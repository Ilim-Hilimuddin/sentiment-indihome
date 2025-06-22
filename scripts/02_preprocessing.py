import pandas as pd
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import spacy
from spacy.lang.id import Indonesian
from spacy.tokens import Token

# Inisialisasi stemmer Sastrawi
stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()

# Load SpaCy model untuk Bahasa Indonesia (karena model resmi belum tersedia, gunakan spacy.blank)
nlp = spacy.blank("id")

# Daftar stopwords bahasa Indonesia dari NLTK
stop_words = set(stopwords.words('indonesian'))

# Keluarkan kata 'belum' dari daftar stopword agar tidak terhapus
stop_words.discard('belum')
stop_words.discard('tidak')
stop_words.discard('ada')

# Kamus normalisasi kata slang ke bentuk baku (contoh sederhana, bisa diperluas)
slang_dict = {
    "gak": "tidak",
    "ga": "tidak",
    "nggak": "tidak",
    "gada": "tidak ada",
    "kalo": "kalau",
    "kpn": "kapan",
    "dgn": "dengan",
    "yg": "yang",
    "aja": "saja",
    "anjir": "astaga",
    "bgt": "banget",
    "dr": "dari",
    "udh": "sudah",
    "tdk": "tidak",
    "jgn": "jangan",
    "krn": "karena",
    "sm": "sama",
    "tp": "tapi",
    "sy": "saya",
    "km": "kamu",
    "sdh": "sudah",
    "blm": "belum",
    "dlm": "dalam",
    "hrs": "harus",
    "pdhl": "padahal",
    "msh": "masih",
    "bkn": "bukan",
    "nih": "ini",
    "kok": "kenapa",
    "loh": "loh",
    "deh": "deh",
    "si": "si",
    "dong": "dong",
    "yah": "ya",
    "lemot": "lambat",
    "lemotnya": "lambat",
    "tdi": "tadi",
    "lag" : "lambat",
}

# Fungsi untuk normalisasi slang
def normalize_slang(text):
    words = text.split()
    normalized_words = [slang_dict.get(word, word) for word in words]
    return " ".join(normalized_words)

# Fungsi untuk menghapus noise media sosial (URL, mention, hashtag, emoticon)
def remove_noise(text):
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)  # Hapus URL
    text = re.sub(r"@\w+", "", text)  # Hapus mention
    text = re.sub(r"#\w+", "", text)  # Hapus hashtag
    text = re.sub(r"[^\w\s]", "", text)  # Hapus tanda baca dan simbol
    text = re.sub(r"\d+", "", text)  # Hapus angka
    return text

# Fungsi lemmatization dengan SpaCy (custom sederhana)
def lemmatize_text(text):
    doc = nlp(text)
    lemmas = []
    for token in doc:
        # Jika token adalah stopword, tetap hapus (sudah dihapus sebelumnya)
        # Karena model SpaCy Indonesia belum lengkap, kita gunakan token.text sebagai fallback
        lemma = token.lemma_ if token.lemma_ != '' else token.text
        lemmas.append(lemma)
    return " ".join(lemmas)

# Fungsi utama preprocessing
def preprocess_text(text):
    if not isinstance(text, str):
        return ""

    # 1. Lowercase
    text = text.lower()

    # 2. Hapus noise media sosial (URL, mention, hashtag, emoticon)
    text = remove_noise(text)

    # 3. Normalisasi slang
    text = normalize_slang(text)

    # 4. Hapus tanda baca dan simbol (jika masih ada)
    text = text.translate(str.maketrans('', '', string.punctuation))

    # 5. Tokenisasi
    tokens = word_tokenize(text)

    # 6. Hapus stopwords dan kata terlalu pendek (<=2 karakter)
    tokens = [token for token in tokens if token not in stop_words and len(token) > 2]

    # 7. Lemmatization
    text_lemma = lemmatize_text(" ".join(tokens))

    # 8. Stemming (opsional)
    text_stem = stemmer.stem(text_lemma)

    # 9. Hapus kata tidak relevan (misal kata terlalu pendek setelah stemming)
    tokens_final = [token for token in text_stem.split() if len(token) > 2]

    # Gabungkan kembali menjadi string
    processed_text = " ".join(tokens_final)

    return processed_text

# Contoh penerapan pada dataset CSV
def main():
    # Anda bisa ganti path file CSV sesuai kebutuhan
    input_csv = "tweets_all.csv"
    output_csv = "data_tweets_preprocessed.csv"

    # Baca data CSV
    df = pd.read_csv(input_csv)

    # 1. Penghapusan duplikasi berdasarkan kolom 'text'
    df = df.drop_duplicates(subset=['text'])

    # 2. Terapkan preprocessing pada kolom 'text'
    df['text_clean'] = df['text'].apply(preprocess_text)

    # Simpan hasil ke CSV
    df.to_csv(output_csv, index=False)

    print(f"Preprocessing selesai. Hasil disimpan di {output_csv}")

if __name__ == "__main__":
    main()
