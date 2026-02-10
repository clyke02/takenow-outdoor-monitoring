# 🔐 Login Feature - Panduan Penggunaan

## Overview

Dashboard sekarang dilengkapi dengan fitur **authentication** sederhana untuk memastikan hanya user terotorisasi yang dapat mengakses sistem.

---

## 📋 Credentials Default

**Username:** `admin`  
**Password:** `admin123`

> ⚠️ **Catatan:** Ini adalah demo credentials. Untuk production, gunakan password yang lebih kuat dan implementasi hashing.

---

## 🚀 Cara Menggunakan

### 1. Menjalankan Aplikasi

```bash
streamlit run app.py
```

### 2. Login

- Aplikasi akan otomatis menampilkan **Login Page**
- Masukkan username: `admin`
- Masukkan password: `admin123`
- Klik tombol **Login**

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

Untuk mengubah username/password, edit file `config.py`:

```python
# Authentication settings
USERNAME = "admin"           # Ubah username
PASSWORD = "admin123"        # Ubah password
USER_DISPLAY_NAME = "Administrator"  # Nama display
```

---

## 📊 Fitur Login

### ✅ Yang Sudah Diimplementasi:

1. **Login Page** dengan form username/password
2. **Session Management** menggunakan Streamlit session state
3. **User Info Display** di sidebar
4. **Logout Button** untuk keluar dari sistem
5. **Auto-redirect** ke dashboard setelah login
6. **Validasi credentials** dengan error message

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
> Sistem dilengkapi dengan mekanisme autentikasi untuk memastikan hanya pengguna terotorisasi yang dapat mengakses dashboard. Login page dirancang dengan interface yang sederhana namun profesional, meminta user untuk memasukkan username dan password sebelum dapat mengakses fitur monitoring.
>
> Session management menggunakan Streamlit session state untuk tracking status login user. Ketika user berhasil login, informasi user ditampilkan di sidebar dan user dapat logout kapan saja dengan menekan tombol logout yang tersedia.
>
> Implementasi authentication ini menggunakan single-user model dengan credentials yang tersimpan di file konfigurasi, cocok untuk deployment internal atau demo purposes.

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
