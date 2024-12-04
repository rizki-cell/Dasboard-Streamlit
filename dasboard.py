import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

# Load data
data_path = "dinkes-od_15940_jumlah_kasus_penyakit_berdasarkan_jenis_penyakit_data.csv"
data = pd.read_csv(data_path)

# Load data
data_path = "dinkes-od_15940_jumlah_kasus_penyakit_berdasarkan_jenis_penyakit_data.csv"
data = pd.read_csv(data_path)

# Sidebar Filters

# Menambahkan logo Dinas Kesehatan di Sidebar
logo_path = "images.jpg"  # Ganti dengan path ke logo yang sesuai
st.sidebar.image(logo_path, use_container_width=True, caption="Dinas Kesehatan Jawa Barat")

# Filter Tahun
selected_year = st.sidebar.multiselect(
    "📅 Pilih Tahun", 
    options=data["tahun"].unique(), 
    default=data["tahun"].unique(),
    help="Pilih satu atau beberapa tahun untuk melihat data kasus penyakit."
)

# Filter Kota/Kabupaten
selected_city = st.sidebar.multiselect(
    "🏙️ Pilih Kota/Kabupaten", 
    options=data["nama_kabupaten_kota"].unique(),  # Pastikan kolom ini ada dalam dataset Anda
    default=data["nama_kabupaten_kota"].unique(),
    help="Pilih satu atau lebih Kota/Kabupaten untuk melihat distribusi kasus penyakit."
)

# Informasi Sidebar
st.sidebar.markdown("""
**Info:**
- Gunakan filter untuk menyesuaikan data berdasarkan Tahun dan Kabupaten/kota.
- Anda dapat memilih beberapa opsi dari masing-masing filter.
""")

# Menampilkan jumlah data yang dipilih di sidebar
st.sidebar.markdown(f"### Total Data yang Dipilih: {len(selected_year)} Tahun, {len(selected_city)} Kota/Kabupaten")

# Filter data berdasarkan pilihan
filtered_data = data[
    (data["tahun"].isin(selected_year)) & (data["nama_kabupaten_kota"].isin(selected_city))  # Menggunakan kolom kota/kabupaten
]

# Menampilkan data yang difilter di halaman utama
st.title("Dashboard Kasus Penyakit")
st.markdown("### Data yang difilter:")
st.dataframe(filtered_data)

# KPI Metrics
st.header("Ringkasan")
col1, col2, col3 = st.columns(3)
col1.metric("Total Kasus", f"{filtered_data['jumlah_kasus'].sum():,}")
col2.metric("Jenis Penyakit", filtered_data["jenis_penyakit"].nunique())
col3.metric("Kabupaten/Kota", filtered_data["nama_kabupaten_kota"].nunique())

# Periksa kolom-kolom dalam data
print(data.columns)

# Hitung statistik deskriptif
@st.cache_data
def calculate_descriptive_stats(data):
    # Melakukan agregasi berdasarkan 'jenis_penyakit'
    descriptive_stats = data.groupby('jenis_penyakit')['jumlah_kasus'].agg(['mean', 'median', pd.Series.mode]).reset_index()
    
    # Memeriksa kolom setelah agregasi
    print(descriptive_stats.columns)
    
    # Jika kolom 'jumlah_kasus' ada, lanjutkan proses konversi
    if 'jumlah_kasus' in descriptive_stats.columns:
        descriptive_stats['jumlah_kasus'] = pd.to_numeric(descriptive_stats['jumlah_kasus'], errors='coerce')
    
    # Pastikan 'jenis_penyakit' bertipe string
    descriptive_stats['jenis_penyakit'] = descriptive_stats['jenis_penyakit'].astype(str)

    return descriptive_stats

# Calculate descriptive stats
descriptive_stats = calculate_descriptive_stats(data)

# Tampilkan Tabel Statistik Deskriptif
st.subheader("Statistik Deskriptif")
st.dataframe(descriptive_stats)

# Tambahkan visualisasi lainnya sesuai kebutuhan
# Misalnya, visualisasi menggunakan plotly atau seaborn
# Visualisasi distribusi kasus berdasarkan jenis penyakit
st.subheader("Distribusi Kasus Berdasarkan Jenis Penyakit")
cases_by_disease = data.groupby('jenis_penyakit')['jumlah_kasus'].sum().reset_index()
fig = px.bar(cases_by_disease, x='jenis_penyakit', y='jumlah_kasus', title="Jumlah Kasus Berdasarkan Jenis Penyakit")
st.plotly_chart(fig)

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

# --- Penyakit dengan Jumlah Kasus Terkecil ---
st.subheader("Penyakit dengan Jumlah Kasus Terkecil di Setiap Kota/Kabupaten")

# Menentukan penyakit dengan jumlah kasus terkecil di setiap kabupaten/kota
smallest_disease_city = data.loc[data.groupby('nama_kabupaten_kota')['jumlah_kasus'].idxmin()]

# Membuat visualisasi bar chart horizontal
smallest_chart = px.bar(
    smallest_disease_city,
    x='jumlah_kasus',
    y='nama_kabupaten_kota',
    color='jenis_penyakit',
    orientation='h',
    title="Penyakit dengan Jumlah Kasus Terkecil di Setiap Kota/Kabupaten",
    labels={
        "jumlah_kasus": "Jumlah Kasus",
        "nama_kabupaten_kota": "Kota/Kabupaten",
        "jenis_penyakit": "Jenis Penyakit"
    },
    text='jumlah_kasus'
)

# Menyesuaikan tata letak chart
smallest_chart.update_layout(
    xaxis_title="Jumlah Kasus",
    yaxis_title="Kota/Kabupaten",
    legend_title="Jenis Penyakit"
)

# Menampilkan chart pada Streamlit
st.plotly_chart(smallest_chart)


st.subheader("Jumlah Kasus Berdasarkan Jenis Penyakit")
cases_by_disease = filtered_data.groupby("jenis_penyakit")["jumlah_kasus"].sum().reset_index()
fig_disease = px.pie(
    cases_by_disease,
    values="jumlah_kasus",
    names="jenis_penyakit",
    title="Distribusi Kasus Berdasarkan Jenis Penyakit",
)
st.plotly_chart(fig_disease)


# Menghitung korelasi antara penyakit
st.subheader("Matriks Korelasi Antar Penyakit")
correlation_matrix = pivot_data.corr()
st.write("Matriks Korelasi Antar Penyakit:")
st.write(correlation_matrix)

# Plot heatmap untuk matriks korelasi
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)


# Tampilkan plot menggunakan Streamlit
st.pyplot(plt)