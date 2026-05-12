import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import skew, kurtosis

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Air Quality Dashboard",
    layout="wide"
)

sns.set(style="whitegrid")

# =========================================================
# TITLE
# =========================================================

st.title("Air Quality Dashboard")

st.markdown("""
Dashboard interaktif untuk analisis kualitas udara Beijing menggunakan dataset PRSA.
""")

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    files = [
        "PRSA_Data_Aotizhongxin_20130301-20170228.csv",
        "PRSA_Data_Changping_20130301-20170228.csv",
        "PRSA_Data_Dingling_20130301-20170228.csv",
        "PRSA_Data_Dongsi_20130301-20170228.csv",
        "PRSA_Data_Guanyuan_20130301-20170228.csv",
        "PRSA_Data_Gucheng_20130301-20170228.csv",
        "PRSA_Data_Huairou_20130301-20170228.csv",
        "PRSA_Data_Nongzhanguan_20130301-20170228.csv",
        "PRSA_Data_Shunyi_20130301-20170228.csv",
        "PRSA_Data_Tiantan_20130301-20170228.csv",
        "PRSA_Data_Wanliu_20130301-20170228.csv",
        "PRSA_Data_Wanshouxigong_20130301-20170228.csv"
    ]

    df_list = []

    for file in files:
        df = pd.read_csv(file)
        df_list.append(df)

    all_df = pd.concat(df_list, ignore_index=True)

    # Datetime
    all_df['datetime'] = pd.to_datetime(
        all_df[['year', 'month', 'day', 'hour']]
    )

    return all_df

all_df = load_data()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("Filter")

selected_station = st.sidebar.multiselect(
    "Pilih Station",
    options=all_df['station'].unique(),
    default=all_df['station'].unique()
)

selected_year = st.sidebar.multiselect(
    "Pilih Tahun",
    options=sorted(all_df['year'].unique()),
    default=sorted(all_df['year'].unique())
)

filtered_df = all_df[
    (all_df['station'].isin(selected_station)) &
    (all_df['year'].isin(selected_year))
]

# =========================================================
# KPI
# =========================================================

st.subheader("Ringkasan Data")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Jumlah Data",
    f"{filtered_df.shape[0]:,}"
)

col2.metric(
    "Rata-rata PM2.5",
    round(filtered_df['PM2.5'].mean(), 2)
)

col3.metric(
    "Rata-rata PM10",
    round(filtered_df['PM10'].mean(), 2)
)

col4.metric(
    "Rata-rata Suhu",
    round(filtered_df['TEMP'].mean(), 2)
)

# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Business Question 1",
    "Business Question 2",
    "EDA Univariate",
    "EDA Multivariate",
    "Raw Data"
])

# =========================================================
# BUSINESS QUESTION 1
# =========================================================

with tab1:

    st.subheader(
        "Pengaruh PM2.5 terhadap Hari Tidak Sehat"
    )

    dongsi_winter = filtered_df[
        (filtered_df['station'] == 'Dongsi') &
        (filtered_df['datetime'] >= '2015-11-01') &
        (filtered_df['datetime'] <= '2016-02-29')
    ]

    daily_pm25 = dongsi_winter.groupby(
        dongsi_winter['datetime'].dt.date
    )['PM2.5'].mean().reset_index()

    daily_pm25['air_quality'] = np.where(
        daily_pm25['PM2.5'] > 150,
        'Tidak Sehat',
        'Sehat'
    )

    unhealthy_days = daily_pm25[
        daily_pm25['air_quality'] == 'Tidak Sehat'
    ]

    st.metric(
        "Jumlah Hari Tidak Sehat",
        unhealthy_days.shape[0]
    )

    fig1, ax1 = plt.subplots(figsize=(14,6))

    sns.lineplot(
        x='datetime',
        y='PM2.5',
        data=daily_pm25,
        ax=ax1
    )

    ax1.axhline(
        y=150,
        color='red',
        linestyle='--',
        label='Batas Tidak Sehat'
    )

    ax1.legend()

    st.pyplot(fig1)

    # Barplot kategori udara

    air_quality_count = daily_pm25[
        'air_quality'
    ].value_counts().reset_index()

    air_quality_count.columns = [
        'Kategori',
        'Jumlah Hari'
    ]

    fig2, ax2 = plt.subplots(figsize=(7,5))

    sns.barplot(
        x='Kategori',
        y='Jumlah Hari',
        data=air_quality_count,
        ax=ax2
    )

    st.pyplot(fig2)

# =========================================================
# BUSINESS QUESTION 2
# =========================================================

