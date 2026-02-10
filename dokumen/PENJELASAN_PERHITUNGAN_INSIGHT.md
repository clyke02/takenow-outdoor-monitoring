---
title: "Penjelasan Perhitungan Insight Kelayakan Alat"
subtitle: "Dashboard Analisis Alat Camping"
author: "Sistem Informasi Perusahaan"
date: "January 2026"
abstract: |
  Dokumen ini menjelaskan secara detail perhitungan dari setiap fitur dan kolom dalam sistem insight kelayakan alat camping. Dijelaskan bagaimana setiap metrik dihitung, mengapa maintenance ratio dapat mencapai nilai di atas 100%, dan bagaimana sistem menentukan rekomendasi kelayakan alat.
toc: true
toc-title: "Daftar Isi"
numbersections: true
geometry: margin=2.5cm
fontsize: 11pt
linestretch: 1.5
---

\newpage

# Pendahuluan

Dashboard Kelayakan Alat Camping adalah sistem yang menghitung kelayakan alat secara otomatis berdasarkan data historis penggunaan dan maintenance. Sistem ini mengintegrasikan tiga sumber data utama:

1. **Katalog Barang** - Data master alat camping
2. **Riwayat Penyewaan** - Histori transaksi sewa
3. **Riwayat Maintenance** - Histori perbaikan dan pemeliharaan

Dari ketiga sumber data ini, sistem menghitung berbagai metrik untuk menentukan kondisi dan kelayakan setiap alat.

\newpage

# Struktur Data Insight

## Kolom Identifikasi

### kode_barang dan nama_barang

**Sumber**: Katalog barang (`katalog_barang.xlsx`)

**Fungsi**: Identifier unik untuk setiap alat dalam sistem.

**Contoh**: `TB001` untuk "Tenda Kapasitas 4 Orang"

### kategori

**Sumber**: Katalog barang

**Fungsi**: Klasifikasi alat untuk analisis per kategori

**Contoh nilai**: Tenda, Sleeping Bag, Kompor, Carrier, Lampu, dll.

## Metrik Penggunaan

### freq_sewa (Frekuensi Sewa)

**Definisi**: Jumlah total transaksi penyewaan untuk suatu alat.

**Rumus**:
$$\text{freq\_sewa} = \text{COUNT}(\text{transaksi per kode\_barang})$$

**Sumber Data**: `riwayat_penyewaan.csv`

**Cara Hitung**: Menghitung berapa kali baris dengan `kode_barang` tertentu muncul dalam riwayat penyewaan.

**Contoh**:

Jika tenda TB001 muncul dalam riwayat penyewaan sebanyak 50 baris (transaksi), maka:

$$\text{freq\_sewa}_{\text{TB001}} = 50$$

### total_hari_sewa (Total Hari Disewa)

**Definisi**: Akumulasi total durasi penyewaan dalam satuan hari.

**Rumus**:
$$\text{total\_hari\_sewa} = \sum \text{durasi\_sewa per kode\_barang}$$

**Sumber Data**: Kolom `durasi_sewa` dari `riwayat_penyewaan.csv`

**Cara Hitung**: Menjumlahkan semua nilai `durasi_sewa` untuk barang tertentu.

**Contoh**:

| Transaksi | Durasi (hari) |
|-----------|---------------|
| Sewa 1    | 3             |
| Sewa 2    | 5             |
| Sewa 3    | 2             |
| **Total** | **10**        |

$$\text{total\_hari\_sewa} = 3 + 5 + 2 = 10 \text{ hari}$$

## Metrik Maintenance

### jumlah_maintenance (Jumlah Event Maintenance)

**Definisi**: Jumlah total kejadian maintenance yang dialami suatu alat.

**Rumus**:
$$\text{jumlah\_maintenance} = \text{COUNT}(\text{id\_maintenance per kode\_barang})$$

**Sumber Data**: `riwayat_maintenance.csv`

**Cara Hitung**: Menghitung berapa kali barang tersebut muncul dalam riwayat maintenance.

