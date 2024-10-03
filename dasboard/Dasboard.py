import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Memuat dataset day.csv dan hour.csv
day_data = pd.read_csv('dasboard/day.csv')
hour_data = pd.read_csv('dasboard/hour.csv')

# Judul aplikasi Streamlit
st.title("Dashboard Analisis Penggunaan Sepeda")

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
option = st.sidebar.selectbox("Pilih Visualisasi", 
                              ["Jumlah Penyewa Berdasarkan Hari", 
                               "Jumlah Penyewa Berdasarkan Jam",
                               "Distribusi Cuaca & Musim",
                               "Hubungan Suhu dan Penyewa Sepeda",
                               "Distribusi Penyewa per Hari dalam Seminggu"])

# 1. Visualisasi Jumlah Penyewa Berdasarkan Hari
if option == "Jumlah Penyewa Berdasarkan Hari":
    st.subheader("Jumlah Penyewa Sepeda Berdasarkan Hari")
    
    # Mengonversi kolom tanggal ke datetime agar bisa diformat dengan benar
    day_data['dteday'] = pd.to_datetime(day_data['dteday'])
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(day_data['dteday'], day_data['cnt'], label='Jumlah Penyewa', color='blue')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Jumlah Penyewa')
    ax.set_title('Jumlah Penyewa Sepeda Harian')
    
    # Format sumbu x dengan tanggal
    ax.xaxis.set_major_locator(mdates.MonthLocator())  # Menampilkan setiap bulan
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Format tanggal
    plt.xticks(rotation=45)  # Memutar label tanggal agar tidak bertumpuk
    
    st.pyplot(fig)

# 2. Visualisasi Jumlah Penyewa Berdasarkan Jam
elif option == "Jumlah Penyewa Berdasarkan Jam":
    st.subheader("Jumlah Penyewa Sepeda Berdasarkan Jam")
    hourly_avg = hour_data.groupby('hr')['cnt'].mean()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(hourly_avg.index, hourly_avg, color='green')
    ax.set_xlabel('Jam')
    ax.set_ylabel('Rata-rata Penyewa')
    ax.set_title('Rata-rata Penyewa Sepeda Berdasarkan Jam')
    st.pyplot(fig)

# 3. Visualisasi Distribusi Cuaca & Musim
elif option == "Distribusi Cuaca & Musim":
    st.subheader("Distribusi Penggunaan Sepeda Berdasarkan Cuaca dan Musim")
    
    # Distribusi berdasarkan cuaca
    weather_avg = day_data.groupby('weathersit')['cnt'].mean()
    fig, ax = plt.subplots(figsize=(8, 5))

    # Periksa jumlah kategori cuaca dalam dataset
    categories = weather_avg.index

    # Tetapkan label hanya untuk kategori yang ada
    labels = ['Cerah', 'Berkabut', 'Hujan Ringan', 'Hujan Lebat']
    ax.bar(categories, weather_avg, color=['skyblue', 'orange', 'green', 'red'])
    ax.set_xlabel('Kategori Cuaca')
    ax.set_ylabel('Rata-rata Penyewa')
    ax.set_title('Rata-rata Penyewa Berdasarkan Cuaca')

    # Sesuaikan label x berdasarkan kategori yang ada
    ax.set_xticks(categories)
    ax.set_xticklabels([labels[i - 1] for i in categories], rotation=0)
    st.pyplot(fig)

    # Distribusi berdasarkan musim
    season_avg = day_data.groupby('season')['cnt'].mean()
    season_labels = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
    season_avg.index = season_avg.index.map(season_labels)
    fig, ax = plt.subplots(figsize=(8, 5))
    season_avg.plot(kind='bar', ax=ax, color=['springgreen', 'gold', 'orange', 'lightblue'])
    ax.set_xlabel('Musim')
    ax.set_ylabel('Rata-rata Penyewa')
    ax.set_title('Rata-rata Penyewa Berdasarkan Musim')
    st.pyplot(fig)

# 4. Hubungan antara Suhu dan Penyewa Sepeda
elif option == "Hubungan Suhu dan Penyewa Sepeda":
    st.subheader("Hubungan antara Suhu dan Jumlah Penyewa Sepeda")
    day_data['temp_celsius'] = day_data['temp'] * (39 - (-8)) + (-8)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(day_data['temp_celsius'], day_data['cnt'], color='orange')
    ax.set_xlabel('Suhu (Celsius)')
    ax.set_ylabel('Jumlah Penyewa')
    ax.set_title('Hubungan Suhu dan Jumlah Penyewa Sepeda')
    st.pyplot(fig)

# 5. Distribusi Penyewa per Hari dalam Seminggu
elif option == "Distribusi Penyewa per Hari dalam Seminggu":
    st.subheader("Distribusi Penyewa Sepeda Berdasarkan Hari dalam Seminggu")
    day_data['weekday'] = pd.to_datetime(day_data['dteday']).dt.day_name()
    weekday_avg = day_data.groupby('weekday')['cnt'].mean().sort_values()
    fig, ax = plt.subplots(figsize=(10, 5))
    weekday_avg.plot(kind='bar', ax=ax, color='purple')
    ax.set_xlabel('Hari')
    ax.set_ylabel('Rata-rata Penyewa')
    ax.set_title('Rata-rata Penyewa Berdasarkan Hari dalam Seminggu')
    plt.xticks(rotation=45)
    st.pyplot(fig)