with tab2:

    st.subheader(
        "Pengaruh Kecepatan Angin terhadap PM10"
    )

    changping_df = filtered_df[
        (filtered_df['station'] == 'Changping') &
        (filtered_df['datetime'] >= '2016-01-01') &
        (filtered_df['datetime'] <= '2016-06-30')
    ]

    median_wspm = changping_df['WSPM'].median()

    low_wind = changping_df[
        changping_df['WSPM'] < median_wspm
    ]

    high_wind = changping_df[
        changping_df['WSPM'] >= median_wspm
    ]

    low_pm10 = low_wind['PM10'].mean()

    high_pm10 = high_wind['PM10'].mean()

    decrease_percentage = (
        (low_pm10 - high_pm10) / low_pm10
    ) * 100

    st.metric(
        "Penurunan PM10",
        f"{decrease_percentage:.2f}%"
    )

    comparison_df = pd.DataFrame({
        'Kategori Angin': ['Low Wind', 'High Wind'],
        'Rata-rata PM10': [low_pm10, high_pm10]
    })

    fig3, ax3 = plt.subplots(figsize=(8,5))

    sns.barplot(
        x='Kategori Angin',
        y='Rata-rata PM10',
        data=comparison_df,
        ax=ax3
    )

    st.pyplot(fig3)

    # Scatterplot

    fig4, ax4 = plt.subplots(figsize=(10,6))

    sns.regplot(
        x='WSPM',
        y='PM10',
        data=changping_df,
        scatter_kws={'alpha':0.3},
        ax=ax4
    )

    st.pyplot(fig4)

# =========================================================
# EDA UNIVARIATE
# =========================================================

with tab3:

    st.subheader("Descriptive Statistics")

    st.dataframe(
        filtered_df.describe()
    )

    # Histogram

    st.subheader("Histogram PM2.5")

    fig5, ax5 = plt.subplots(figsize=(10,5))

    sns.histplot(
        filtered_df['PM2.5'].dropna(),
        bins=30,
        kde=True,
        ax=ax5
    )

    st.pyplot(fig5)

    # Density plot

    st.subheader("Density Plot PM2.5")

    fig6, ax6 = plt.subplots(figsize=(10,5))

    sns.kdeplot(
        filtered_df['PM2.5'].dropna(),
        fill=True,
        ax=ax6
    )

    st.pyplot(fig6)

    # Boxplot

    st.subheader("Boxplot PM2.5")

    fig7, ax7 = plt.subplots(figsize=(10,4))

    sns.boxplot(
        x=filtered_df['PM2.5'],
        ax=ax7
    )

    st.pyplot(fig7)

    # Skewness & Kurtosis

    st.subheader("Skewness & Kurtosis")

    skewness = skew(
        filtered_df['PM2.5'].dropna()
    )

    kurt = kurtosis(
        filtered_df['PM2.5'].dropna()
    )

    stats_df = pd.DataFrame({
        'Statistik': ['Skewness', 'Kurtosis'],
        'Nilai': [skewness, kurt]
    })

    st.dataframe(stats_df)

    # Countplot

    st.subheader("Jumlah Data per Station")

    fig8, ax8 = plt.subplots(figsize=(12,5))

    sns.countplot(
        x='station',
        data=filtered_df,
        ax=ax8
    )

    plt.xticks(rotation=45)

    st.pyplot(fig8)

# =========================================================
# EDA MULTIVARIATE
# =========================================================

with tab4:

    st.subheader("Correlation Heatmap")

    corr = filtered_df[
        ['PM2.5','PM10','SO2','NO2','CO','O3']
    ].corr()

    fig9, ax9 = plt.subplots(figsize=(10,6))

    sns.heatmap(
        corr,
        annot=True,
        cmap='coolwarm',
        ax=ax9
    )

    st.pyplot(fig9)

    # Pairplot

    st.subheader("Pairplot")

    sample_df = filtered_df[
        ['PM2.5','PM10','SO2','NO2']
    ].dropna().sample(500)

    pairplot = sns.pairplot(sample_df)

    st.pyplot(pairplot.fig)

    # Scatterplot PM2.5 vs PM10

    st.subheader("PM2.5 vs PM10")

    fig10, ax10 = plt.subplots(figsize=(10,6))

    sns.regplot(
        x='PM2.5',
        y='PM10',
        data=filtered_df,
        scatter_kws={'alpha':0.3},
        ax=ax10
    )

    st.pyplot(fig10)

# =========================================================
# RAW DATA
# =========================================================

with tab5:

    st.subheader("Dataset")

    st.dataframe(filtered_df)

    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv'
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption("Dashboard dibuat menggunakan Streamlit")
