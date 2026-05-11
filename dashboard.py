import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import skew, kurtosis, shapiro
from scipy import stats
import statsmodels.api as sm


st.set_page_config(
    page_title="Air Quality Dashboard",
    layout="wide"
)

sns.set(style='whitegrid')

# TITLE

st.title("Air Quality Dashboard")

st.markdown("""
Dashboard analisis kualitas udara Beijing menggunakan dataset PRSA.
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

    all_df = pd.concat(df_list, ignore_index=True)

    all_df['datetime'] = pd.to_datetime(
        all_df[['year', 'month', 'day', 'hour']]
    )

    return all_df

all_df = load_data()

# SIDEBAR

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

# KPI

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

# TABS

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Descriptive",
    "Univariate",
    "Multivariate",
    "Statistical Test",
    "Raw Data"
])

# TAB 1 - DESCRIPTIVE

with tab1:

    st.subheader("Descriptive Statistics")

    st.dataframe(
        filtered_df.describe()
    )

    st.subheader("Descriptive Statistics (All Columns)")

    st.dataframe(
        filtered_df.describe(include='all')
    )

# TAB 2 - UNIVARIATE

with tab2:

    numerical_cols = [
        'PM2.5',
        'PM10',
        'SO2',
        'NO2',
        'CO',
        'O3'
    ]

    # Histogram
    st.subheader("Histogram")

    fig, ax = plt.subplots(figsize=(12,6))

    filtered_df[numerical_cols].hist(
        bins=30,
        figsize=(15,10)
    )

    st.pyplot(plt)

    # KDE Plot
    st.subheader("Density Plot PM2.5")

    fig2, ax2 = plt.subplots(figsize=(10,5))

    sns.kdeplot(
        filtered_df['PM2.5'].dropna(),
        fill=True,
        ax=ax2
    )

    st.pyplot(fig2)

    # Boxplot
    st.subheader("Boxplot PM2.5")

    fig3, ax3 = plt.subplots(figsize=(10,5))

    sns.boxplot(
        x=filtered_df['PM2.5'],
        ax=ax3
    )

    st.pyplot(fig3)

    # Skewness & Kurtosis
    st.subheader("Skewness & Kurtosis")

    skew_kurt = pd.DataFrame({
        'Column': numerical_cols,
        'Skewness': [
            skew(filtered_df[col].dropna())
            for col in numerical_cols
        ],
        'Kurtosis': [
            kurtosis(filtered_df[col].dropna())
            for col in numerical_cols
        ]
    })

    st.dataframe(skew_kurt)

    # Countplot
    st.subheader("Station Frequency")

    fig4, ax4 = plt.subplots(figsize=(12,5))

    sns.countplot(
        x='station',
        data=filtered_df,
        ax=ax4
    )

    plt.xticks(rotation=45)

    st.pyplot(fig4)

# TAB 3 - MULTIVARIATE

with tab3:

    st.subheader("Correlation Matrix")

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

    # Regression Plot
    st.subheader("Regression Plot PM2.5 vs PM10")

    fig6, ax6 = plt.subplots(figsize=(10,6))

    sns.regplot(
        x='PM2.5',
        y='PM10',
        data=filtered_df,
        scatter_kws={'alpha':0.3},
        ax=ax6
    )

    st.pyplot(fig6)

    # Pairplot
    st.subheader("Pairplot")

    sample_df = filtered_df[
        ['PM2.5','PM10','SO2','NO2']
    ].dropna().sample(500)

    pairplot = sns.pairplot(sample_df)

    st.pyplot(pairplot.fig)

# TAB 4 - STATISTICAL TEST

with tab4:

    st.subheader("Quantile Analysis")

    quantiles = filtered_df[
        ['PM2.5','PM10','SO2','NO2']
    ].quantile(
        [0.05,0.10,0.25,0.50,0.75,0.90,0.95]
    )

    st.dataframe(quantiles)

    # Q-Q Plot
    st.subheader("Q-Q Plot PM2.5")

    fig7 = sm.qqplot(
        filtered_df['PM2.5'].dropna(),
        line='s'
    )

    st.pyplot(fig7)

    # Shapiro Test
    st.subheader("Shapiro-Wilk Test")

    sample_data = filtered_df[
        'PM2.5'
    ].dropna().sample(5000)

    stat, p = shapiro(sample_data)

    st.write(f"Statistics : {stat}")
    st.write(f"P-Value : {p}")

    if p > 0.05:
        st.success("Data berdistribusi normal")
    else:
        st.error("Data tidak berdistribusi normal")

    # ANOVA
    st.subheader("ANOVA Test")

    stations = filtered_df['station'].unique()

    groups = [
        filtered_df[
            filtered_df['station'] == s
        ]['PM2.5'].dropna()
        for s in stations
    ]

    f_stat, p_val = stats.f_oneway(*groups)

    st.write(f"F-Statistic : {f_stat}")
    st.write(f"P-Value : {p_val}")

    if p_val < 0.05:
        st.success(
            "Terdapat perbedaan signifikan rata-rata PM2.5 antar station"
        )
    else:
        st.info(
            "Tidak terdapat perbedaan signifikan rata-rata PM2.5 antar station"
        )

# TAB 5 - RAW DATA

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

# FOOTER

st.markdown("---")

st.caption("Air Quality Dashboard using Streamlit")
