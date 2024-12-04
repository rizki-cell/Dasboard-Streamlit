import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data_path = "dinkes-od_15940_jumlah_kasus_penyakit_berdasarkan_jenis_penyakit_data.csv"
data = pd.read_csv(data_path)

# Sidebar Filters
st.sidebar.header("Filter Data")
selected_year = st.sidebar.multiselect(
    "Pilih Tahun", options=data["tahun"].unique(), default=data["tahun"].unique()
)
selected_province = st.sidebar.multiselect(
    "Pilih Provinsi", options=data["nama_provinsi"].unique(), default=data["nama_provinsi"].unique()
)

# Filter data
filtered_data = data[
    (data["tahun"].isin(selected_year)) & (data["nama_provinsi"].isin(selected_province))
]

# Dashboard Header
st.title("Dashboard Kasus Penyakit di Jawa Barat Tahun 2019")
st.markdown("### Anggota Kelompok")
st.markdown("""
- **NRP 1**: 210514007 - M Rizki Pratama  
- **NRP 2**: 210514016 - Niko Fauzan S 
- **NRP 3**: 210514014 - Fauzan Kamal
- **NRP 4**: 229534030 - Nida salamah
- **NRP 5**: 210514011 - Rizkita Mayra
""")

# KPI Metrics
st.header("Ringkasan")
col1, col2, col3 = st.columns(3)
col1.metric("Total Kasus", f"{filtered_data['jumlah_kasus'].sum():,}")
col2.metric("Jenis Penyakit", filtered_data["jenis_penyakit"].nunique())
col3.metric("Kabupaten/Kota", filtered_data["nama_kabupaten_kota"].nunique())

import streamlit as st
import pandas as pd


# Hitung statistik deskriptif
@st.cache_data
def calculate_descriptive_stats(data):
    descriptive_stats = data.groupby('jenis_penyakit')['jumlah_kasus'].agg(['mean', 'median', pd.Series.mode]).reset_index()
    descriptive_stats['mean'] = descriptive_stats['mean'].round(2)
    descriptive_stats['median'] = descriptive_stats['median'].round(2)
    descriptive_stats['mode'] = descriptive_stats['mode'].apply(lambda x: x if isinstance(x, list) else [x])
    return descriptive_stats

descriptive_stats = calculate_descriptive_stats(data)


# Tampilkan Tabel Statistik Deskriptif
st.subheader("Statistik Deskriptif")
st.dataframe(descriptive_stats)

# Tambahkan Ringkasan Angka
st.subheader("Ringkasan Statistik")
total_penyakit = descriptive_stats['jenis_penyakit'].nunique()
total_kasus = data['jumlah_kasus'].sum()

col1, col2 = st.columns(2)
col1.metric("Jenis Penyakit", total_penyakit)
col2.metric("Total Kasus", f"{total_kasus:,}")

# Visualisasi Tren Kasus Berdasarkan Jenis Penyakit
st.subheader("Visualisasi Tren Kasus per Jenis Penyakit")
selected_disease = st.selectbox("Pilih Jenis Penyakit", descriptive_stats['jenis_penyakit'])
filtered_data = data[data['jenis_penyakit'] == selected_disease]

if not filtered_data.empty:
    trend_chart = filtered_data.groupby('tahun')['jumlah_kasus'].sum().reset_index()
    st.line_chart(trend_chart.set_index('tahun'))
else:
    st.warning("Tidak ada data untuk jenis penyakit yang dipilih.")


# Grafik Kasus Berdasarkan Provinsi
st.subheader("Jumlah Kasus Berdasarkan Provinsi")
cases_by_province = filtered_data.groupby("nama_provinsi")["jumlah_kasus"].sum().reset_index()
fig_province = px.bar(
    cases_by_province,
    x="nama_provinsi",
    y="jumlah_kasus",
    title="Jumlah Kasus per Provinsi",
    labels={"jumlah_kasus": "Jumlah Kasus", "nama_provinsi": "Provinsi"},
    text="jumlah_kasus",
)
fig_province.update_traces(texttemplate='%{text:.2s}', textposition='outside')
st.plotly_chart(fig_province)

# Grafik Kasus Berdasarkan Jenis Penyakit
st.subheader("Jumlah Kasus Berdasarkan Jenis Penyakit")
cases_by_disease = filtered_data.groupby("jenis_penyakit")["jumlah_kasus"].sum().reset_index()
fig_disease = px.pie(
    cases_by_disease,
    values="jumlah_kasus",
    names="jenis_penyakit",
    title="Distribusi Kasus Berdasarkan Jenis Penyakit",
)
st.plotly_chart(fig_disease)

# --- Penyakit Dominan di Setiap Kota ---
st.subheader("Penyakit dengan Jumlah Kasus Tertinggi di Setiap Kota/Kabupaten")

# Menentukan penyakit dengan jumlah kasus tertinggi di setiap kabupaten/kota
dominant_disease_city = data.loc[data.groupby('nama_kabupaten_kota')['jumlah_kasus'].idxmax()]
dominant_chart = px.bar(
    dominant_disease_city,
    x='jumlah_kasus',
    y='nama_kabupaten_kota',
    color='jenis_penyakit',
    orientation='h',
    title="Penyakit dengan Jumlah Kasus Tertinggi di Setiap Kota/Kabupaten",
    labels={
        "jumlah_kasus": "Jumlah Kasus",
        "nama_kabupaten_kota": "Kota/Kabupaten",
        "jenis_penyakit": "Jenis Penyakit"
    },
    text='jumlah_kasus'
)

dominant_chart.update_layout(
    xaxis_title="Jumlah Kasus",
    yaxis_title="Kota/Kabupaten",
    legend_title="Jenis Penyakit"
)

st.plotly_chart(dominant_chart)

# Pivot data untuk mendapatkan jumlah kasus tiap penyakit di setiap kabupaten/kota
pivot_data = data.pivot_table(values='jumlah_kasus', index='nama_kabupaten_kota', columns='jenis_penyakit', fill_value=0)

# Menghitung korelasi antara penyakit
correlation_matrix = pivot_data.corr()
print(correlation_matrix)

# Plot heatmap untuk matriks korelasi
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1) # Now sns is defined
plt.title("Matriks Korelasi Antar Penyakit")
plt.show()