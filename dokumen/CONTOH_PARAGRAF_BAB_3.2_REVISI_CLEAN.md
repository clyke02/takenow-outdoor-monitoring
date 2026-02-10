# CONTOH PARAGRAF BAB 3.2.x - VERSI REVISI (CLEAN)

## Siap Export ke PDF dan Copy-Paste ke Dokumen Karya Ilmiah

---

## 3.2.1 Analisis Kebutuhan Penyelesaian Sistem Monitoring Peralatan

Berdasarkan hasil analisis proses bisnis dan identifikasi permasalahan pada bab sebelumnya, proses monitoring peralatan yang saat ini dilakukan secara langsung menyebabkan keterbatasan dalam pemantauan kondisi fisik peralatan, frekuensi penggunaan, serta riwayat perawatan secara terintegrasi. Kondisi tersebut berdampak pada rendahnya efisiensi operasional dan kurangnya dukungan informasi bagi pengambilan keputusan manajerial.

**Sistem monitoring yang dibangun dirancang dengan pendekatan multi-level untuk memenuhi kebutuhan pengambilan keputusan di berbagai tingkatan organisasi. Pada level eksekutif, sistem menyediakan Executive Dashboard yang menampilkan Key Performance Indicators (KPI) strategis seperti total alat, average kelayakan, total penyewaan, dan average utilisasi. Dashboard ini dilengkapi dengan health indicators dalam bentuk gauge chart yang memvisualisasikan overall kelayakan, utilization rate, dan equipment health score dalam skala 0-100%. Pada level operasional, Tactical Dashboard menyediakan monitoring real-time dengan fitur interactive filters, critical items alert, dan category performance cards yang memungkinkan petugas operasional mengidentifikasi alat yang memerlukan perhatian segera. Sedangkan untuk level strategis, Strategic Dashboard menyediakan analisis jangka panjang melalui correlation analysis, portfolio distribution, maintenance burden heatmap, dan lifecycle matrix yang mendukung perencanaan investasi dan penggantian aset.**

Sistem monitoring peralatan yang terintegrasi diperlukan untuk mencatat transaksi penyewaan dan pengembalian secara sistematis, serta menyajikan kondisi alat dalam bentuk yang mudah dianalisis. Menurut Sibarani dan Rorimpandey, sistem monitoring aset berbasis web mampu meningkatkan efektivitas pencatatan dan pemantauan inventaris dalam usaha kecil dan menengah [1]. **Oleh karena itu, sistem monitoring yang diusulkan perlu dirancang untuk memenuhi kebutuhan pencatatan data penggunaan, kondisi alat, dan riwayat perawatan secara real-time, serta menyediakan visualisasi data multi-level yang sesuai dengan kebutuhan pengambilan keputusan di berbagai tingkatan organisasi, mulai dari operasional harian hingga perencanaan strategis jangka panjang.**

---

## 3.2.2 Analisis Pendekatan Penyelesaian Sistem Monitoring Peralatan

Pendekatan yang diusulkan untuk menyelesaikan permasalahan monitoring peralatan pada Takenow Outdoor adalah dengan penerapan sistem monitoring berbasis performance dashboard yang memanfaatkan visualisasi data sebagai alat bantu. Dashboard visualisasi data dipilih karena mampu menyajikan informasi secara ringkas dan mudah dipahami, sehingga membantu pemilik usaha dalam memantau kondisi alat tanpa harus menganalisis data mentah secara manual. Penelitian oleh Setiawan dan Suharjo menunjukkan bahwa dashboard dengan notifikasi otomatis efektif dalam pemantauan aset melalui informasi visual yang terintegrasi [2]. Selain itu, Lutfiyah et al. juga menekankan bahwa penggunaan dashboard digital dapat meningkatkan pemahaman pengguna terhadap metrik kinerja operasional secara efektif, terutama dalam kondisi di mana data berasal dari berbagai sumber dan memerlukan agregasi visual [3].

