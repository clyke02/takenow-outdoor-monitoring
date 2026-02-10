# Dashboard Kelayakan Alat Camping ⛺

Dashboard interaktif untuk monitoring kondisi dan kelayakan alat camping menggunakan Streamlit dengan arsitektur modular.

## 📁 Struktur Projekt

```
Programm/
├── app.py                          # Main application (with login check)
├── auth.py                         # Authentication module
├── config.py                       # Configuration & constants (with user credentials)
├── requirements.txt                # Python dependencies
├── LOGIN_GUIDE.md                  # Login feature documentation
├── WIREFRAME_LOGIN_PROMPT.md       # Login wireframe prompt
├── dataset/                        # Data files
│   ├── katalog_barang.xlsx
│   ├── riwayat_penyewaan.csv
│   ├── riwayat_maintenance.csv
│   └── insight_kelayakan_alat.csv
└── src/                           # Source modules (clean architecture)
    ├── data/                      # Data layer
    │   ├── loader.py             # Data loading dengan caching
    │   └── processor.py          # Data transformation & agregasi
    ├── visualization/            # Presentation layer
    │   ├── charts.py            # Chart components (Plotly)
    │   └── metrics.py           # Metric displays
    └── utils/                    # Utilities
```

## 🚀 Cara Menjalankan

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Dashboard

```bash
streamlit run app.py
```

Dashboard akan terbuka di browser pada `http://localhost:8501`

### 3. Login

Setelah dashboard terbuka, Anda akan melihat **Login Page**.

**User Accounts:**

**A. Admin/Owner** (Akses: Executive & Planning)
- Username: `owner`
- Password: `owner123`

**B. Admin Operational** (Akses: Operational only)
- Username: `operational`
- Password: `ops123`

Setelah login berhasil, Anda akan diarahkan ke dashboard sesuai role.

> 📖 Untuk detail lengkap tentang fitur login dan RBAC, lihat:
> - [LOGIN_GUIDE.md](LOGIN_GUIDE.md)
> - [RBAC_GUIDE.md](RBAC_GUIDE.md)

## 🔐 Authentication & Authorization

Dashboard dilengkapi dengan **Role-Based Access Control (RBAC)** untuk memastikan setiap user hanya dapat mengakses fitur sesuai role-nya.

**Fitur:**

- ✅ Login page dengan username/password
- ✅ Multi-user support (Owner & Operational)
- ✅ Role-based menu access (different menus for different roles)
- ✅ Session management (tetap login selama sesi browser)
- ✅ User info display dengan role badge di sidebar
- ✅ Access control enforcement (error jika akses unauthorized)
- ✅ Logout button untuk keluar

**Access Levels:**

| Feature | Owner 👔 | Operational 🔧 |
|---------|----------|----------------|
| Executive Dashboard | ✅ | ❌ |
| Tactical Dashboard | ❌ | ✅ |
| Critical Items | ❌ | ✅ |
| Strategic Dashboard | ✅ | ❌ |
| Data Tables | ✅ | ❌ |

**Security Note:**  
Implementasi ini adalah demo authentication untuk keperluan academic/internal. Untuk production, implementasikan password hashing, database user management, dan security best practices lainnya.

## 📊 Fitur Dashboard

### 1. **Overview** 📊

- Key metrics (Total alat, maintenance events, biaya)
- Distribusi status kelayakan alat
- Pie chart rekomendasi
- Bar chart tingkat kerusakan
- Trend penyewaan bulanan

### 2. **Maintenance Analysis** 🔧

- Summary metrics maintenance
- Distribusi severity (Ringan/Sedang/Berat)
- Kondisi alat setelah perbaikan
- Top 10 alat dengan maintenance terbanyak
- Maintenance ratio analysis

### 3. **Rental Analysis** 📈

- Total transaksi dan item disewa
- Revenue per kategori alat
- Chart utilisasi alat
- Detail revenue breakdown

### 4. **Critical Items** ⚠️

- Filter berdasarkan maintenance ratio threshold
- List alat yang memerlukan perhatian khusus
- Rekomendasi actionable untuk setiap item
- Detail metrics per item kritis

### 5. **Data Tables** 📋

- View raw data: Katalog, Penyewaan, Maintenance, Insight
- Pagination untuk performa optimal

## 🏗️ Arsitektur (Clean Architecture)

### Data Layer (`src/data/`)

- **loader.py**: Menghandle loading data dengan Streamlit caching
- **processor.py**: Transformasi, agregasi, dan business logic

### Visualization Layer (`src/visualization/`)

- **charts.py**: Reusable chart components (Plotly)
- **metrics.py**: Reusable metric card components

### Configuration (`config.py`)

- Centralized constants & settings
- Color schemes & styling
- File paths

## ⚡ Optimasi Performa

1. **Caching**: Semua data loading menggunakan `@st.cache_data` dengan TTL 1 jam
2. **Modular**: Setiap komponen independent, load hanya yang dibutuhkan
3. **Lazy Loading**: Charts hanya di-render saat tab/page aktif
4. **Pagination**: Display maksimal 20 rows untuk table besar

## 🎨 Customization

### Ubah Warna

Edit `config.py`:

```python
COLORS = {
    'primary': '#1f77b4',
    'success': '#2ecc71',
    'warning': '#f39c12',
    'danger': '#e74c3c',
}
```

### Ubah Cache TTL

```python
CACHE_TTL = 3600  # seconds
```

### Ubah Max Display Rows

```python
MAX_ROWS_DISPLAY = 20
```

## 📌 Key Insights yang Ditampilkan

1. **Maintenance Ratio**: `jumlah_maintenance / freq_sewa`

   - > 50% = 🔴 PERLU PERHATIAN KHUSUS
   - 30-50% = 🟡 TINGKATKAN PEMELIHARAAN
   - < 30% = 🟢 LAYAK OPERASIONAL

2. **Cost-Benefit Ratio**: `total_revenue / total_biaya_maintenance`

3. **Utilisasi**: Frekuensi sewa & total hari sewa

4. **Severity Distribution**: Ringan / Sedang / Berat

## 🔧 Troubleshooting

**Error: Module not found**

```bash
pip install -r requirements.txt
```

**Error: File not found**

- Pastikan semua file di folder `dataset/` ada
- Check path di `config.py`

**Dashboard lambat**

- Reduce `MAX_ROWS_DISPLAY` di config
- Clear cache: klik "Refresh Data" di sidebar

## 📝 Notes

- Dashboard menggunakan data fiktif untuk demo
- Semua metrik dan rekomendasi di-generate otomatis
- Cocok untuk tugas Sistem Informasi Perusahaan

## 👨‍💻 Tech Stack

- **Streamlit**: Web framework
- **Pandas**: Data manipulation
- **Plotly**: Interactive charts
- **Python 3.11+**

---

**Dibuat dengan Clean Architecture untuk kemudahan maintenance dan scalability** 🚀
