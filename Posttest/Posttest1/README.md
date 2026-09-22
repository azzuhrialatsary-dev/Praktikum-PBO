# Sistem Pendataan Jadwal Operasional Alat Berat pada Perusahaan Tambang

Program ini dibuat untuk tugas Pemrograman Berorientasi Objek (PBO), menerapkan konsep **Class & Object**, **Atribut & Method**, dan **Encapsulation**.

## Tentang Program

Program ini mencatat data **alat berat**, **operator**, dan **jadwal operasional** di sebuah perusahaan tambang. Setiap jadwal menghubungkan satu alat berat dengan satu operator, lalu menghitung total biaya sewanya.

## Struktur Class

Ada 3 class di dalam program ini:

### 1. `AlatBerat`
Menyimpan data alat berat.
- `kode`, `jenis` → bisa diakses bebas (public)
- `__status` → data tersembunyi (private), hanya bisa diubah lewat `status` (getter/setter). Nilai yang diterima hanya `"Baik"` atau `"Rusak"`.
- `total_alat` → menghitung jumlah alat yang sudah dibuat (atribut kelas).

### 2. `Operator`
Menyimpan data operator.
- `id_operator`, `nama` → bisa diakses bebas (public)
- `__no_sim` → data tersembunyi (private), hanya bisa diubah lewat `no_sim` (getter/setter). Nilai yang diterima harus angka.
- `total_operator` → menghitung jumlah operator yang sudah dibuat (atribut kelas).

### 3. `JadwalOperasional`
Menghubungkan `AlatBerat` dan `Operator` dalam satu jadwal kerja.
- `id_jadwal`, `alat`, `operator` → bisa diakses bebas (public)
- `__durasi_jam` → data tersembunyi (private), hanya bisa diubah lewat `durasi_jam` (getter/setter). Nilai harus lebih dari 0.
- `tarif_per_jam` → tarif sewa per jam, sama untuk semua jadwal (atribut kelas).
- `total_biaya()` → menghitung total biaya = durasi jam × tarif per jam.
- `ubah_tarif()` → mengubah tarif per jam untuk semua jadwal sekaligus.

## Cara Menjalankan

```bash
python3 main.py
```

## Panduan Pengujian

Saat dijalankan, program akan mencetak beberapa bagian secara berurutan:

1. **DATA AWAL** — menampilkan 2 alat, 2 operator, dan 2 jadwal yang baru dibuat.
2. **TOTAL BIAYA & VALIDASI** — menghitung biaya jadwal, mengecek nomor SIM, dan mengubah tarif per jam.
3. **UJI DATA TIDAK VALID** — mencoba mengisi data yang salah (status aneh, SIM huruf, durasi minus). Program akan menolak dan mencetak pesan gagal.
4. **UJI DATA VALID** — mengisi ulang dengan data yang benar. Kali ini data berhasil disimpan.
5. **DATA AKHIR** — menampilkan data setelah perubahan, sebagai bukti hanya data valid yang tersimpan.
6. **REKAP DATA** — menampilkan total alat dan total operator yang terdaftar.