import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import timedelta

# Load data
try:
    dingling = pd.read_csv('./submission/dashboard/main_data.csv', encoding='utf-8')
except FileNotFoundError:
    st.error("File not found. Please check the file path.")
    st.stop()

# Data Cleaning
dingling = dingling.bfill()  
dingling.drop(['No', 'station'], axis=1, inplace=True)

st.title('Analisis Kualitas Udara di Kota Dingling (2013-2017)')

# Aggregating data
def aggregate_data(df, group_by_cols):
    aggregated_df = df.groupby(by=group_by_cols).agg({
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean"
    }).sort_values(by=group_by_cols, ascending=True).reset_index()

    return aggregated_df.round({
        "PM2.5": 0,
        "PM10": 0,
        "SO2": 0,
        "NO2": 0,
        "CO": 0,
        "O3": 0
    })

# Daily aggregation
dingling_polusi_harian = aggregate_data(dingling, ['year', 'month', 'day', 'hour'])
dingling_polusi_harian['date_time'] = pd.to_datetime(dingling_polusi_harian[['year', 'month', 'day', 'hour']])
dingling_polusi_harian = dingling_polusi_harian.set_index('date_time').drop(columns=['year', 'month', 'day', 'hour'])

# Weekly aggregation
dingling_polusi_mingguan = aggregate_data(dingling, ['year', 'month', 'day'])
dingling_polusi_mingguan['date_time'] = pd.to_datetime(dingling_polusi_mingguan[['year', 'month', 'day']])
dingling_polusi_mingguan = dingling_polusi_mingguan.set_index('date_time').drop(columns=['year', 'month', 'day'])

# Monthly aggregation
dingling_polusi_bulanan = aggregate_data(dingling, ['year', 'month'])
dingling_polusi_bulanan['date_time'] = pd.to_datetime(dingling_polusi_bulanan[['year', 'month']].assign(day=1))
dingling_polusi_bulanan = dingling_polusi_bulanan.set_index('date_time').drop(columns=['year', 'month'])

# Annual aggregation
dingling_polusi_tahunan = aggregate_data(dingling, ['year'])
dingling_polusi_tahunan['time'] = dingling_polusi_tahunan['year'].astype(str)
dingling_polusi_tahunan = dingling_polusi_tahunan.set_index(pd.to_datetime(dingling_polusi_tahunan['time'] + '-01-01')).drop(columns=['year', 'time'])

# Filtering and displaying data
def filter_and_display_data(df, period, key_suffix):
    start_date = st.date_input(f'Mulai tanggal ({period})', value=pd.to_datetime('2013-03-01'), key=f'start_date_{key_suffix}')
    if start_date is not None:
        if period == 'Harian':
            end_date = start_date + timedelta(days=1)
        elif period == 'Mingguan':
            end_date = start_date + timedelta(days=7)
        elif period == 'Bulanan':
            end_date = start_date + timedelta(days=30)
        elif period == 'Tahunan':
            end_date = start_date + timedelta(days=365)
        st.write(f'Sampai tanggal: {end_date.strftime("%Y-%m-%d")}')
        
        try:
            mask = (df.index >= pd.to_datetime(start_date)) & (df.index < pd.to_datetime(end_date))
            filtered_data = df.loc[mask]
        except Exception as e:
            st.error(f"An error occurred while filtering the data: {e}")
            st.stop()

        st.header(f'Data yang Difilter Berdasarkan Tanggal ({period})')
        st.write(filtered_data)
        return filtered_data

# Display data for different periods
daily_filtered_data = filter_and_display_data(dingling_polusi_harian, 'Harian', 'daily_pollution')
weekly_filtered_data = filter_and_display_data(dingling_polusi_mingguan, 'Mingguan', 'weekly_pollution')
monthly_filtered_data = filter_and_display_data(dingling_polusi_bulanan, 'Bulanan', 'monthly_pollution')
annual_filtered_data = filter_and_display_data(dingling_polusi_tahunan, 'Tahunan', 'annual_pollution')