**Dengan demikian, performance dashboard menjadi pendekatan yang relevan untuk menyelesaikan masalah monitoring peralatan di Takenow Outdoor. Dashboard yang dibangun mengadopsi arsitektur modular berbasis Clean Architecture dengan pemisahan layer data (data loading dan processing), business logic (perhitungan kelayakan dan insight), dan presentation (visualisasi chart dan metrics). Implementasi dashboard menggunakan Streamlit sebagai framework web yang memungkinkan interaktivitas tinggi, Pandas untuk data manipulation, dan Plotly untuk interactive charts. Sistem dilengkapi dengan mekanisme caching untuk optimasi performa, lazy loading untuk chart rendering on-demand, dan pagination system untuk menangani dataset besar. Pendekatan ini tidak hanya menyajikan informasi secara visual, namun juga memastikan sistem dapat berskala dan mudah dimaintain seiring bertambahnya volume data dan kompleksitas analisis yang dibutuhkan.**

---

## 3.2.3 Analisis Penyelesaian Monitoring Peralatan

Secara konseptual, sistem monitoring dirancang untuk mengintegrasikan data dari proses penyewaan dan pengembalian peralatan. Setiap penyewaan menghasilkan informasi penggunaan alat yang dapat direkam dan diolah sebagai input untuk perhitungan kondisi alat. Sebaliknya, setiap pengembalian menghasilkan data kondisi fisik alat yang diverifikasi oleh petugas operasional. Data penggunaan dan kondisi tersebut diolah secara terpusat dan ditampilkan melalui performance dashboard.

**Mekanisme monitoring yang diimplementasikan mencakup tiga komponen utama. Pertama, komponen data loading yang menggunakan caching mechanism untuk memuat data katalog barang, riwayat penyewaan, dan riwayat maintenance secara efisien dengan Time-To-Live (TTL) selama 1 jam. Kedua, komponen data processing yang melakukan agregasi dan transformasi data untuk menghasilkan insight kelayakan alat. Proses perhitungan kelayakan alat mempertimbangkan empat faktor utama: umur barang sejak pembelian (degradasi 0.01% per hari, maksimal 20%), frekuensi penyewaan (degradasi 0.5% per sewa, maksimal 30%), total hari sewa (degradasi 0.05% per hari, maksimal 20%), dan riwayat maintenance (degradasi 0.2% per event, maksimal 15%). Dengan pendekatan ini, setiap alat memiliki skor kelayakan dalam range 0-100% yang dihitung secara otomatis dan diperbarui setiap kali data dimuat ulang. Ketiga, komponen visualization yang menyajikan hasil monitoring dalam berbagai format sesuai kebutuhan pengguna, mulai dari gauge chart untuk KPI, pie chart untuk distribusi status, bar chart untuk ranking, scatter plot untuk correlation analysis, box plot untuk portfolio distribution, heatmap untuk maintenance burden, hingga quadrant chart untuk lifecycle matrix.**

Pendekatan seperti ini telah berhasil diterapkan pada sistem monitoring inventaris yang meningkatkan akurasi pencatatan dan visibilitas data inventaris secara keseluruhan [1]. Mekanisme ini memungkinkan sistem memantau aset secara real-time, sekaligus mencatat riwayat pemakaian yang dibutuhkan untuk evaluasi dan perawatan preventif.

---

## 3.2.4 Analisis Penyelesaian Penurunan Kondisi Peralatan

**Permasalahan penurunan kondisi peralatan akibat pemakaian berulang ditangani dengan pendekatan multi-faktor yang lebih komprehensif. Sistem mengimplementasikan formula kelayakan yang mempertimbangkan tidak hanya frekuensi penggunaan, namun juga umur barang, intensitas pemakaian (total hari sewa), dan riwayat maintenance. Setiap alat dimulai dengan kondisi awal 100%, kemudian mengalami degradasi bertahap berdasarkan empat faktor dengan batasan maksimal untuk setiap faktor: degradasi natural dari umur (maksimal 20%), degradasi dari frekuensi sewa (maksimal 30%), degradasi dari intensitas pemakaian (maksimal 20%), dan degradasi dari maintenance events (maksimal 15%). Pendekatan ini memastikan bahwa kelayakan alat mencerminkan kondisi aktual berdasarkan riwayat penggunaan yang lengkap, bukan hanya frekuensi sewa semata.**

