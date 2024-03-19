
import re
import json
import os

def save_to_json(formatted_tweets, filename):
    """
    Menyimpan tweet yang diformat ke dalam berkas JSON di dalam folder 'data'.

    Args:
        formatted_tweets (list): Daftar kamus tweet yang diformat.
        filename (str): Nama berkas JSON untuk disimpan.
    """
    # Mengonversi nama file ke dalam format yang benar
    filename = re.sub(r'[^\w\s.-]', '_', filename)
    
    # Membuat path ke folder data
    data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
    
    # Membuat path lengkap ke berkas JSON (tidak perlu karena nama file sudah termasuk tanggal)
    file_path = os.path.join(data_folder, filename)
    
    # Membuat folder data jika belum ada
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    
    # Menyimpan formatted_tweets ke dalam berkas JSON
    with open(file_path, 'w') as f:
        json.dump(formatted_tweets, f, indent=4)