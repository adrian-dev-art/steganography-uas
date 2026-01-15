# LAPORAN INVESTIGASI: ANALISIS STEGANOGRAFI PADA FILE SUSPECT
**ID Kasus:** UAS-STEGANO-2026
**Objek:** `Picture_UAS_Steganografi.jpg`

---

## 1. RINGKASAN EKSEKUTIF
Investigasi ini bertujuan untuk memverifikasi keberadaan data tersembunyi pada file `Picture_UAS_Steganografi.jpg`. Melalui serangkaian pengujian struktural, statistik, dan visual, file tersebut dibandingkan dengan referensi bersih (Baseline) dan sampel steganografi aktif (Steghide & OpenStego).

## 2. DETAIL BARANG BUKTI
| Atribut | Nilai |
| :--- | :--- |
| **Nama File** | `Picture_UAS_Steganografi.jpg` |
| **Ukuran** | 90,453 Bytes |
| **MD5 Hash** | `85a9c9d86e0f48740ee56696c97f1371` |
| **Status** | Suspect |

## 3. HASIL INVESTIGASI (DFF)

### 3.1 Analisis Struktur (EOI)
Mengecek apakah ada data yang ditempel setelah marker End of Image (`FF D9`).
- **Hasil:** 1 Marker ditemukan.
- **Kesimpulan:** Tidak ada data tambahan di akhir file.

### 3.2 Analisis Statistik LSB
Menghitung rata-rata bit terakhir pada setiap channel warna.
- **Suspect:** `R: 0.494881, G: 0.495346, B: 0.498152`
- **Clean:** `R: 0.494881, G: 0.495346, B: 0.498152`
- **Hasil:** Identik 100% dengan file bersih.

### 3.3 Advanced Steganalysis (Chi-Square)
Menguji keacakan distribusi bit LSB.
- **Suspect P-Value:** `0.379700` (Pola Alami)
- **Steghide P-Value:** `0.383922` (Pola Terkompresi/Sengaja)

### 3.4 Analisis Visual (LSB Plane)
Membandingkan perbedaan bit plane LSB secara visual menggunakan teknik *Red Rectangle Marking*.

| Perbandingan | Blok Berbeda | Status |
| :--- | :---: | :--- |
| **Suspect vs Clean** | **0** | **IDENTIK** |
| **Suspect vs Steghide** | 500 | Anomali |

#### Bukti Visual (Suspect vs Clean):
![Suspect vs Clean](diff_suspect_vs_clean.png)
*(Gambar di atas menunjukkan tidak adanya kotak merah, membuktikan integritas data pixel yang sempurna)*

## 4. ANALISIS METADATA
Ditemukan perbedaan 36 byte antara Suspect dan Clean. Investigasi mendalam pada header menunjukkan adanya tag EXIF `Orientation: 1` pada file Suspect yang tidak ada pada file Clean (hasil WhatsApp). Hal ini merupakan informasi metadata standar dan bukan merupakan media penyisipan pesan rahasia.

## 5. KESIMPULAN AKHIR
Berdasarkan bukti-bukti teknis di atas, tim investigator menyimpulkan bahwa file **`Picture_UAS_Steganografi.jpg`** adalah **BERSIH (CLEAN)** dari segala bentuk steganografi yang diuji.

---
**Investigator:** Adrian
**Tanggal:** 15 Januari 2026