**Sistem juga mengimplementasikan mekanisme maintenance ratio yang dihitung sebagai perbandingan jumlah maintenance terhadap frekuensi sewa. Alat dengan maintenance ratio lebih dari 50% dikategorikan sebagai "PERLU PERHATIAN KHUSUS" dan ditampilkan di Critical Items Alert pada Tactical Dashboard. Alat dengan ratio 30-50% dikategorikan sebagai "TINGKATKAN PEMELIHARAAN", sedangkan alat dengan ratio kurang dari 30% dikategorikan sebagai "LAYAK OPERASIONAL". Mekanisme ini memungkinkan identifikasi proaktif terhadap alat yang memiliki beban maintenance tinggi relatif terhadap utilisasinya, sehingga dapat dilakukan tindakan preventif sebelum kondisi semakin memburuk.**

**Lebih lanjut, sistem menyediakan Lifecycle Classification yang mengkategorikan setiap alat ke dalam salah satu dari enam tahap lifecycle: Prime (kondisi optimal), Active (produktif), Underutilized (kurang digunakan), Aging (perlu perhatian), Maintenance Heavy (beban tinggi), dan End of Life (pertimbangkan penggantian). Klasifikasi ini membantu pemilik usaha dalam menyusun strategi maintenance dan replacement yang lebih terstruktur.**

Pendekatan monitoring yang didasarkan pada riwayat penggunaan dan pemeliharaan seperti ini sejalan dengan prinsip preventive maintenance yang dibahas dalam penelitian tentang IoT-based inventory control untuk usaha kecil dan menengah, di mana pemantauan kondisi real-time mampu membantu mencegah kerusakan yang lebih besar serta meningkatkan ketahanan aset secara keseluruhan [4].

---

## 3.2.5 Penyajian Informasi Performance Dashboard

**Informasi hasil monitoring disajikan melalui performance dashboard yang terstruktur dalam lima halaman utama, masing-masing dirancang untuk kebutuhan spesifik level organisasi dan jenis keputusan yang diambil. Executive Dashboard (Overview) menyediakan gambaran menyeluruh dengan Key Performance Indicators meliputi total alat, average kelayakan, total penyewaan, dan average utilisasi, dilengkapi dengan health indicators dalam bentuk gauge chart untuk overall kelayakan, utilization rate, dan equipment health score. Tactical Dashboard menyediakan monitoring operasional real-time dengan interactive filters (kelayakan threshold dan kategori), critical items alert yang otomatis menampilkan alat dengan kelayakan di bawah threshold, key tactical metrics (critical items count, average kelayakan, high maintenance count, underutilized items), category performance cards dengan visual indicators, serta visualisasi top maintenance burden dan top utilization dalam bentuk horizontal bar chart. Strategic Dashboard menyediakan analisis strategis melalui empat tab: Correlation Analysis yang menampilkan scatter plot utilisasi vs kelayakan dengan perhitungan correlation coefficient dan interpretasi otomatis, Portfolio Distribution yang menampilkan box plot distribusi kelayakan per kategori beserta identifikasi best/worst performer, Maintenance Burden yang menampilkan heatmap beban maintenance per kategori dengan color-coded severity, dan Lifecycle Matrix yang menampilkan quadrant chart nilai utilisasi vs beban maintenance dengan empat kuadran strategis (Ideal, Perhatian, Rendah, Kritis) beserta rekomendasi spesifik untuk setiap kuadran.**

