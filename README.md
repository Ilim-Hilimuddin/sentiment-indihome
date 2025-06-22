# Analisis Sentimen Pelanggan IndiHome dari Twitter

Proyek ini bertujuan untuk menganalisis opini pelanggan IndiHome berdasarkan data tweet, kemudian memvisualisasikannya menggunakan dashboard Grafana.

## 🔍 Tahapan Proyek

1. **Pengumpulan Data:** Menggunakan Twitter API v2 (tweepy)
2. **Preprocessing Teks:** Cleaning, normalisasi, stopword removal
3. **Analisis Sentimen:** Lexicon-based dengan daftar kata positif, negatif, dan negasi
4. **Penyimpanan Data:** PostgreSQL
5. **Visualisasi:** Dashboard Grafana

## 🗂 Struktur Folder

- `data/`: Berisi dataset hasil scraping dan preprocessing
- `scripts/`: Semua script Python dari scraping hingga visualisasi
- `dashboard/`: Cuplikan hasil visualisasi Grafana
- `poster/`: Poster proyek dalam format PDF
- `README.md`: Deskripsi proyek
- `requirements.txt`: Dependensi Python

## 🖼 Contoh Hasil

![grafana](dashboard/dashboard.png)

## 📦 Requirements

```bash
pip install -r requirements.txt
```
