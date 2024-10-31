import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

# Generate sample data
jenis_surat_list = [
    'Pengumuman', 'Nota Dinas', 'Surat', 'Surat Tugas', 
    'Undangan', 'Surat Perintah', 'Surat Keterangan', 
    'Surat Edaran', 'Berita Acara', 'Laporan', 'Notula', 'Surat Kuasa'
]
data = []

# Randomly generate data for each type of letter with different quantities
for jenis_surat in jenis_surat_list:
    for _ in range(random.randint(5, 30)):  # Random number of each type
        tanggal_terima = datetime(2024, 10, random.randint(1, 20))
        perlu_respon = random.choice([True, False])
        jatuh_tempo = (tanggal_terima + timedelta(days=random.randint(5, 15))) if perlu_respon else None
        status_respon = 'Belum direspons' if perlu_respon else 'Tidak perlu'
        if perlu_respon and random.choice([True, False]):
            status_respon = 'Sudah direspons'
        
        data.append({
            'ID Surat': random.randint(1000, 9999),
            'Jenis Surat': jenis_surat,
            'Tanggal Terima': tanggal_terima,
            'Perlu Respon': perlu_respon,
            'Jatuh Tempo': jatuh_tempo,
            'Status Respon': status_respon,
            'Keterangan': '' if status_respon == 'Tidak perlu' else 'Perlu tindak lanjut' if status_respon == 'Belum direspons' else 'Respon dikirim'
        })

# Create DataFrame
df = pd.DataFrame(data)

# Display the logo in the top-left corner
st.markdown(
    """
    <style>
    .logo {
        display: flex;
        align-items: center;
        position: absolute;
        top: 10px;
        left: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.image("logo-kemenkeu.png", width=100)

# Sidebar filters
st.sidebar.title("Filter Surat")
jenis_surat_filter = st.sidebar.multiselect("Pilih Jenis Surat", options=df['Jenis Surat'].unique(), default=df['Jenis Surat'].unique())
respon_filter = st.sidebar.selectbox("Perlu Respon?", options=["Semua", "Perlu", "Tidak Perlu"])

# Filter Data
filtered_df = df[df['Jenis Surat'].isin(jenis_surat_filter)]
if respon_filter == "Perlu":
    filtered_df = filtered_df[filtered_df['Perlu Respon'] == True]
elif respon_filter == "Tidak Perlu":
    filtered_df = filtered_df[filtered_df['Perlu Respon'] == False]

# Display Dashboard
st.title("Dashboard Monitoring Surat")

# 1. Bar Chart: Jumlah Surat per Jenis
st.subheader("Jumlah Surat Berdasarkan Jenis")
jenis_count = filtered_df['Jenis Surat'].value_counts().reset_index()
jenis_count.columns = ['Jenis Surat', 'Jumlah']
bar_chart = px.bar(
    jenis_count, 
    x='Jenis Surat', 
    y='Jumlah', 
    title="Jumlah Surat per Jenis", 
    color_discrete_sequence=['#005bbb'],  # Biru
)
st.plotly_chart(bar_chart)

# 2. Pie Chart: Proporsi Surat Perlu Respon vs Tidak Perlu Respon
st.subheader("Proporsi Surat Perlu Respon vs Tidak Perlu Respon")
respon_count = filtered_df['Perlu Respon'].value_counts().reset_index()
respon_count.columns = ['Perlu Respon', 'Jumlah']
respon_count['Perlu Respon'] = respon_count['Perlu Respon'].map({True: 'Perlu Respon', False: 'Tidak Perlu Respon'})
pie_chart = px.pie(
    respon_count, 
    names='Perlu Respon', 
    values='Jumlah', 
    title="Proporsi Surat Perlu Respon vs Tidak Perlu Respon", 
    color_discrete_sequence=['#005bbb', '#ffd700']  # Biru dan Kuning
)
st.plotly_chart(pie_chart)

# 3. Line Chart: Waktu Tersisa untuk Surat yang Perlu Respon
st.subheader("Monitoring Jatuh Tempo untuk Surat yang Perlu Respon")
jatuh_tempo_df = filtered_df[filtered_df['Perlu Respon'] == True].copy()
jatuh_tempo_df['Waktu Tersisa (Hari)'] = (jatuh_tempo_df['Jatuh Tempo'] - datetime.now()).dt.days
line_chart = px.line(
    jatuh_tempo_df, 
    x='Jenis Surat', 
    y='Waktu Tersisa (Hari)', 
    title="Waktu Tersisa untuk Surat yang Perlu Respon", 
    markers=True,
    color_discrete_sequence=['#ffd700']  # Kuning
)
st.plotly_chart(line_chart)

# Tabel Surat yang Perlu Respon
st.subheader("Tabel Surat yang Perlu Respon")
perlu_respon_df = filtered_df[filtered_df['Perlu Respon'] == True]
st.write(perlu_respon_df[['ID Surat', 'Jenis Surat', 'Tanggal Terima', 'Jatuh Tempo', 'Status Respon']])

# Tabel Surat yang Tidak Perlu Respon
st.subheader("Tabel Surat yang Tidak Perlu Respon")
tidak_perlu_respon_df = filtered_df[filtered_df['Perlu Respon'] == False]
st.write(tidak_perlu_respon_df[['ID Surat', 'Jenis Surat', 'Tanggal Terima']])
