# 🔐 Login Feature - Panduan Penggunaan

## Overview

Dashboard sekarang dilengkapi dengan fitur **authentication** sederhana untuk memastikan hanya user terotorisasi yang dapat mengakses sistem.

---

## 📋 User Accounts & Access Levels

### **User 1: Admin/Owner** 👔
- **Username:** `owner`
- **Password:** `owner123`
- **Role:** Owner
- **Access:**
  - ✅ EXECUTIVE (Overview)
  - ✅ PLANNING (Strategic Dashboard, Data Tables)
  - ❌ OPERATIONAL (tidak bisa akses)

### **User 2: Admin Operational** 🔧
- **Username:** `operational`
- **Password:** `ops123`
- **Role:** Operational
- **Access:**
  - ✅ OPERATIONAL (Tactical Dashboard, Critical Items)
  - ❌ EXECUTIVE (tidak bisa akses)
  - ❌ PLANNING (tidak bisa akses)

> ⚠️ **Catatan:** Ini adalah demo credentials. Untuk production, gunakan password yang lebih kuat dan implementasi hashing.

---

## 🚀 Cara Menggunakan

### 1. Menjalankan Aplikasi

```bash
streamlit run app.py
```

### 2. Login

- Aplikasi akan otomatis menampilkan **Login Page**

**Pilih salah satu user:**

**A. Login sebagai Owner:**
- Masukkan username: `owner`
- Masukkan password: `owner123`
- Klik tombol **Login**
- Anda akan melihat menu EXECUTIVE dan PLANNING

**B. Login sebagai Operational:**
- Masukkan username: `operational`
- Masukkan password: `ops123`
- Klik tombol **Login**
- Anda akan melihat menu OPERATIONAL saja

### 3. Akses Dashboard

- Setelah login berhasil, Anda akan diarahkan ke **Executive Dashboard**
- User info akan muncul di **sidebar atas**
- Navigasi normal dapat digunakan

### 4. Logout

- Klik tombol **Logout** di sidebar atas
- Anda akan kembali ke Login Page
- Session akan di-clear

---

## 📁 File Structure

```
Programm/
├── app.py              # Main dashboard (modified)
├── auth.py             # NEW: Authentication logic
├── config.py           # Updated: User credentials
├── LOGIN_GUIDE.md      # Dokumentasi login
└── ...
```

---

## 🔧 Modifikasi Credentials

Untuk mengubah username/password atau menambah user, edit file `config.py`:

```python
# Authentication settings
USERS = {
    "owner": {
        "password": "owner123",        # Ubah password owner
        "display_name": "Admin Owner", # Ubah display name
        "role": "owner",
        "description": "Full access to Executive and Planning"
    },
    "operational": {
        "password": "ops123",          # Ubah password operational
        "display_name": "Admin Operational",
        "role": "operational",
        "description": "Access to Operational only"
    },
    # Tambah user baru di sini jika perlu
}

# Role-based menu access
ROLE_PERMISSIONS = {
    "owner": {
        "executive": True,
        "operational": False,
        "planning": True
    },
    "operational": {
        "executive": False,
        "operational": True,
        "planning": False
    }
}
```

---

## 📊 Fitur Login

### ✅ Yang Sudah Diimplementasi:

1. **Login Page** dengan form username/password
2. **Multi-User Support** dengan 2 user (Owner & Operational)
3. **Role-Based Access Control (RBAC)** - setiap user punya akses berbeda
4. **Session Management** menggunakan Streamlit session state
5. **User Info Display** di sidebar dengan role badge
6. **Logout Button** untuk keluar dari sistem
7. **Auto-redirect** ke dashboard setelah login
8. **Validasi credentials** dengan error message
9. **Access Control** - error jika mencoba akses menu yang tidak diizinkan

### 🔒 Security Note:

Implementasi ini adalah **demo authentication** untuk keperluan skripsi/academic. Untuk production:

- ✅ Gunakan password hashing (bcrypt, argon2)
- ✅ Implementasi HTTPS
- ✅ Session timeout
- ✅ Rate limiting untuk prevent brute force
- ✅ Database untuk user management
- ✅ Role-based access control (RBAC)

---

## 🎯 Untuk Karya Ilmiah

### Tambahan di Bab 3.2.x:

> **3.2.X Authentication & Authorization**
> 
> Sistem dilengkapi dengan mekanisme autentikasi dan otorisasi berbasis peran (Role-Based Access Control/RBAC) untuk memastikan hanya pengguna terotorisasi yang dapat mengakses dashboard sesuai dengan hak aksesnya. Login page dirancang dengan interface yang sederhana namun profesional, meminta user untuk memasukkan username dan password sebelum dapat mengakses fitur monitoring.
> 
> **Implementasi Multi-User:**
> 
> Sistem mendukung dua jenis pengguna dengan hak akses yang berbeda:
> 
> 1. **Admin/Owner**: Memiliki akses penuh ke menu Executive Dashboard (untuk monitoring high-level KPIs) dan Planning Dashboard (untuk analisis strategis dan data tables). User ini tidak dapat mengakses menu Operational karena fokusnya pada keputusan strategis dan perencanaan jangka panjang.
> 
> 2. **Admin Operational**: Memiliki akses eksklusif ke menu Operational Dashboard (Tactical Dashboard dan Critical Items) untuk monitoring operasional harian dan penanganan item kritis. User ini tidak dapat mengakses menu Executive dan Planning karena fokusnya pada operasional teknis.
> 
> **Session Management:**
> 
> Session management menggunakan Streamlit session state untuk tracking status login user, termasuk username, display name, dan role. Ketika user berhasil login, sistem akan menyimpan informasi user dan menampilkannya di sidebar dengan badge role yang sesuai. User dapat logout kapan saja dengan menekan tombol logout yang tersedia, yang akan menghapus semua data session dan mengarahkan kembali ke login page.
> 
> **Access Control:**
> 
> Setiap halaman dashboard dilindungi dengan pemeriksaan hak akses. Jika user mencoba mengakses halaman yang tidak diizinkan untuk role-nya, sistem akan menampilkan pesan "Access Denied" dan mencegah akses ke halaman tersebut. Sidebar navigation juga hanya menampilkan menu yang sesuai dengan hak akses user, sehingga meningkatkan user experience dan keamanan sistem.
> 
> Implementasi RBAC ini cocok untuk organisasi yang memiliki pemisahan tugas (separation of duties) antara level manajerial/strategis dan operasional, memastikan setiap user hanya dapat mengakses informasi dan fitur yang relevan dengan tanggung jawabnya.

### Screenshot yang Perlu Ditambahkan:

1. **Login Page** - Tampilan awal sebelum login
2. **Login Error** - Tampilan ketika credentials salah
3. **Dashboard dengan User Info** - Sidebar menampilkan logged user
4. **Logout Confirmation** - Kembali ke login page

---

## 🐛 Troubleshooting

### Login tidak berhasil

- Pastikan username: `admin` (case-sensitive)
- Pastikan password: `admin123` (case-sensitive)
- Clear browser cache dan reload page

### Session hilang

- Streamlit akan reset session jika:
  - Browser di-refresh (F5)
  - File code di-edit (auto-reload)
  - Server di-restart
- Solusi: Login kembali

### User info tidak muncul

- Pastikan `auth.py` sudah dibuat dengan benar
- Cek import di `app.py` sudah ada `from auth import ...`
- Restart Streamlit server

---

## 📞 Support

Untuk pertanyaan lebih lanjut, silakan hubungi developer atau lihat dokumentasi Streamlit:
https://docs.streamlit.io/

---

**© 2026 - Dashboard Kelayakan Alat Camping**
