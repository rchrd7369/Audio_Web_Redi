import os
import sys
from flask import Flask, render_template, request, send_file, jsonify
from pydub.utils import mediainfo
import pandas as pd

# Tentukan lokasi ffmpeg.exe dalam bundel PyInstaller
if getattr(sys, 'frozen', False):  # Jika aplikasi dibundel dengan PyInstaller
    base_path = sys._MEIPASS
else:  # Jika dijalankan dalam mode pengembangan
    base_path = os.path.abspath(".")

ffmpeg_path = os.path.join(base_path, "ffmpeg.exe")
ffprobe_path = os.path.join(base_path, "ffprobe.exe")

print(f"ffmpeg path: {ffmpeg_path}")
print(f"ffprobe path: {ffprobe_path}")

app = Flask(__name__)

# Fungsi untuk membaca folder dan mendapatkan informasi file
def get_audio_file_info(folder_path):
    file_info = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if os.path.isfile(file_path) and filename.lower().endswith(('mp3', 'wav', 'flac', 'aac', 'ogg')):
            # Mengambil informasi media
            info = mediainfo(file_path)
            duration_sec = float(info['duration'])  # Durasi dalam detik
            size_bytes = os.path.getsize(file_path)  # Ukuran file dalam bytes

            # Mengonversi ukuran file ke MB
            size_mb = size_bytes / (1024 * 1024)

            # Menghitung total menit dan detik menggunakan operasi modulo
            duration_min = int(duration_sec // 60)  # Mendapatkan menit bulat
            remaining_sec = int(duration_sec % 60)  # Menggunakan integer untuk detik

            # Menyimpan informasi file dengan format menit.detik
            file_info.append({
                'Nama File': filename,
                'Ukuran (Byte)': size_bytes,
                'Ukuran (MB)': round(size_mb, 2),
                'Durasi (Detik)': round(duration_sec, 2),
                'Durasi (Menit)': f'{duration_min}.{remaining_sec}',  # Format menit.detik
            })

    return file_info

# Fungsi untuk mengekspor data ke file Excel
def export_to_excel(file_info):
    df = pd.DataFrame(file_info)
    min_size = df['Ukuran (MB)'].min()
    max_size = df['Ukuran (MB)'].max()
    mean_size = df['Ukuran (MB)'].mean()

    min_duration_sec = df['Durasi (Detik)'].min()
    max_duration_sec = df['Durasi (Detik)'].max()
    mean_duration_sec = df['Durasi (Detik)'].mean()

    min_duration_min = int(min_duration_sec // 60)
    min_duration_rem_sec = int(min_duration_sec % 60)

    max_duration_min = int(max_duration_sec // 60)
    max_duration_rem_sec = int(max_duration_sec % 60)

    mean_duration_min = int(mean_duration_sec // 60)
    mean_duration_rem_sec = int(mean_duration_sec % 60)

    summary = pd.DataFrame([{
        'Nama File': '',
        'Ukuran (Byte)': '',
        'Ukuran (MB)': '',
        'Durasi (Detik)': '',
        'Durasi (Menit)': '',
    }])

    summary.loc[0, 'Nama File'] = 'Summary'

    min_row = pd.DataFrame([{
        'Nama File': 'Min',
        'Ukuran (Byte)': '',
        'Ukuran (MB)': f'{min_size:.2f}'.replace('.', ','),
        'Durasi (Detik)': f'{min_duration_sec:.2f}'.replace('.', ','),
        'Durasi (Menit)': f'{min_duration_min}.{min_duration_rem_sec}'
    }])

    max_row = pd.DataFrame([{
        'Nama File': 'Max',
        'Ukuran (Byte)': '',
        'Ukuran (MB)': f'{max_size:.2f}'.replace('.', ','),
        'Durasi (Detik)': f'{max_duration_sec:.2f}'.replace('.', ','),
        'Durasi (Menit)': f'{max_duration_min}.{max_duration_rem_sec}'
    }])

    mean_row = pd.DataFrame([{
        'Nama File': 'Mean',
        'Ukuran (Byte)': '',
        'Ukuran (MB)': f'{mean_size:.2f}'.replace('.', ','),
        'Durasi (Detik)': f'{mean_duration_sec:.2f}'.replace('.', ','),
        'Durasi (Menit)': f'{mean_duration_min}.{mean_duration_rem_sec}'
    }])

    df = pd.concat([df, summary, min_row, max_row, mean_row], ignore_index=True)
    
    excel_path = "output_audio_info.xlsx"
    df.to_excel(excel_path, index=False)
    
    return excel_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_folder', methods=['POST'])
def process_folder():
    if 'folder' not in request.form:
        return jsonify({"error": "No folder path provided."}), 400
    
    folder_path = request.form['folder']
    
    if not os.path.isdir(folder_path):
        return jsonify({"error": "Provided folder path is invalid."}), 400

    file_info = get_audio_file_info(folder_path)
    
    if not file_info:
        return jsonify({"error": "No audio files found in the folder."}), 400

    excel_file = export_to_excel(file_info)
    return send_file(excel_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

