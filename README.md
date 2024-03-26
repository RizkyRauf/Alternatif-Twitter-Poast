# Alternatif Twitter Poast

**Alternatif Twitter Poast** adalah alat Python yang dirancang untuk mengotomatisasi proses pengambilan data dari [nitter.poast](https://nitter.poast.org/), sebuah antarmuka Twitter tanpa JavaScript. Alat ini menggunakan Selenium untuk web scraping dan menyediakan cara yang nyaman untuk mengekstrak tweet berdasarkan kriteria pencarian.

## Instalasi

1. Pastikan Anda memiliki Python terinstal di komputer Anda. Anda dapat mengunduh Python dari [sini](https://www.python.org/downloads/).

2. Unduh atau klon proyek ini ke komputer Anda.

3. Instal dependensi dengan menjalankan perintah berikut di terminal atau command prompt:

```
pip install -r requirements.txt
```

## Penggunaan

Pastikan Anda telah mengatur konfigurasi yang diperlukan sebelum menjalankan aplikasi ini. Anda mungkin perlu mengatur beberapa variabel lingkungan atau konfigurasi lainnya.

Untuk menjalankan aplikasi, jalankan main.py dengan menjalankan perintah berikut di terminal atau command prompt:

```
python main.py --key "keyword" --start_date "YYYY-MM-DD" --end_date "YYYY-MM-DD"

or you can use this command

python main.py --key "keyword"
```

Ikuti petunjuk yang muncul di layar untuk menggunakan aplikasi.

## Struktur Proyek

```
├── driver
│   └── chromedriver.exe
├── lib
│   ├── __init__.py
│   ├── utils.py
│   └── twitter_poast.py
└── main.py
```

Penjelasan singkat tentang struktur proyek:

driver: Direktori ini berisi file `chromedriver.exe` yang digunakan oleh Selenium WebDriver.
lib: Direktori ini berisi berkas-berkas Python yang mengimplementasikan logika aplikasi.
  - `scraper.py`: Berisi kelas untuk melakukan scraping data dari situs web tertentu.
  - `utils.py`: Berisi fungsi-fungsi bantu yang digunakan di berbagai bagian aplikasi.
  - `twitter_poast.py`: Berisi kelas yang bertanggung jawab untuk berinteraksi dengan Twitter dan melakukan posting.
main.py: Berkas utama yang menjalankan aplikasi.

## Kontribusi
Kami terbuka untuk kontribusi! Jika Anda ingin berkontribusi pada proyek ini, silakan buat pull request atau buka issue baru untuk memulai diskusi.