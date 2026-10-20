# Informatics Practitioner Lecture Series - Implementasi Studi Kasus (Sesi 1-6)

Kumpulan program Python mandiri untuk enam sesi *Informatics Practitioner Lecture Series*
(Informatika Unib). Tiap file mewakili satu sesi dan berisi satu studi kasus lengkap, dari
pembuatan data simulasi sampai hasil yang bisa dijalankan.

## Sesi 1: Make Sense of Data with Analysis and AI
- **Narasumber:** Andria Arisal (BRIN)
- **Studi kasus:** Analisis risiko piutang dan strategi penanganan kredit
- **Isi:** imputasi nilai hilang dengan median -> analisis deskriptif, diagnostik (diskon vs gagal bayar),
  prediktif (*Logistic Regression*) -> simulasi kebijakan berdasarkan probabilitas gagal bayar.

## Sesi 2: Bridging Global Infrastructure to Address Local Challenges with HPC
- **Narasumber:** Asst. Prof. Dr. Worawan Diaz Carbalo (Thammasat University)
- **Studi kasus:** Penyebaran polusi PM2.5 dengan pemrosesan paralel
- **Isi:** simulasi difusi 2D pada grid; domain dibagi per baris untuk `multiprocessing` dengan teknik *halo*;
  waktu sekuensial vs paralel dibandingkan dan hasilnya diverifikasi identik.
  Speedup bergantung jumlah core mesin Anda.

## Sesi 3: Career and Competition in Industrial Era with GIS
- **Narasumber:** Widi Primadepa (GIS Analyst)
- **Studi kasus:** Pemantauan kondisi aset infrastruktur berbasis lokasi
- **Isi:** jarak *Haversine* ke zona bahaya, skor prioritas inspeksi (usia, kerusakan, jarak),
  ekspor ke `output/aset_infrastruktur.geojson` (bisa dibuka di QGIS atau geojson.io).

## Sesi 4: Introduction to Machine Learning
- **Narasumber:** Dr. Taniza binti Tajuddin (UiTM)
- **Studi kasus:** Prediksi kelayakan pinjaman
- **Isi:** data pemohon simulasi, pembagian 80/20, *Random Forest*, evaluasi (*confusion matrix*,
  precision, recall, F1), dan uji pada pemohon baru lengkap dengan probabilitasnya.

## Sesi 5: Human-Computer Interaction & Data Visualization
- **Narasumber:** Dr. Arafat Febriandirza (BRIN)
- **Studi kasus:** Dashboard pemantauan kinerja sistem
- **Isi:** membuat `output/dashboard.html`: kartu metrik, status optimal/waspada/kritis dengan warna +
  ikon + teks (tidak hanya warna), tombol diagnostik dengan umpan balik langsung.

## Sesi 6: Attributing Direct Drivers to Deforestation Alerts with Satellite Imagery and AI
- **Narasumber:** Dr. Bart Slagter
- **Studi kasus:** Identifikasi penyebab deforestasi dari data satelit
- **Isi:** fitur simulasi (delta NDVI, delta NBR, jarak jalan, luas), label awal berbasis aturan,
  *Random Forest*, laporan klasifikasi, dan klasifikasi peringatan baru.

---

## Catatan
- Semua data **simulasi** untuk belajar konsep dan alur kerja, bukan pengganti analisis lapangan.
- Studi kasus dan kode dirancang dari struktur materi sesi; sesuaikan dengan isi presentasi
  pemateri yang sebenarnya. Nama dan afiliasi narasumber perlu diverifikasi.
- Sesi 6: label dibuat dari aturan sehingga akurasi mendekati 100% adalah hal wajar dan **tidak**
  mencerminkan performa di dunia nyata.
