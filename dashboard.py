import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# PAGE CONFIG

st.set_page_config(
    page_title="Air Quality Dashboard",
    layout="wide",
    page_icon="🌍"
)

# TITLE

st.title("🌍 Dashboard Analisis Kualitas Udara Beijing")

st.markdown("""
Dashboard interaktif untuk menganalisis kualitas udara berdasarkan dataset PRSA.
""")

# LOAD DATA

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

    data = pd.concat(df_list, ignore_index=True)

    # datetime
    data['datetime'] = pd.to_datetime(
        data[['year', 'month', 'day', 'hour']]
    )

    return data

df = load_data()

# SIDEBAR

st.sidebar.header("🔎 Filter Data")

stations = st.sidebar.multiselect(
    "Pilih Station",
    options=df['station'].unique(),
    default=df['station'].unique()
)

years = st.sidebar.multiselect(
    "Pilih Tahun",
    options=sorted(df['year'].unique()),
    default=sorted(df['year'].unique())
)

# filter dataframe
filtered_df = df[
    (df['station'].isin(stations)) &
    (df['year'].isin(years))
]

# KPI

st.subheader("📌 Ringkasan Data")

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

# ======================================================
# TABS
# ======================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Trend",
    "📊 Distribusi",
    "🔥 Korelasi",
    "📋 Raw Data"
])

# ======================================================
# TAB 1
# ======================================================

with tab1:

    st.subheader("Trend PM2.5")

    trend_pm25 = filtered_df.groupby(
        'year'
    )['PM2.5'].mean()

    fig, ax = plt.subplots(figsize=(12,5))

    trend_pm25.plot(
        marker='o',
        linewidth=3,
        ax=ax
    )

    ax.set_ylabel("PM2.5")
    ax.set_xlabel("Tahun")

    st.pyplot(fig)

    # ==============================================

    st.subheader("Trend PM10")

    trend_pm10 = filtered_df.groupby(
        'year'
    )['PM10'].mean()

    fig2, ax2 = plt.subplots(figsize=(12,5))

    trend_pm10.plot(
        marker='o',
        linewidth=3,
        ax=ax2
    )

    ax2.set_ylabel("PM10")
    ax2.set_xlabel("Tahun")

    st.pyplot(fig2)

# ======================================================
# TAB 2
# ======================================================

with tab2:

    st.subheader("Distribusi PM2.5")

    fig3, ax3 = plt.subplots(figsize=(10,5))

    sns.histplot(
        filtered_df['PM2.5'].dropna(),
        bins=30,
        kde=True,
        ax=ax3
    )

    st.pyplot(fig3)

    # ==============================================

    st.subheader("Scatter Plot PM2.5 vs PM10")

    fig4, ax4 = plt.subplots(figsize=(10,6))

    sns.scatterplot(
        x='PM2.5',
        y='PM10',
        hue='station',
        data=filtered_df,
        ax=ax4
    )

    st.pyplot(fig4)

# ======================================================
# TAB 3
# ======================================================

with tab3:

    st.subheader("Heatmap Korelasi")

    corr = filtered_df[
        ['PM2.5','PM10','SO2','NO2','CO','O3','TEMP','PRES','WSPM']
    ].corr()

    fig5, ax5 = plt.subplots(figsize=(10,8))

    sns.heatmap(
        corr,
        annot=True,
        cmap='coolwarm',
        ax=ax5
    )

    st.pyplot(fig5)

# ======================================================
# TAB 4
# ======================================================

with tab4:

    st.subheader("Raw Dataset")

    st.dataframe(filtered_df)

    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name='filtered_air_quality.csv',
        mime='text/csv'
    )

# ======================================================
# INSIGHT
# ======================================================

st.markdown("---")

st.subheader("🧠 Insight")

st.markdown("""
- PM2.5 dan PM10 memiliki korelasi positif yang cukup kuat.
- Beberapa station menunjukkan tingkat polusi lebih tinggi dibanding lainnya.
- Kecepatan angin cenderung membantu menurunkan konsentrasi polusi udara.
- Polusi udara meningkat pada periode tertentu dan dapat dianalisis berdasarkan tren tahunan.
""")

st.caption("Dashboard dibuat menggunakan Streamlit")