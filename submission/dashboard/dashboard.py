
import streamlit as st
import pandas as pd

#load data 
dingling = pd.read_csv('main_data.csv')

#clenaing data 
# Pengisian data elemen yang kosong
dingling = dingling.fillna(method='bfill')
#membauat data set menjadi date_time
dingling['date_time'] = pd.to_datetime(dingling[['year', 'month', 'day', 'hour']]) 
dingling.drop(['No', 'year', 'month', 'day', 'hour'], axis=1, inplace=True)
# Fungsi untuk menghitung rata-rata polusi udara untuk rentang waktu tertentu
def calculate_air_pollution_data(dataframe, start_datetime, end_datetime):
    # Filter data berdasarkan rentang waktu
    filtered_data = dataframe[
        (dataframe['date_time'] >= start_datetime) & (dataframe['date_time'] <= end_datetime)
    ].copy()

    # Group by hour dan hitung rata-rata polusi udara
    hourly_avg_pollution = filtered_data.groupby(filtered_data['date_time'].dt.hour).agg({
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean",
    })

    # Bulatkan hasilnya
    hourly_avg_pollution = hourly_avg_pollution.round(0)

    return hourly_avg_pollution

# Load data
dingling = pd.read_csv('main_data.csv')  # Ganti dengan nama file CSV Anda

# Streamlit app
st.title('Analisis Polusi Udara')

# Pilihan rentang waktu
start_date = st.date_input('Pilih Tanggal Awal', value=pd.to_datetime('2013-03-01'))
end_date = st.date_input('Pilih Tanggal Akhir', value=pd.to_datetime('2013-03-01'))

# Pastikan 'date_time' dalam dataframe adalah tipe datetime
dingling['date_time'] = pd.to_datetime(dingling['date_time'])

# Panggil fungsi untuk menghitung rata-rata polusi udara
dingling_air_data_pollution_hour = calculate_air_pollution_data(dingling, start_date, end_date)

# Tampilkan hasilnya dalam tabel di Streamlit
st.write("Rata-rata polusi udara per jam:")
st.write(dingling_air_data_pollution_hour)

dingling['date_time'] = pd.to_datetime(dingling['date_time'])

# Input dari pengguna untuk rentang tanggal
start_date = st.date_input("Pilih Tanggal Awal", min_value=pd.to_datetime(dingling['date_time']).min())
end_date = st.date_input("Pilih Tanggal Akhir", max_value=pd.to_datetime(dingling['date_time']).max())

# Filter data berdasarkan rentang tanggal
dingling_filtered = dingling[(dingling['date_time'] >= start_date) & (dingling['date_time'] <= end_date)]

# Group by date (ignoring time), then calculate means
dingling_air_data_pollution_days = dingling_filtered.groupby(dingling_filtered['date_time'].dt.date).agg({
    "PM2.5": "mean",
    "PM10": "mean",
    "SO2": "mean",
    "NO2": "mean",
    "CO": "mean",
    "O3": "mean",
}).reset_index()

# Membulatkan nilai rata-rata ke bilangan bulat
dingling_air_data_pollution_days = dingling_air_data_pollution_days.round(0)

# Tampilkan data dalam tabel di Streamlit
st.write("Data Polusi Udara (Rata-rata per Hari)")
st.write(dingling_air_data_pollution_days)

# Visualisasi data menggunakan matplotlib di Streamlit
st.write("Grafik Rata-rata PM2.5 per Hari")
plt.figure(figsize=(10, 6))
plt.plot(dingling_air_data_pollution_days['date_time'], dingling_air_data_pollution_days['PM2.5'], marker='o')
plt.xlabel('Tanggal')
plt.ylabel('Rata-rata PM2.5')
plt.xticks(rotation=45)
st.pyplot()

# Visualisasi data menggunakan seaborn di Streamlit
st.write("Boxplot SO2 per Hari")
import seaborn as sns
plt.figure(figsize=(8, 6))
sns.boxplot(x=dingling_air_data_pollution_days['SO2'])
plt.xlabel('SO2')
st.pyplot()