# Visualisasi
def dingling_polusi_graph(df, title):
    fig, ax = plt.subplots(nrows=3, ncols=2, figsize=(15, 15))

    ax[0,0].plot(df.index, df['PM2.5'], marker='o', linewidth=2, color="#39064B")
    ax[0,0].tick_params(axis='y', labelsize=12)
    ax[0,0].tick_params(axis='x', labelsize=12, labelrotation = 45)
    ax[0,0].set_ylabel("PM2.5", fontsize=15)
    ax[0,0].set_title("PM2.5", loc="center", fontsize=18)

    ax[0,1].plot(df.index, df['PM10'], marker='o', linewidth=2, color="#39064B")
    ax[0,1].tick_params(axis='y', labelsize=12)
    ax[0,1].tick_params(axis='x', labelsize=12, labelrotation = 45)
    ax[0,1].set_ylabel("PM10", fontsize=15)
    ax[0,1].set_title("PM10", loc="center", fontsize=18)

    ax[1,0].plot(df.index, df['SO2'], marker='o', linewidth=2, color="#39064B")
    ax[1,0].tick_params(axis='y', labelsize=12)
    ax[1,0].tick_params(axis='x', labelsize=12, labelrotation = 45)
    ax[1,0].set_ylabel("SO2", fontsize=15)
    ax[1,0].set_title("SO2", loc="center", fontsize=18)

    ax[1,1].plot(df.index, df['NO2'], marker='o', linewidth=2, color="#39064B")
    ax[1,1].tick_params(axis='y', labelsize=12)
    ax[1,1].tick_params(axis='x', labelsize=12, labelrotation = 45)
    ax[1,1].set_ylabel("NO2", fontsize=15)
    ax[1,1].set_title("NO2", loc="center", fontsize=18)

    ax[2,0].plot(df.index, df['CO'], marker='o', linewidth=2, color="#39064B")
    ax[2,0].tick_params(axis='y', labelsize=12)
    ax[2,0].tick_params(axis='x', labelsize=12, labelrotation = 45)
    ax[2,0].set_ylabel("CO", fontsize=15)
    ax[2,0].set_title("CO", loc="center", fontsize=18)

    ax[2,1].plot(df.index, df['O3'], marker='o', linewidth=2, color="#39064B")
    ax[2,1].tick_params(axis='y', labelsize=12)
    ax[2,1].tick_params(axis='x', labelsize=12, labelrotation = 45)
    ax[2,1].set_ylabel("O3", fontsize=15)
    ax[2,1].set_title("O3", loc="center", fontsize=18)

    fig.tight_layout(pad=2.0)

    plt.suptitle(title, fontsize=22, y=1.02)
    st.pyplot(fig)

# Display graphs for the filtered data
if daily_filtered_data is not None and not daily_filtered_data.empty:
    st.header("Trend Polusi Udara Harian")
    dingling_polusi_graph(daily_filtered_data, "Trend Tingkat Polusi Udara Harian di Dingling")

if weekly_filtered_data is not None and not weekly_filtered_data.empty:
    st.header("Trend Polusi Udara Mingguan")
    dingling_polusi_graph(weekly_filtered_data, "Trend Tingkat Polusi Udara Mingguan di Dingling")

if monthly_filtered_data is not None and not monthly_filtered_data.empty:
    st.header("Trend Polusi Bulanan")
    dingling_polusi_graph(monthly_filtered_data, "Trend Polusi Bulanan")