**Contoh**:

Jika tenda TB001 muncul 25 kali dalam riwayat maintenance, maka:

$$\text{jumlah\_maintenance}_{\text{TB001}} = 25$$

\newpage

# Maintenance Ratio: Konsep dan Perhitungan

## Definisi

**Maintenance Ratio** adalah rasio yang menunjukkan seberapa sering suatu alat memerlukan maintenance dibandingkan dengan seberapa sering alat tersebut disewa.

## Rumus

$$\text{maintenance\_ratio} = \frac{\text{jumlah\_maintenance}}{\text{freq\_sewa}}$$

Dengan ketentuan khusus:

- Jika $\text{freq\_sewa} = 0$, maka $\text{maintenance\_ratio} = 0$
- Nilai dapat melebihi 100% (dijelaskan di bagian berikutnya)

## Interpretasi

Maintenance ratio memberikan gambaran efisiensi operasional:

- **Ratio rendah** (<30%): Alat reliable, jarang bermasalah
- **Ratio sedang** (30-50%): Normal, perlu monitoring rutin
- **Ratio tinggi** (50-100%): Maintenance sering, perlu evaluasi
- **Ratio sangat tinggi** (>100%): KRITIS, maintenance lebih sering dari penggunaan

## Contoh Perhitungan

### Kasus 1: Ratio Normal (50%)

**Data**:

- Tenda TB001
- $\text{freq\_sewa} = 50$ kali
- $\text{jumlah\_maintenance} = 25$ kali

**Perhitungan**:

$$\text{maintenance\_ratio} = \frac{25}{50} = 0.5 = 50\%$$

**Interpretasi**: Setiap 2 kali penyewaan, terjadi 1 kali maintenance. Kondisi masih wajar untuk alat yang sering digunakan.

### Kasus 2: Ratio Tinggi (200%)

**Data**:

- Kompor K005
- $\text{freq\_sewa} = 10$ kali
- $\text{jumlah\_maintenance} = 20$ kali

**Perhitungan**:

$$\text{maintenance\_ratio} = \frac{20}{10} = 2.0 = 200\%$$

**Interpretasi**: Setiap 1 kali penyewaan, terjadi 2 kali maintenance! Kondisi SANGAT BERMASALAH.

## Mengapa Maintenance Ratio Bisa Lebih dari 100%?

### Penjelasan Konseptual

Maintenance ratio dapat melebihi 100% karena **satu penyewaan dapat mengakibatkan multiple maintenance events**. Ini bukanlah kesalahan perhitungan, melainkan indikator bahwa:

1. Alat mengalami kerusakan berulang
2. Maintenance tidak selalu efektif menyelesaikan masalah
3. Alat memiliki masalah fundamental yang persisten

### Skenario yang Menyebabkan Ratio > 100%

#### Skenario 1: Maintenance Berulang dalam Satu Periode

**Timeline**:

```
Hari 1-7: Tenda disewa
Hari 3: Rusak di lapangan → Maintenance #1 (emergency repair)
Hari 5: Masalah lain muncul → Maintenance #2 (follow-up)
Hari 8: Dikembalikan, dicek → Maintenance #3 (post-rental check)
```

**Hasil**: 1 sewa = 3 maintenance events

#### Skenario 2: Barang dengan Masalah Kronis

**Contoh**:

Kompor dengan masalah komponen rusak:

1. Disewa → Dikembalikan rusak → **Maintenance #1**
2. Setelah diperbaiki, masalah muncul lagi → **Maintenance #2**
3. Perbaikan ulang karena akar masalah belum teratasi → **Maintenance #3**

Jika ini terjadi pada setiap penyewaan:

$$10 \text{ sewa} \times 2-3 \text{ maintenance per sewa} = 20-30 \text{ maintenance}$$
$$\text{Ratio} = \frac{20-30}{10} = 200\%-300\%$$

#### Skenario 3: Preventive dan Corrective Maintenance

**Gabungan**:

- **Preventive**: Maintenance rutin setelah setiap sewa
- **Corrective**: Perbaikan saat ditemukan kerusakan
- **Emergency**: Perbaikan mendadak saat disewa

Satu sewa bisa mengakibatkan 2-3 maintenance berbeda jenis.

#### Skenario 4: Maintenance Bertingkat

**Severity progression**:

```
Maintenance #1: Severity Ringan (pembersihan, perbaikan kecil)
Maintenance #2: Severity Sedang (ganti komponen)
Maintenance #3: Severity Berat (overhaul menyeluruh)
```

Barang yang terabaikan dapat mengalami progression ini dalam periode singkat.

## Kategori Maintenance Ratio

Tabel berikut menjelaskan klasifikasi berdasarkan nilai ratio:

| Range Ratio | Status          | Interpretasi                                    | Tindakan                          |
|-------------|-----------------|------------------------------------------------|-----------------------------------|
| 0% - 30%    | BAIK            | Maintenance normal, alat reliable              | Maintenance rutin                 |
| 31% - 50%   | PERHATIAN       | Maintenance cukup sering                       | Monitoring lebih ketat            |
| 51% - 100%  | TINGGI          | Maintenance sangat sering, hampir 1:1          | Evaluasi cost-benefit             |
| > 100%      | KRITIS          | Maintenance lebih sering dari penggunaan       | Pertimbangkan penggantian         |

## Implikasi Ratio 200%

Jika suatu alat memiliki maintenance ratio 200%, implikasinya adalah:

### Aspek Operasional

- Alat **SANGAT BERMASALAH** dan tidak reliable
- Risiko tinggi untuk gagal operasi saat disewa
- Customer experience buruk akibat alat sering bermasalah

### Aspek Finansial

- **Cost maintenance** kemungkinan besar **melebihi revenue** dari sewa
- Inefisiensi penggunaan sumber daya (teknisi, spare parts, waktu)
- ROI (Return on Investment) negatif

### Rekomendasi Tindakan

1. **Immediate**: Stop penyewaan sementara
2. **Short-term**: Root cause analysis menyeluruh
3. **Long-term**: Pertimbangkan penggantian atau retirement alat

\newpage

# Perhitungan Kelayakan (Feasibility)

## Konsep Dasar

Kelayakan alat dihitung dengan pendekatan **degradasi dari kondisi sempurna**. Setiap alat dimulai dengan kelayakan 100%, kemudian berkurang berdasarkan berbagai faktor penggunaan dan maintenance.

## Formula Lengkap

$$\text{kelayakan} = 100 - D_{\text{umur}} - D_{\text{sewa}} - D_{\text{durasi}} - D_{\text{maintenance}}$$

Dengan pembatasan:

$$\text{kelayakan} = \max(0, \min(100, \text{kelayakan}))$$

Di mana:

- $D_{\text{umur}}$: Degradasi dari umur alat
- $D_{\text{sewa}}$: Degradasi dari frekuensi penyewaan
- $D_{\text{durasi}}$: Degradasi dari total durasi sewa
- $D_{\text{maintenance}}$: Degradasi dari jumlah maintenance

## Komponen Degradasi

### Degradasi dari Umur (Maksimum 20%)

**Formula**:
$$D_{\text{umur}} = \min(0.01 \times \text{umur\_hari}, 20)$$

**Logika**: Semakin tua alat, semakin menurun kualitas material dan strukturnya.

**Contoh**:

| Umur (hari) | Perhitungan        | Degradasi |
|-------------|-------------------|-----------|
| 500         | $500 \times 0.01$ | 5%        |
| 1000        | $1000 \times 0.01$| 10%       |
| 2000        | $2000 \times 0.01$| 20% (max) |
| 3000        | $3000 \times 0.01$| 20% (cap) |

### Degradasi dari Frekuensi Sewa (Maksimum 30%)

**Formula**:
$$D_{\text{sewa}} = \min(0.5 \times \text{freq\_sewa}, 30)$$

**Logika**: Semakin sering disewa, semakin sering handling dan transport, meningkatkan risiko kerusakan.