**Critical Items page menyediakan fokus khusus pada alat yang memerlukan perhatian segera, dengan fitur threshold-based filtering menggunakan slider, critical items cards yang menampilkan visual indicators dengan kode warna (merah untuk kritis, kuning untuk warning, hijau untuk sehat), metrics detail per item (kelayakan, frekuensi, maintenance), dan rekomendasi spesifik per item. Data Tables page menyediakan akses ke data mentah dalam empat tab (Katalog Barang, Riwayat Penyewaan, Riwayat Maintenance, Insight Kelayakan Alat) dengan pagination system yang dilengkapi navigasi First, Previous, Next, Last, sorting options untuk Insight tab (berdasarkan kelayakan, frekuensi sewa, total hari sewa, atau maintenance), serta format display yang konsisten untuk tanggal (YYYY-MM-DD), persentase, dan angka. Seluruh visualisasi menggunakan Plotly interactive charts yang mendukung zoom, pan, hover tooltips, dan export ke format gambar, sehingga memudahkan pengguna dalam eksplorasi data dan penyajian insight kepada stakeholder lain.**

Menurut penelitian oleh Setiani et al., representasi visual data melalui dashboard membantu mempermudah pemahaman terhadap metrik kinerja dan mendukung pengambilan keputusan berbasis data secara lebih efisien [5]. Dengan demikian, performance dashboard menjadi komponen penting dalam sistem monitoring yang mampu memperkuat mekanisme evaluasi dan pengendalian kondisi peralatan dalam Takenow Outdoor.

---

## 3.2.6 Dampak Penyelesaian Masalah terhadap Operasional

Penerapan sistem monitoring peralatan berbasis performance dashboard diperkirakan akan memberikan dampak positif terhadap operasional Takenow Outdoor. Dengan tersedianya data penggunaan dan kondisi peralatan yang terintegrasi, proses pemantauan menjadi lebih efisien dan akurat.

**Secara spesifik, penerapan sistem ini memberikan dampak terukur pada beberapa aspek operasional. Pertama, efisiensi monitoring meningkat signifikan karena pemilik usaha tidak lagi perlu melakukan penelusuran manual pada beberapa sumber pencatatan terpisah, melainkan dapat mengakses seluruh informasi kondisi peralatan melalui single dashboard dengan navigasi yang intuitif. Tactical Dashboard dengan critical items alert memungkinkan identifikasi proaktif terhadap alat yang memerlukan maintenance, mengurangi risiko equipment failure saat disewakan kepada pelanggan. Kedua, kualitas pengambilan keputusan meningkat melalui visualisasi data multi-level yang sesuai dengan konteks keputusan yang diambil. Executive Dashboard menyediakan KPI strategis untuk evaluasi performa bisnis secara keseluruhan, Tactical Dashboard menyediakan operational metrics untuk decision making harian, dan Strategic Dashboard menyediakan advanced analytics untuk perencanaan jangka panjang seperti investment priority dan replacement strategy. Ketiga, transparansi dan akuntabilitas pengelolaan aset meningkat karena seluruh riwayat penggunaan, maintenance, dan perubahan kondisi alat tercatat secara sistematis dan dapat diakses melalui Data Tables page dengan timestamp yang jelas.**

Selain itu, sistem ini dapat membantu pemilik usaha dalam merencanakan jadwal perawatan atau penggantian alat berdasarkan indikator riwayat penggunaan dan status kondisi yang disajikan, sehingga kualitas layanan kepada pelanggan dapat terjaga. Penelitian yang dilakukan oleh Minasa et al. membuktikan bahwa penerapan sistem monitoring berbasis web memberikan efisiensi dalam pengelolaan inventaris UMKM dan mendukung pengambilan keputusan manajerial berbasis data [6].

**Melalui mekanisme tersebut, Takenow Outdoor dapat meningkatkan efektivitas operasional, ketepatan dalam pengelolaan kondisi peralatan, serta responsivitas terhadap kebutuhan maintenance dan penggantian alat. Sistem monitoring ini juga memberikan fondasi data-driven decision making yang dapat mendukung ekspansi bisnis di masa depan, seperti penambahan kategori alat baru, optimasi inventory level, atau pengembangan strategi pricing yang berbasis pada kondisi dan utilisasi alat.**

