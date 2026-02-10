---
title: "Flowchart Sistem Dashboard Kelayakan Alat"
subtitle: "Alur Sistem"
author: "Sistem Informasi Perusahaan"
date: "January 2026"
geometry: margin=2cm
fontsize: 12pt
---

\newpage

# Flowchart Sistem

![Flowchart](flowchart-diagram.png)

## Diagram Alur

```
                            [START]
                               |
                               v
                    +------------------------+
                    |  Load Data dari File   |
                    |  - katalog_barang.xlsx |
                    |  - riwayat_penyewaan   |
                    |  - riwayat_maintenance |
                    +----------+-------------+
                               |
                               v
                      /-------------------\
                      | Data berhasil?    |
                      \---------+---------/
                           YES  |  NO
                               |   |
                               |   +---> [Error & Stop] --> [END]
                               |
                               v
                  +----------------------------+
                  | Agregasi Data Penyewaan    |
                  | - freq_sewa                |
                  | - total_hari_sewa          |
                  +------------+---------------+
                               |
                               v
                  +----------------------------+
                  | Agregasi Data Maintenance  |
                  | - jumlah_maintenance       |
                  +------------+---------------+
                               |
                               v
                  +----------------------------+
                  | Hitung Kelayakan (0-100%)  |
                  | - Degradasi umur           |
                  | - Degradasi freq_sewa      |
                  | - Degradasi durasi         |
                  | - Degradasi maintenance    |
                  +------------+---------------+
                               |
                               v
                  +----------------------------+
                  | Hitung Maintenance Ratio   |
                  | ratio = maint / sewa       |
                  +------------+---------------+
                               |
                               v
                  +----------------------------+
                  | Tentukan Rekomendasi       |
                  | >= 85%: Sangat Baik        |
                  | >= 70%: Layak              |
                  | >= 40%: Tingkatkan         |
                  | < 40%: Perlu Perhatian     |
                  +------------+---------------+
                               |
                               v
                  +----------------------------+
                  | Tampilkan Dashboard        |
                  | - Metrics                  |
                  | - Charts                   |
                  | - Tables                   |
                  +------------+---------------+
                               |
                               v
                       /--------------\
                       | Pilih Menu?  |
                       \------+-------/
                              |
                +-------------+-------------+
                |             |             |
                v             v             v
          [Overview]    [Critical]     [Refresh]
                |             |             |
                |             |             |
                +-------------+-------------+
                              |
                              v
                        /----------\
                        | Exit?    |
                        \----+-----/
                         YES | NO
                             |  |
                             |  +---> (Loop back)
                             v
                          [END]
```

\newpage

# Penjelasan Singkat

## Alur Utama

1. **START** → Sistem dimulai
2. **Load Data** → Baca 3 file data (katalog, penyewaan, maintenance)
3. **Validasi** → Cek apakah data berhasil dimuat
4. **Agregasi** → Hitung frekuensi sewa dan total maintenance per alat
5. **Perhitungan Kelayakan** → Hitung degradasi dari berbagai faktor
6. **Hitung Ratio** → maintenance_ratio = jumlah_maintenance / freq_sewa
7. **Rekomendasi** → Tentukan status berdasarkan kelayakan
8. **Display** → Tampilkan dashboard ke user
9. **Interaction** → User memilih menu/action
10. **Loop/End** → Kembali ke interaction atau keluar

## Decision Points

- **Data berhasil dimuat?** → Jika NO, stop. Jika YES, lanjut.
- **Pilih Menu** → Overview, Critical Items, Refresh, atau Exit
- **Exit?** → Jika YES, END. Jika NO, loop kembali.

## Formula Kunci

**Maintenance Ratio**:
$$\text{maintenance\_ratio} = \frac{\text{jumlah\_maintenance}}{\text{freq\_sewa}}$$

**Kelayakan** (mulai dari 100%, lalu dikurangi):
$$\text{kelayakan} = 100 - \sum \text{degradasi}$$

Di mana degradasi meliputi:
- Umur barang (max -20%)
- Frekuensi sewa (max -30%)
- Total hari sewa (max -20%)
- Jumlah maintenance (max -15%)

---

**Konversi ke PDF**:
```bash
pandoc ALUR_SISTEM.md -o Alur_Sistem.pdf --pdf-engine=xelatex
```