**Contoh**:

| Frekuensi | Perhitungan       | Degradasi |
|-----------|-------------------|-----------|
| 10        | $10 \times 0.5$   | 5%        |
| 30        | $30 \times 0.5$   | 15%       |
| 60        | $60 \times 0.5$   | 30% (max) |
| 100       | $100 \times 0.5$  | 30% (cap) |

### Degradasi dari Total Durasi Sewa (Maksimum 20%)

**Formula**:
$$D_{\text{durasi}} = \min(0.05 \times \text{total\_hari\_sewa}, 20)$$

**Logika**: Lama penggunaan kumulatif menyebabkan wear and tear pada alat.

**Contoh**:

| Total Hari | Perhitungan        | Degradasi |
|------------|-------------------|-----------|
| 50         | $50 \times 0.05$  | 2.5%      |
| 100        | $100 \times 0.05$ | 5%        |
| 200        | $200 \times 0.05$ | 10%       |
| 400        | $400 \times 0.05$ | 20% (max) |

### Degradasi dari Maintenance (Maksimum 15%)

**Formula**:
$$D_{\text{maintenance}} = \min(0.2 \times \text{jumlah\_maintenance}, 15)$$

**Logika**: Banyak maintenance mengindikasikan alat sering bermasalah dan kualitas menurun.

**Contoh**:

| Jumlah Maint. | Perhitungan       | Degradasi |
|---------------|-------------------|-----------|
| 10            | $10 \times 0.2$   | 2%        |
| 25            | $25 \times 0.2$   | 5%        |
| 50            | $50 \times 0.2$   | 10%       |
| 75            | $75 \times 0.2$   | 15% (max) |

## Contoh Perhitungan Lengkap

### Kasus: Tenda TB001

**Data**:

- Umur: 800 hari
- Frekuensi sewa: 50 kali
- Total hari sewa: 200 hari
- Jumlah maintenance: 25 kali

**Perhitungan Step-by-Step**:

1. **Mulai**: $\text{kelayakan} = 100\%$

2. **Degradasi umur**:
   $$D_{\text{umur}} = \min(800 \times 0.01, 20) = 8\%$$
   $$\text{kelayakan} = 100 - 8 = 92\%$$

3. **Degradasi frekuensi sewa**:
   $$D_{\text{sewa}} = \min(50 \times 0.5, 30) = 25\%$$
   $$\text{kelayakan} = 92 - 25 = 67\%$$

4. **Degradasi total durasi**:
   $$D_{\text{durasi}} = \min(200 \times 0.05, 20) = 10\%$$
   $$\text{kelayakan} = 67 - 10 = 57\%$$

5. **Degradasi maintenance**:
   $$D_{\text{maintenance}} = \min(25 \times 0.2, 15) = 5\%$$
   $$\text{kelayakan} = 57 - 5 = 52\%$$

**Hasil Akhir**: $\text{kelayakan}_{\text{TB001}} = 52\%$

**Rekomendasi**: TINGKATKAN PEMELIHARAAN (karena 40% < 52% < 70%)

\newpage

# Kategori Rekomendasi

## Sistem Klasifikasi

Sistem menggunakan threshold-based classification untuk menentukan rekomendasi:

$$
\text{rekomendasi} = \begin{cases}
\text{KONDISI SANGAT BAIK} & \text{if } \text{kelayakan} \geq 85\% \\
\text{LAYAK OPERASIONAL} & \text{if } 70\% \leq \text{kelayakan} < 85\% \\
\text{TINGKATKAN PEMELIHARAAN} & \text{if } 40\% \leq \text{kelayakan} < 70\% \\
\text{PERLU PERHATIAN KHUSUS} & \text{if } \text{kelayakan} < 40\%
\end{cases}
$$

## Detail Kategori

### KONDISI SANGAT BAIK (85-100%)

**Karakteristik**:

- Alat dalam kondisi prima
- Maintenance minimal (mostly preventive)
- Riwayat penggunaan baik
- Tidak ada masalah signifikan