---

## TABEL 3.6 - TAMBAHAN KEBUTUHAN FUNGSIONAL

**Tambahkan baris-baris berikut pada Tabel 3.6 (setelah SKPL-F-011):**

| Kode SKPL  | Spesifikasi Kebutuhan Fungsional                                                                                                           |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| SKPL-F-012 | Sistem dapat menampilkan Executive Dashboard dengan KPI strategis dan health indicators dalam bentuk gauge chart                           |
| SKPL-F-013 | Sistem dapat menampilkan Tactical Dashboard dengan interactive filters, critical alerts, dan operational metrics                           |
| SKPL-F-014 | Sistem dapat menampilkan Strategic Dashboard dengan correlation analysis, portfolio distribution, maintenance burden, dan lifecycle matrix |
| SKPL-F-015 | Sistem dapat melakukan filtering dinamis berdasarkan kelayakan threshold dan kategori                                                      |
| SKPL-F-016 | Sistem dapat menghasilkan critical items alert secara otomatis berdasarkan threshold yang ditentukan                                       |
| SKPL-F-017 | Sistem dapat mengklasifikasikan alat ke dalam lifecycle stage (Prime, Active, Underutilized, Aging, Maintenance Heavy, End of Life)        |
| SKPL-F-018 | Sistem dapat menghitung maintenance ratio sebagai perbandingan jumlah maintenance terhadap frekuensi sewa                                  |
| SKPL-F-019 | Sistem dapat mengidentifikasi investment priority berdasarkan utilisasi tinggi dan kelayakan menurun                                       |
| SKPL-F-020 | Sistem dapat menampilkan correlation coefficient antara utilisasi dan kelayakan dengan interpretasi otomatis                               |
| SKPL-F-021 | Sistem dapat menampilkan quadrant chart lifecycle matrix dengan empat kategori strategis                                                   |
| SKPL-F-022 | Sistem dapat melakukan sorting dan pagination pada data tables dengan navigasi lengkap                                                     |
| SKPL-F-023 | Sistem dapat mengimplementasikan caching mechanism untuk optimasi performa loading data                                                    |
| SKPL-F-024 | Sistem dapat melakukan lazy loading pada visualisasi chart untuk meningkatkan responsivitas                                                |

---

## CATATAN PENGGUNAAN

### Cara Menggunakan Dokumen Ini:

1. **Copy paragraf yang sudah bold (tebal)** - Ini adalah bagian yang ditambahkan/direvisi
2. **Paste ke dokumen Word karya ilmiah** Anda pada posisi yang sesuai
3. **Sesuaikan formatting** (font, spacing, dll) agar konsisten dengan dokumen Anda
4. **Review kembali** untuk memastikan flow paragraf tetap natural
5. **Update nomor referensi** [1], [2], [3], dst jika berbeda di dokumen Anda

### Perbedaan dengan Versi Sebelumnya:

- Semua emoji telah dihapus atau diganti dengan teks deskriptif
- Simbol Unicode yang tidak kompatibel dengan LaTeX telah dihilangkan
- Dokumen siap untuk diconvert ke PDF menggunakan pandoc
- Format tetap akademis dan profesional

### Cara Convert ke PDF:

```bash
pandoc CONTOH_PARAGRAF_BAB_3.2_REVISI_CLEAN.md -o bab_3.2.pdf
```

Atau dengan template yang lebih bagus:

```bash
pandoc CONTOH_PARAGRAF_BAB_3.2_REVISI_CLEAN.md -o bab_3.2.pdf --pdf-engine=xelatex -V geometry:margin=2.5cm
```

---

**Versi:** 1.1 (Clean - No Emoji)  
**Tanggal:** 28 Januari 2026  
**Status:** Ready for PDF Export

**Catatan:** Dokumen ini telah dibersihkan dari semua emoji dan karakter Unicode yang tidak kompatibel dengan LaTeX untuk memastikan konversi PDF berjalan lancar.