# Fungsi untuk mengklasifikasikan tingkat polusi
def dingling_polusi(df):
    pm25 = round(df['PM2.5'].mean(), 1)
    pm10 = round(df['PM10'].mean(), 1)
    so2 = round(df['SO2'].mean(), 1)
    no2 = round(df['NO2'].mean(), 1)
    co = round(df['CO'].mean(), 1)
    o3 = round(df['O3'].mean(), 1)
    
    if pm25 >= 250 or pm10 >= 420 or so2 >= 2620 or no2 >= 1130 or co >= 60 or o3 >= 800:
        return 'Berbahaya'
    elif pm25 >= 150 or pm10 >= 355 or so2 >= 1310 or no2 >= 565 or co >= 30 or o3 >= 400:
        return 'Sangat Tidak Sehat'
    elif pm25 >= 115 or pm10 >= 250 or so2 >= 800 or no2 >= 375 or co >= 17 or o3 >= 300:
        return 'Tidak Sehat'
    elif pm25 >= 75 or pm10 >= 150 or so2 >= 365 or no2 >= 188 or co >= 9 or o3 >= 180:
        return 'Tidak Sehat bagi Kelompok Sensitif'
    elif pm25 >= 35 or pm10 >= 50 or so2 >= 80 or no2 >= 100 or co >= 4 or o3 >= 120:
        return 'Sedang'
    else:
        return 'Baik'

# Displaying pollution level classification
st.subheader('Klasifikasi Tingkat Polusi Udara di Dingling')
st.write('Harian: ', dingling_polusi(daily_filtered_data))
st.write('Mingguan: ', dingling_polusi(weekly_filtered_data))
st.write('Bulanan: ', dingling_polusi(monthly_filtered_data))
st.write('Tahunan: ', dingling_polusi(annual_filtered_data))

st.title('Analisis Kualitas Udara di Kota Dingling (2013-2017)')

# Aggregating data for temperature and pressure
def aggregate_data(df, group_by_cols):
    aggregate_df = df.groupby(by=group_by_cols).agg({
        "TEMP": "mean",
        "PRES": "mean",
    }).sort_values(by=group_by_cols, ascending=True).reset_index()

    return aggregate_df.round({
        "TEMP": 0,
        "PRES": 0,
    })

# Daily aggregation
dingling_parameters_harian = aggregate_data(dingling, ['year', 'month', 'day', 'hour'])
dingling_parameters_harian['date_time'] = pd.to_datetime(dingling_parameters_harian[['year', 'month', 'day', 'hour']])
dingling_parameters_harian = dingling_parameters_harian.set_index('date_time').drop(columns=['year', 'month', 'day', 'hour'])

# Weekly aggregation
dingling_parameters_mingguan = aggregate_data(dingling, ['year', 'month', 'day'])
dingling_parameters_mingguan['date_time'] = pd.to_datetime(dingling_parameters_mingguan[['year', 'month', 'day']])
dingling_parameters_mingguan = dingling_parameters_mingguan.set_index('date_time').drop(columns=['year', 'month', 'day'])

# Monthly aggregation
dingling_parameters_bulanan = aggregate_data(dingling, ['year', 'month'])
dingling_parameters_bulanan['date_time'] = pd.to_datetime(dingling_parameters_bulanan[['year', 'month']].assign(day=1))
dingling_parameters_bulanan = dingling_parameters_bulanan.set_index('date_time').drop(columns=['year', 'month'])

# Annual aggregation
dingling_parameters_tahunan = aggregate_data(dingling, ['year'])
dingling_parameters_tahunan['time'] = dingling_parameters_tahunan['year'].astype(str)
dingling_parameters_tahunan = dingling_parameters_tahunan.set_index(pd.to_datetime(dingling_parameters_tahunan['time'] + '-01-01')).drop(columns=['year', 'time'])

# Filtering and displaying data
def filter_and_display_data(df, period, key_suffix):
    start_date = st.date_input(f'Mulai tanggal ({period})', value=pd.to_datetime('2013-03-01'), key=f'start_date_{key_suffix}')
    if start_date is not None:
        if period == 'Harian':
            end_date = start_date + timedelta(days=1)
        elif period == 'Mingguan':
            end_date = start_date + timedelta(days=7)
        elif period == 'Bulanan':
            end_date = start_date + timedelta(days=30)
        elif period == 'Tahunan':
            end_date = start_date + timedelta(days=365)
        st.write(f'Sampai tanggal: {end_date.strftime("%Y-%m-%d")}')
        
        try:
            mask = (df.index >= pd.to_datetime(start_date)) & (df.index < pd.to_datetime(end_date))
            filtered_data = df.loc[mask]
        except Exception as e:
            st.error(f"An error occurred while filtering the data: {e}")
            st.stop()

        st.header(f'Data yang Difilter Berdasarkan Tanggal ({period})')
        st.write(filtered_data)
        return filtered_data