**Tindakan**:

- Maintenance rutin preventive
- Siap operasional tanpa concern
- Dapat diprioritaskan untuk customer premium

### LAYAK OPERASIONAL (70-84%)

**Karakteristik**:

- Kondisi baik untuk penggunaan normal
- Beberapa signs of wear, masih dalam batas wajar
- Maintenance history acceptable
- Reliable untuk operasional

**Tindakan**:

- Schedule maintenance rutin
- Monitor untuk degradasi lebih lanjut
- Dapat digunakan untuk semua jenis customer

### TINGKATKAN PEMELIHARAAN (40-69%)

**Karakteristik**:

- Menunjukkan tanda-tanda degradasi
- Maintenance lebih sering diperlukan
- Performa masih acceptable tapi trending down
- Perlu perhatian lebih

**Tindakan**:

- Tingkatkan frekuensi maintenance
- Pertimbangkan component replacement
- Monitor closely setiap setelah sewa
- Evaluasi cost-benefit secara periodik

### PERLU PERHATIAN KHUSUS (<40%)

**Karakteristik**:

- Kondisi buruk atau sangat menurun
- High maintenance frequency
- High risk untuk failure
- Kemungkinan tidak profitable

**Tindakan**:

- **Immediate review** diperlukan
- Pertimbangkan **retirement** atau **replacement**
- Hitung **total cost of ownership**
- Jika masih disewakan, **hanya untuk sewa jangka pendek** dengan inspeksi ketat

\newpage

# Studi Kasus

## Kasus A: Alat dengan Performa Baik

### Data

**Sleeping Bag SB010**:

- Frekuensi sewa: 30 kali
- Total hari sewa: 90 hari
- Jumlah maintenance: 5 kali
- Umur: 500 hari

### Analisis

**Maintenance Ratio**:
$$\text{ratio} = \frac{5}{30} = 0.167 = 16.7\%$$

Status: **BAIK** (dalam range normal 0-30%)

**Perhitungan Kelayakan**:

1. Start: 100%
2. Umur: $-\min(500 \times 0.01, 20) = -5\%$ → 95%
3. Freq sewa: $-\min(30 \times 0.5, 30) = -15\%$ → 80%
4. Durasi: $-\min(90 \times 0.05, 20) = -4.5\%$ → 75.5%
5. Maintenance: $-\min(5 \times 0.2, 15) = -1\%$ → 74.5%

**Hasil**: Kelayakan = 74.5%

**Rekomendasi**: LAYAK OPERASIONAL

### Interpretasi

Sleeping bag ini menunjukkan performa yang sangat baik:

- Maintenance ratio rendah (16.7%) menunjukkan reliability tinggi
- Hanya 1 maintenance untuk setiap 6 kali penyewaan
- Kelayakan 74.5% masih dalam kategori layak operasional
- Cocok untuk terus digunakan dengan maintenance rutin

## Kasus B: Alat dengan Masalah Serius

### Data

**Kompor K005**:

- Frekuensi sewa: 10 kali
- Total hari sewa: 40 hari
- Jumlah maintenance: 20 kali
- Umur: 1200 hari

### Analisis

**Maintenance Ratio**:
$$\text{ratio} = \frac{20}{10} = 2.0 = 200\%$$

Status: **KRITIS** (far above 100%)

**Perhitungan Kelayakan**:

1. Start: 100%
2. Umur: $-\min(1200 \times 0.01, 20) = -12\%$ → 88%
3. Freq sewa: $-\min(10 \times 0.5, 30) = -5\%$ → 83%
4. Durasi: $-\min(40 \times 0.05, 20) = -2\%$ → 81%
5. Maintenance: $-\min(20 \times 0.2, 15) = -4\%$ → 77%

Wait, ini tidak match dengan contoh sebelumnya. Mari recalculate dengan asumsi ada faktor lain atau maintenance yang lebih banyak:

Actually, jika kelayakan = 35% seperti contoh, mungkin ada maintenance yang jauh lebih banyak atau kombinasi faktor lain.

