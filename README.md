# Air Quality Dashboard #

Dashboard interaktif untuk analisis kualitas udara menggunakan dataset PRSA Beijing Air Quality dan Streamlit.

## Cara Menjalankan

1. Install library yang dibutuhkan

[bash]
pip install streamlit pandas matplotlib seaborn numpy

2. Pastikan file `dashboard.py` dan seluruh file dataset `.csv` berada dalam satu folder.

3. Jalankan aplikasi Streamlit

[bash]
streamlit run dashboard.py

4. Buka browser dan akses:

[bash]
http://localhost:8501

## Fitur Dashboard

- Filter station
- Filter tahun
- Statistik data
- Visualisasi PM2.5 dan PM10
- Heatmap korelasi
- Download dataset hasil filter

## Libraries

- Python
- Streamlit
- Pandas
- Matplotlib
- Seaborn