# Display data for different periods
daily_filtered_data = filter_and_display_data(dingling_parameters_harian, 'Harian', 'daily_temp_pres')
weekly_filtered_data = filter_and_display_data(dingling_parameters_mingguan, 'Mingguan', 'weekly_temp_pres')
monthly_filtered_data = filter_and_display_data(dingling_parameters_bulanan, 'Bulanan', 'monthly_temp_pres')
annual_filtered_data = filter_and_display_data(dingling_parameters_tahunan, 'Tahunan', 'annual_temp_pres')

# Visualisasi
def dingling_parameters_graph(df, title):
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(15, 10))

    ax[0].plot(df.index, df['TEMP'], marker='o', linewidth=2, color="#FF4500")
    ax[0].tick_params(axis='y', labelsize=12)
    ax[0].tick_params(axis='x', labelsize=12, labelrotation = 45)
    ax[0].set_ylabel("Temperature (TEMP)", fontsize=15)
    ax[0].set_title("Temperature", loc="center", fontsize=18)

    ax[1].plot(df.index, df['PRES'], marker='o', linewidth=2, color="#1E90FF")
    ax[1].tick_params(axis='y', labelsize=12)
    ax[1].tick_params(axis='x', labelsize=12, labelrotation = 45)
    ax[1].set_ylabel("Pressure (PRES)", fontsize=15)
    ax[1].set_title("Pressure", loc="center", fontsize=18)

    fig.tight_layout(pad=2.0)

    plt.suptitle(title, fontsize=22, y=1.02)
    st.pyplot(fig)

# Display graphs for the filtered data
if daily_filtered_data is not None and not daily_filtered_data.empty:
    st.header("Trend Suhu dan Tekanan Udara Harian")
    dingling_parameters_graph(daily_filtered_data, "Trend Suhu dan Tekanan Udara Harian di Dingling")

if weekly_filtered_data is not None and not weekly_filtered_data.empty:
    st.header("Trend Suhu dan Tekanan Udara Mingguan")
    dingling_parameters_graph(weekly_filtered_data, "Trend Suhu dan Tekanan Udara Mingguan di Dingling")

if monthly_filtered_data is not None and not monthly_filtered_data.empty:
    st.header("Trend Suhu dan Tekanan Udara Bulanan")
    dingling_parameters_graph(monthly_filtered_data, "Trend Suhu dan Tekanan Udara Bulanan di Dingling")

if annual_filtered_data is not None and not annual_filtered_data.empty:
    st.header("Trend Suhu dan Tekanan Udara Tahunan")
    dingling_parameters_graph(annual_filtered_data, "Trend Suhu dan Tekanan Udara Tahunan di Dingling")