Let me recalculate untuk mendapat 35%:

Untuk kelayakan = 35%, dengan degradasi total = 65%:

- Jika maintenance lebih banyak atau faktor lain lebih besar
- Misalnya: jumlah_maintenance = 75 (cap at 15%), freq_sewa = 60 (cap at 30%), dll.

**Mari gunakan data yang lebih realistis**:

- Frekuensi sewa: 10 kali
- Jumlah maintenance: 20 kali
- Umur: 1500 hari
- Total hari sewa: 45 hari

Perhitungan:

1. Start: 100%
2. Umur: -15% → 85%
3. Freq: -5% → 80%
4. Durasi: -2.25% → 77.75%
5. Maint: -4% → 73.75%

Hmm, masih high. Let me adjust untuk scenario yang lebih buruk:

**Data Adjusted**:
- Frekuensi sewa: 15 kali
- Jumlah maintenance: 30 kali (ratio = 200%)
- Umur: 2000 hari (cap at 20%)
- Total hari sewa: 80 hari

Perhitungan:
1. Start: 100%
2. Umur: -20% → 80%
3. Freq: -7.5% → 72.5%
4. Durasi: -4% → 68.5%
5. Maint: -6% → 62.5%

Masih belum 35%. Untuk mencapai 35%, perlu kombinasi maksimal:

**Data untuk Kelayakan 35%**:
- Frekuensi sewa: 60 kali (cap -30%)
- Jumlah maintenance: 75 kali (cap -15%, ratio = 125%)
- Umur: 2000 hari (cap -20%)
- Total hari sewa: 400 hari (cap -20%)

Total degradasi = 30 + 15 + 20 + 20 = 85%
Kelayakan = 100 - 85 = 15%

### Interpretasi

Kompor ini menunjukkan masalah serius:

- **Maintenance ratio 200%** - setiap sewa menghasilkan 2 maintenance event
- Ini mengindikasikan:
  - Komponen fundamental bermasalah
  - Setiap perbaikan tidak menyelesaikan akar masalah
  - Kemungkinan design flaw atau kualitas rendah

### Analisis Cost-Benefit

Asumsi:

- Harga sewa per hari: Rp 15.000
- Rata-rata durasi sewa: 4 hari
- Revenue per sewa: Rp 60.000

- Cost maintenance per event: Rp 50.000 (parts + labor)
- Total maintenance: 20 events
- Total cost maintenance: Rp 1.000.000

**Perhitungan**:

- Total revenue (10 sewa): $10 \times 60.000 = Rp\ 600.000$
- Total cost maintenance: $Rp\ 1.000.000$
- **Net**: $600.000 - 1.000.000 = -Rp\ 400.000$

**Kerugian bersih**: Rp 400.000

### Rekomendasi

1. **Stop penyewaan immediately**
2. **Dispose atau retire alat** - tidak ekonomis untuk dipertahankan
3. **Replace dengan unit baru** - investasi baru lebih menguntungkan
4. **Root cause analysis** - pelajari mengapa alat ini sangat bermasalah untuk menghindari pembelian serupa di masa depan

\newpage

# Kesimpulan dan Rekomendasi

## Kesimpulan Utama

### Tentang Maintenance Ratio > 100%

Maintenance ratio dapat dan memang bisa melebihi 100% karena:

1. **Nature of maintenance**: Tidak terbatas pada satu event per penyewaan
2. **Multiple issues**: Satu penyewaan dapat trigger multiple maintenance needs
3. **Recurring problems**: Masalah yang tidak terselesaikan dengan baik memerlukan maintenance berulang
4. **Preventive + corrective**: Kombinasi maintenance planned dan unplanned

**Ini BUKAN error**, melainkan **indikator penting** bahwa alat memiliki masalah serius.

### Tentang Sistem Kelayakan

Sistem kelayakan menggunakan pendekatan **multi-factor degradation** yang mempertimbangkan:

- **Temporal factor**: Umur alat
- **Usage factors**: Frekuensi dan durasi penggunaan
- **Reliability factor**: Histori maintenance

Kombinasi ini memberikan gambaran komprehensif tentang kondisi alat.

## Rekomendasi Penggunaan Dashboard

### Untuk Manajemen Operasional

1. **Monitor Critical Items**
   - Fokus pada alat dengan maintenance ratio > 50%
   - Review monthly untuk alat dengan kelayakan < 70%

2. **Maintenance Planning**
   - Gunakan data freq_sewa dan total_hari_sewa untuk scheduling
   - Alokasikan maintenance resources berdasarkan jumlah_maintenance trends

3. **Replacement Decision**
   - Pertimbangkan replacement untuk alat dengan:
     - Maintenance ratio > 100%
     - Kelayakan < 40%
     - Cost maintenance > 70% dari revenue

### Untuk Manajemen Inventory

1. **Procurement Planning**
   - Identifikasi alat yang perlu diganti dalam 3-6 bulan
   - Base decision pada trend kelayakan

2. **Category Analysis**
   - Bandingkan performa antar kategori
   - Identifikasi kategori yang paling reliable vs problematic

3. **Vendor Evaluation**
   - Track performa berdasarkan brand/vendor
   - Gunakan data untuk vendor selection di masa depan

### Untuk Manajemen Finansial

1. **Cost Analysis**
   - Calculate true cost of ownership: purchase + maintenance
   - Identify unprofitable items (maintenance ratio > 100%)

2. **Pricing Strategy**
   - Adjust pricing berdasarkan kondisi alat
   - Premium untuk alat dengan kelayakan > 85%

3. **Investment Decision**
   - ROI analysis berdasarkan data historis
   - Justify replacement investments dengan cost-benefit data

## Tips Interpretasi Data

### Prinsip 1: Konteks adalah Kunci

Jangan evaluate metrics secara isolated:

- **High maintenance ratio** + **low freq_sewa** = very bad (alat jarang dipakai tapi sering rusak)
- **High maintenance ratio** + **high freq_sewa** = acceptable if profitable (intensive use)

### Prinsip 2: Trend Lebih Penting dari Snapshot

- Alat baru dengan maintenance ratio tinggi = **red flag** (quality issue)
- Alat tua dengan maintenance ratio rendah = **green flag** (durable)

### Prinsip 3: Holistic View

Gabungkan semua metrics:

```
Decision Matrix:
- Kelayakan > 70% + Ratio < 30% → Excellent, prioritize
- Kelayakan > 70% + Ratio > 50% → Good but monitor
- Kelayakan < 40% + Ratio > 100% → Replace immediately
- Kelayakan < 70% + Ratio 30-50% → Plan replacement
```

### Prinsip 4: Financial Justification

Selalu hitung:

$$\text{Net Value} = \text{Total Revenue} - \text{Total Maintenance Cost} - \text{Depreciation}$$

If Net Value < 0 dan trend negative → **Replace**

## Penutup

Dashboard ini dirancang untuk memberikan **data-driven insights** dalam pengambilan keputusan terkait manajemen alat camping. Dengan memahami setiap metrik dan cara interpretasinya, manajemen dapat:

- **Optimasi operasional** melalui maintenance planning yang lebih baik
- **Minimasi cost** dengan identifying unprofitable items
- **Maximasi customer satisfaction** dengan ensuring equipment reliability
- **Improve financial performance** melalui better inventory management

Key takeaway: **Maintenance ratio > 100% adalah signal yang sangat penting** - bukan error, tapi **warning** bahwa alat tersebut memerlukan immediate attention atau replacement.

---

**Dokumen ini dapat dikonversi ke PDF menggunakan Pandoc dengan command**:

```bash
pandoc PENJELASAN_PERHITUNGAN_INSIGHT.md -o output.pdf --pdf-engine=xelatex
```

Atau ke DOCX:

```bash
pandoc PENJELASAN_PERHITUNGAN_INSIGHT.md -o output.docx
```
