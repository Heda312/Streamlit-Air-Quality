# Air Quality Dashboard

Dashboard interaktif untuk analisis kualitas udara menggunakan dataset PRSA Beijing Air Quality dan Streamlit.

## Struktur Project

project/

- dashboard.py
- requirements.txt
- README.md
- file dataset CSV

## Membuat Virtual Environment

# Windows:

python -m venv venv

Aktifkan environment:

venv\Scripts\activate

# Linux / MacOS:

python3 -m venv venv

Aktifkan environment:

source venv/bin/activate

## Install Library

Install seluruh library menggunakan:

pip install -r requirements.txt

## Menjalankan Dashboard

Jalankan perintah berikut:

streamlit run dashboard.py

Aplikasi akan berjalan pada browser:

http://localhost:8501

## Fitur Dashboard

- Filter station dan tahun
- Statistik deskriptif
- Histogram dan density plot
- Boxplot dan outlier visualization
- Correlation heatmap
- Regression plot
- Pairplot
- Quantile analysis
- Normality testing
- ANOVA statistical test
- Download filtered dataset

## Dataset

Dataset yang digunakan adalah PRSA Beijing Air Quality Dataset periode 2013–2017.

Dataset berisi informasi kualitas udara seperti:
- PM2.5
- PM10
- SO2
- NO2
- CO
- O3
- Temperatur
- Tekanan udara
- Kecepatan angin

## Libraries

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy
- Statsmodels