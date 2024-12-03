import streamlit as st
import pandas as pd
import plotly.express as px

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
st.title("Dashboard Kasus Penyakit di Indonesia")
st.markdown("**Aplikasi ini wajib bisa diakses secara online**")
st.markdown("### Identitas Kelompok")
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

# Grafik Tren Kasus per Tahun
st.subheader("Tren Jumlah Kasus per Tahun")
cases_by_year = filtered_data.groupby("tahun")["jumlah_kasus"].sum().reset_index()
fig_trend = px.line(
    cases_by_year,
    x="tahun",
    y="jumlah_kasus",
    title="Jumlah Kasus per Tahun",
    labels={"jumlah_kasus": "Jumlah Kasus", "tahun": "Tahun"},
)
st.plotly_chart(fig_trend)

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

# Peta Interaktif (Opsional jika data lokasi tersedia)
if "nama_provinsi" in filtered_data.columns:
    st.subheader("Peta Interaktif Jumlah Kasus")
    geo_data = filtered_data.groupby("nama_provinsi")["jumlah_kasus"].sum().reset_index()
    fig_map = px.choropleth(
        geo_data,
        locations="nama_provinsi",
        locationmode="country names",
        color="jumlah_kasus",
        title="Peta Sebaran Kasus per Provinsi",
        labels={"jumlah_kasus": "Jumlah Kasus"},
    )
    st.plotly_chart(fig_map)
