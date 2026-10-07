# Sistem Pendataan Jadwal Operasional Alat Berat pada Perusahaan Tambang

Program ini dibuat untuk tugas Pemrograman Berorientasi Objek (PBO), menerapkan konsep **Class & Object**, **Atribut & Method**, **Encapsulation**, **Relasi UML**, dan **Inheritance**.

## Tentang Program

Program ini mencatat data **alat berat**, **operator**, dan **jadwal operasional** di sebuah perusahaan tambang. Setiap jadwal menghubungkan satu alat berat dengan satu operator, lalu menghitung total biaya sewanya. Tarif tiap alat berbeda sesuai jenisnya (Excavator atau Dump Truck).

## Struktur Class

Ada 7 class di dalam program ini:

### 1. `AlatBerat` (superclass)
Menyimpan data umum semua alat berat.
- `kode`, `jenis` → bisa diakses bebas (public)
- `_status` → data protected, bisa diubah lewat `status` (getter/setter). Nilai yang diterima hanya `"Baik"` atau `"Rusak"`.
- `__harga_perolehan` → data tersembunyi (private), hanya dipakai di dalam `AlatBerat` dan dibaca lewat property `harga_perolehan`.
- `total_alat` → menghitung jumlah alat yang sudah dibuat (atribut kelas).
- `hitung_tarif()` → mengembalikan tarif per jam (akan di-override subclass).

### 2. `Excavator` dan `DumpTruck` (subclass dari `AlatBerat`)
- `Excavator` punya atribut unik `kapasitas_bucket` dan method `gali()`.
- `DumpTruck` punya atribut unik `kapasitas_ton` dan method `angkut()`.

### 3. `CatatanPerawatan`
Menyimpan satu baris riwayat alat (registrasi, pemakaian, perubahan status).

### 4. `Operator`
Menyimpan data operator.
- `id_operator`, `nama` → bisa diakses bebas (public)
- `__no_sim` → data tersembunyi (private), hanya bisa diubah lewat `no_sim` (getter/setter). Nilai yang diterima harus angka.
- `total_operator` → menghitung jumlah operator yang sudah dibuat (atribut kelas).
- `operasikan(alat, jam)` → operator menjalankan alat (ditolak jika alat rusak).

### 5. `Perusahaan`
Menampung daftar alat berat dan operator milik perusahaan.

### 6. `JadwalOperasional`
Menghubungkan `AlatBerat` dan `Operator` dalam satu jadwal kerja.
- `id_jadwal`, `alat`, `operator` → bisa diakses bebas (public)
- `__durasi_jam` → data tersembunyi (private), hanya bisa diubah lewat `durasi_jam` (getter/setter). Nilai harus lebih dari 0.
- `tarif_per_jam` → tarif dasar per jam, sama untuk semua jadwal (atribut kelas).
- `total_biaya()` → menghitung total biaya = durasi jam × tarif alat (hasil `hitung_tarif()` milik alat).
- `ubah_tarif()` → mengubah tarif dasar per jam untuk semua jadwal sekaligus.

## 1. Relasi UML

| Relasi | Kelas | Cara di kode |
|---|---|---|
| Asosiasi | `Operator` menggunakan `AlatBerat` | Alat diterima lewat parameter `operasikan(alat, jam)` |
| Agregasi | `Perusahaan` memiliki `AlatBerat` dan `Operator` | Objek dibuat di luar, lalu dimasukkan ke list |
| Komposisi | `AlatBerat` terdiri dari `CatatanPerawatan` | Catatan dibuat di dalam `AlatBerat` lewat `_buat_catatan()` |

## 2. Inheritance

| Syarat | Penerapan |
|---|---|
| Superclass dan subclass | `AlatBerat` (superclass), `Excavator` dan `DumpTruck` (subclass) |
| `super().__init__(...)` | Dipanggil di konstruktor `Excavator` dan `DumpTruck` |
| Atribut unik | `Excavator.kapasitas_bucket`, `DumpTruck.kapasitas_ton` |
| Method overriding | `hitung_tarif()` dan `info()` di-override di kedua subclass |
| Protected (`_`) | `_status` di `AlatBerat`, dibaca langsung oleh `Excavator.gali()` dan `DumpTruck.angkut()` |
| Private (`__`) | `__harga_perolehan`, hanya dipakai di dalam `AlatBerat` |

### Contoh overriding

Tarif dasar Rp 150.000/jam, tiap subclass menghitung tarifnya sendiri:

| Alat | Rumus | Hasil |
|---|---|---|
| Excavator (bucket 1,5 m³) | tarif dasar + bucket x 25.000 | Rp 187.500/jam |
| Dump Truck (10 ton) | tarif dasar + ton x 5.000 | Rp 200.000/jam |

## Cara Menjalankan

```bash
python main.py
```

## Panduan Pengujian

Saat dijalankan, program akan mencetak beberapa bagian secara berurutan:

1. **DATA AWAL** — menampilkan 2 alat (Excavator dan Dump Truck) dan 2 operator yang baru dibuat.
2. **AGREGASI** — menampilkan alat dan operator yang dimiliki perusahaan.
3. **ASOSIASI** — operator menjalankan alat; alat juga mencoba menggali dan mengangkut muatan.
4. **METHOD OVERRIDING** — menampilkan tarif tiap alat dan total biaya jadwal, lalu mengubah tarif dasar.
5. **UJI DATA TIDAK VALID** — mencoba mengisi data yang salah (status aneh, SIM huruf, durasi minus). Program akan menolak dan mencetak pesan gagal.
6. **UJI DATA VALID** — mengisi ulang dengan data yang benar. Kali ini data berhasil disimpan.
7. **ALAT RUSAK TIDAK BISA DIPAKAI** — alat berstatus "Rusak" ditolak saat dioperasikan.
8. **DATA AKHIR** — menampilkan data setelah perubahan, sebagai bukti hanya data valid yang tersimpan.
9. **KOMPOSISI** — menampilkan riwayat perawatan tiap alat.
10. **PRIVATE vs PROTECTED** — membuktikan atribut private tidak bisa diakses langsung.
11. **CEK RELASI PEWARISAN** — menguji `isinstance` dan `issubclass`.
12. **REKAP DATA** — menampilkan total alat dan total operator yang terdaftar.
