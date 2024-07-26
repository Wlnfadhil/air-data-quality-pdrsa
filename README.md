# air-data-quality-pdrsa
# air-data-quality-pdrsa
## Analisis Suhu dan Tekanan Udara di Dingling

Proyek ini menganalisis tren perubahan suhu dan tekanan udara di Dingling dengan menggunakan dataset historis. Kami memvisualisasikan data dalam beberapa interval waktu dan menghitung rata-rata untuk memberikan wawasan yang lebih dalam tentang pola cuaca di area tersebut.

### Struktur Proyek

- **Dataset**: Data yang digunakan dalam proyek ini mencakup informasi suhu dan tekanan udara dari berbagai periode waktu.
- **Visualisasi**: Grafik yang menampilkan tren perubahan suhu dan tekanan udara.
- **Analisis**: Menghitung rata-rata suhu dan tekanan udara untuk periode waktu tertentu.

### Instalasi

1. **Clone repository ini**:
    ```bash
    git clone https://github.com/username/repository.git
    cd repository
    ```

2. **Buat lingkungan virtual dan aktifkan**:
    ```bash
    python -m venv env
    source env/bin/activate   # Pada Windows, gunakan `env\Scripts\activate`
    ```

3. **Instal dependensi**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Jalankan aplikasi Streamlit**:
    ```bash
    streamlit run app.py
    ```

## Penggunaan

### Data

Data diambil dari berbagai periode waktu dan dianalisis sebagai berikut:

- **Harian**: Suhu dan tekanan udara selama 23 jam pada tanggal 2013-03-01 pukul 00.00-19.00.
- **Mingguan**: Suhu dan tekanan udara selama 21 hari pada tanggal 2014-09-01 sampai 2014-09-21.
- **Bulanan**: Suhu dan tekanan udara selama 11 bulan pada tanggal 2016-01 sampai 2016-11.
- **Tahunan**: Suhu dan tekanan udara selama 5 tahun dari 2013 sampai 2017.

### Visualisasi

Grafik menunjukkan tren perubahan suhu dan tekanan udara dalam interval waktu yang berbeda. Grafik ini dapat dilihat dalam aplikasi Streamlit setelah menjalankan perintah `streamlit run app.py`.

### Analisis

Rata-rata suhu dan tekanan udara dihitung untuk setiap periode dan ditampilkan bersama grafik.

### Contoh Kode

#### Visualisasi Grafik

```python
def air_parameters_graph(df, title):
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))

    ax[0].plot(df.index, df['TEMP'], marker='o', linewidth=2, color="#39064B")
    ax[0].tick_params(axis='y', labelsize=20)
    ax[0].tick_params(axis='x', labelsize=20, labelrotation = 45)
    ax[0].set_ylabel("Suhu (°C)", fontsize=25)
    ax[0].set_title("Suhu", loc="center", fontsize=35)

    ax[1].plot(df.index, df['PRES'], marker='o', linewidth=2, color="#39064B")
    ax[1].tick_params(axis='y', labelsize=20)
    ax[1].tick_params(axis='x', labelsize=20, labelrotation = 45)
    ax[1].set_ylabel("Tekanan (hPa)", fontsize=25)
    ax[1].set_title("Tekanan", loc="center", fontsize=35)

    fig.tight_layout(pad=2.0)

    plt.suptitle(title, fontsize=45, y=1.05)
    st.pyplot(fig)