# Perhitungan Korelasi Pearson
korelasi_df = dingling[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES']].copy()

# Fungsi untuk menghitung korelasi pearson antara polutan dan suhu
def correlation_suhu(df):
    pm25_suhu = round(df['PM2.5'].corr(df['TEMP'], method="pearson"), 2)
    pm10_suhu = round(df['PM10'].corr(df['TEMP'], method="pearson"), 2)
    SO2_suhu = round(df['SO2'].corr(df['TEMP'], method="pearson"), 2)
    NO2_suhu = round(df['NO2'].corr(df['TEMP'], method="pearson"), 2)
    CO_suhu = round(df['CO'].corr(df['TEMP'], method="pearson"), 2)
    O3_suhu = round(df['O3'].corr(df['TEMP'], method="pearson"), 2)
    correlation_suhu = {
        'parameter': ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"],
        'values': [pm25_suhu, pm10_suhu, SO2_suhu, NO2_suhu, CO_suhu, O3_suhu]
    }
    correlation_suhu_df = pd.DataFrame(correlation_suhu)
    return correlation_suhu_df

# Fungsi untuk menghitung korelasi pearson antara polutan dan tekanan udara
def correlation_pres(df):
    pm25_pres = round(df['PM2.5'].corr(df['PRES'], method="pearson"), 2)
    pm10_pres = round(df['PM10'].corr(df['PRES'], method="pearson"), 2)
    SO2_pres = round(df['SO2'].corr(df['PRES'], method="pearson"), 2)
    NO2_pres = round(df['NO2'].corr(df['PRES'], method="pearson"), 2)
    CO_pres = round(df['CO'].corr(df['PRES'], method="pearson"), 2)
    O3_pres = round(df['O3'].corr(df['PRES'], method="pearson"), 2)
    correlation_pres = {
        'parameter': ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"],
        'values': [pm25_pres, pm10_pres, SO2_pres, NO2_pres, CO_pres, O3_pres]
    }
    correlation_pres_df = pd.DataFrame(correlation_pres)
    return correlation_pres_df

# Hitung korelasi polutan dengan suhu dan tekanan udara
korelasi_suhu = correlation_suhu(korelasi_df)
korelasi_tekanan = correlation_pres(korelasi_df)

# Menampilkan hasil korelasi dalam Streamlit
st.header("Korelasi Polutan dengan Suhu")
st.write(korelasi_suhu)

st.header("Korelasi Polutan dengan Tekanan Udara")
st.write(korelasi_tekanan)

# Visualisasi korelasi dalam bentuk heatmap
st.header("Heatmap Korelasi Polutan")
plt.figure(figsize=(10, 8))
sns.heatmap(korelasi_df.corr(), annot=True, cmap='coolwarm', center=0)
st.pyplot(plt)

dingling['time_span'] = dingling['hour'].apply(lambda x: "Morning" if 6 <= x <= 11 else 
                                              ("Afternoon" if 12 <= x <= 16 else 
                                               ("Evening" if 17 <= x <= 23 else 
                                                "Night")))

# Penggabungan berdasarkan rentang waktu
timespan_particle_df = dingling.groupby(by="time_span").agg({
        "hour": "first",
        "PM2.5": "mean",
        "PM10": "mean"
    }).reset_index()

# Menentukan indeks untuk pengurutan berdasarkan rentang waktu
timespan_particle_df['index'] = timespan_particle_df['hour'].apply(lambda x: 0 if 6 <= x <= 11 else 
                                              (1 if 12 <= x <= 16 else 
                                               (2 if 17 <= x <= 23 else 
                                                3)))

# Mengurutkan DataFrame berdasarkan indeks
timespan_particle_df = timespan_particle_df.sort_values(by='index', ascending=True).reset_index(drop=True)

# Menghapus kolom sementara 'index' dan 'hour'
timespan_particle_df = timespan_particle_df.drop(columns=["index", "hour"])

# Penghitungan arah angin
dingling["wind_direction"] = dingling["wd"]
wind_direction_df = dingling[['wind_direction', 'wd']].copy()
wind_direction_df = wind_direction_df.groupby(by="wind_direction").agg({"wd": "count"}).sort_values(by="wd", ascending=False).reset_index()
wind_direction_df = wind_direction_df.rename(columns={'wd': 'jumlah'})
wind_direction_df['percent'] = round((wind_direction_df['jumlah'] / wind_direction_df['jumlah'].sum()) * 100, 2)

# Streamlit code
st.title('Analisis Data Kualitas Udara Dingling')

# Menampilkan data rentang waktu
st.header('Data Rentang Waktu')
st.write(timespan_particle_df)

# Menampilkan data arah angin
st.header('Data Arah Angin')
st.write(wind_direction_df)

# Menampilkan persentase arah angin
st.header('Persentase Arah Angin')
st.bar_chart(wind_direction_df.set_index('wind_direction')['percent'])

