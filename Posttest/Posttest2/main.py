def rp(angka):
    """Format angka menjadi Rupiah, contoh: Rp 1.200.000"""
    return f"Rp {angka:,}".replace(",", ".")

class CatatanPerawatan:

    def __init__(self, id_catatan, tipe, keterangan):
        self.id_catatan = id_catatan
        self.tipe = tipe
        self.keterangan = keterangan

    def __str__(self):
        return f"[{self.id_catatan}] {self.tipe:<10} | {self.keterangan}"

class AlatBerat:

    total_alat = 0

    def __init__(self, kode, jenis, status, harga_perolehan):
        self.kode = kode
        self.jenis = jenis
        self._status = status
        self._total_jam_pakai = 0
        self._riwayat = []
        self.__harga_perolehan = harga_perolehan

        AlatBerat.total_alat += 1
        self._buat_catatan("REGISTRASI", f"Alat terdaftar dengan status {status}")

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status_baru):
        if self.validasi_status(status_baru):
            status_lama = self._status
            self._status = status_baru
            self._buat_catatan("STATUS", f"{status_lama} -> {status_baru}")
        else:
            print(f"[GAGAL] Status '{status_baru}' tidak valid. Harus 'Baik' atau 'Rusak'.")

    @property
    def total_jam_pakai(self):
        return self._total_jam_pakai

    @property
    def harga_perolehan(self):
        return self.__harga_perolehan

    @staticmethod
    def validasi_status(status):
        return status in ["Baik", "Rusak"]

    def _buat_catatan(self, tipe, keterangan):
        id_baru = f"LOG-{len(self._riwayat) + 1:03d}"
        self._riwayat.append(CatatanPerawatan(id_baru, tipe, keterangan))

    def tampilkan_riwayat(self):
        print(f"Riwayat {self.kode} ({self.jenis}):")
        for catatan in self._riwayat:
            print(f"  {catatan}")

    def catat_pemakaian(self, jam):
        if jam > 0:
            self._total_jam_pakai += jam
            self._buat_catatan("PEMAKAIAN", f"Dipakai selama {jam} jam")

    def nilai_sekarang(self):
        penyusutan = self._total_jam_pakai * 10000
        return max(self.__harga_perolehan - penyusutan, 0)

    def hitung_tarif(self, tarif_dasar):
        """Tarif per jam alat. Akan di-override oleh subclass."""
        return tarif_dasar

    def info(self):
        print(f"{self.kode} - {self.jenis} | Status: {self._status} | "
            f"Jam pakai: {self._total_jam_pakai} jam")

class Excavator(AlatBerat):

    def __init__(self, kode, status, harga_perolehan, kapasitas_bucket):
        super().__init__(kode, "Excavator", status, harga_perolehan)
        self.kapasitas_bucket = kapasitas_bucket

    def hitung_tarif(self, tarif_dasar):
        return tarif_dasar + int(self.kapasitas_bucket * 25000)

    def info(self):
        super().info()
        print(f"   Kapasitas bucket: {self.kapasitas_bucket} m3")

    def gali(self, volume):
        if self._status != "Baik":
            print(f"[GAGAL] {self.kode} rusak, tidak bisa menggali.")
            return
        print(f"{self.kode} menggali tanah sebanyak {volume} m3.")

class DumpTruck(AlatBerat):

    def __init__(self, kode, status, harga_perolehan, kapasitas_ton):
        super().__init__(kode, "Dump Truck", status, harga_perolehan)
        self.kapasitas_ton = kapasitas_ton

    def hitung_tarif(self, tarif_dasar):
        return tarif_dasar + self.kapasitas_ton * 5000

    def info(self):
        super().info()
        print(f"   Kapasitas muatan: {self.kapasitas_ton} ton")

    def angkut(self, ton):
        if self._status != "Baik":
            print(f"[GAGAL] {self.kode} rusak, tidak bisa mengangkut.")
        elif ton > self.kapasitas_ton:
            print(f"[GAGAL] Muatan {ton} ton melebihi kapasitas {self.kapasitas_ton} ton.")
        else:
            print(f"{self.kode} mengangkut muatan {ton} ton.")

class Operator:

    total_operator = 0

    def __init__(self, id_operator, nama, no_sim):
        self.id_operator = id_operator
        self.nama = nama
        self.__no_sim = no_sim

        Operator.total_operator += 1

    @property
    def no_sim(self):
        return self.__no_sim

    @no_sim.setter
    def no_sim(self, no_sim_baru):
        if self.validasi_no_sim(no_sim_baru):
            self.__no_sim = no_sim_baru
        else:
            print(f"[GAGAL] Nomor SIM '{no_sim_baru}' tidak valid. Harus berupa angka.")

    @staticmethod
    def validasi_no_sim(no_sim):
        return str(no_sim).isdigit()

    def operasikan(self, alat, jam):
        if alat.status != "Baik":
            print(f"[GAGAL] {self.nama} tidak bisa mengoperasikan {alat.kode}, alat rusak.")
            return False
        alat.catat_pemakaian(jam)
        print(f"{self.nama} mengoperasikan {alat.jenis} {alat.kode} selama {jam} jam.")
        return True

class Perusahaan:

    def __init__(self, nama):
        self.nama = nama
        self._daftar_alat = []
        self._daftar_operator = []

    def tambah_alat(self, alat):
        self._daftar_alat.append(alat)

    def tambah_operator(self, operator):
        self._daftar_operator.append(operator)

    def tampilkan_aset(self):
        print(f"Perusahaan: {self.nama}")
        print(f"  Alat berat ({len(self._daftar_alat)}):")
        for alat in self._daftar_alat:
            print(f"    - {alat.kode} {alat.jenis} ({alat.status})")
        print(f"  Operator ({len(self._daftar_operator)}):")
        for op in self._daftar_operator:
            print(f"    - {op.id_operator} {op.nama}")

class JadwalOperasional:

    tarif_per_jam = 150000

    def __init__(self, id_jadwal, alat, operator, durasi_jam):
        self.id_jadwal = id_jadwal
        self.alat = alat
        self.operator = operator
        self.__durasi_jam = durasi_jam

    @property
    def durasi_jam(self):
        return self.__durasi_jam

    @durasi_jam.setter
    def durasi_jam(self, durasi_baru):
        if durasi_baru > 0:
            self.__durasi_jam = durasi_baru
        else:
            print(f"[GAGAL] Durasi jam '{durasi_baru}' tidak valid. Harus lebih dari 0.")

    def tarif_alat(self):
        return self.alat.hitung_tarif(JadwalOperasional.tarif_per_jam)

    def total_biaya(self):
        return self.__durasi_jam * self.tarif_alat()

    def jalankan(self):
        return self.operator.operasikan(self.alat, self.__durasi_jam)

    @classmethod
    def ubah_tarif(cls, tarif_baru):
        cls.tarif_per_jam = tarif_baru
        print(f"Tarif dasar per jam berhasil diubah menjadi {rp(cls.tarif_per_jam)}")

alat1 = Excavator("A001", "Baik", 1500000000, 1.5)
alat2 = DumpTruck("A002", "Baik", 900000000, 10)

operator1 = Operator("O001", "Rizal", "1234567890")
operator2 = Operator("O002", "Putri", "0987654321")

jadwal1 = JadwalOperasional("J001", alat1, operator1, 8)
jadwal2 = JadwalOperasional("J002", alat2, operator2, 5)

print("=" * 55)
print("DATA AWAL")
print("=" * 55)
alat1.info()
alat2.info()
print(f"Operator 1 : {operator1.id_operator} - {operator1.nama} (SIM: {operator1.no_sim})")
print(f"Operator 2 : {operator2.id_operator} - {operator2.nama} (SIM: {operator2.no_sim})")

print("\n" + "=" * 55)
print("AGREGASI: PERUSAHAAN MEMILIKI ALAT & OPERATOR")
print("=" * 55)
perusahaan = Perusahaan("PT Borneo Konstruksi")
perusahaan.tambah_alat(alat1)
perusahaan.tambah_alat(alat2)
perusahaan.tambah_operator(operator1)
perusahaan.tambah_operator(operator2)
perusahaan.tampilkan_aset()

print("\n" + "=" * 55)
print("ASOSIASI: OPERATOR MENGGUNAKAN ALAT")
print("=" * 55)
jadwal1.jalankan()
jadwal2.jalankan()
alat1.gali(120)
alat2.angkut(8)
alat2.angkut(15)

print("\n" + "=" * 55)
print("METHOD OVERRIDING: TARIF & TOTAL BIAYA")
print("=" * 55)
print(f"Tarif dasar          : {rp(JadwalOperasional.tarif_per_jam)}/jam")
print(f"Tarif {alat1.jenis:<10}   : {rp(jadwal1.tarif_alat())}/jam")
print(f"Tarif {alat2.jenis:<10}   : {rp(jadwal2.tarif_alat())}/jam")
print(f"Total biaya jadwal 1 : {rp(jadwal1.total_biaya())}")
print(f"Total biaya jadwal 2 : {rp(jadwal2.total_biaya())}")
print(f"Validasi nomor SIM {operator1.nama} = {operator1.validasi_no_sim(operator1.no_sim)}")
JadwalOperasional.ubah_tarif(200000)

print("\n" + "=" * 55)
print("UJI DATA TIDAK VALID")
print("=" * 55)
alat1.status = "Rusak Parah"
operator1.no_sim = "abc123"
jadwal1.durasi_jam = -3

print("\n" + "=" * 55)
print("UJI DATA VALID")
print("=" * 55)
alat1.status = "Rusak"
operator1.no_sim = "1122334455"
jadwal1.durasi_jam = 10
print("Semua perubahan data valid berhasil disimpan.")

print("\n" + "=" * 55)
print("ALAT RUSAK TIDAK BISA DIPAKAI")
print("=" * 55)
jadwal1.jalankan()
alat1.gali(50)

print("\n" + "=" * 55)
print("DATA AKHIR SETELAH PERUBAHAN")
print("=" * 55)
print(f"Status alat 1 baru       : {alat1.status}")
print(f"Nomor SIM operator 1 baru: {operator1.no_sim}")
print(f"Durasi jadwal 1 baru     : {jadwal1.durasi_jam} jam")
print(f"Total biaya jadwal 1 baru: {rp(jadwal1.total_biaya())}")
print(f"Total biaya jadwal 2 baru: {rp(jadwal2.total_biaya())}")

print("\n" + "=" * 55)
print("KOMPOSISI: RIWAYAT PERAWATAN ALAT")
print("=" * 55)
alat1.tampilkan_riwayat()
alat2.tampilkan_riwayat()

print("\n" + "=" * 55)
print("PRIVATE vs PROTECTED")
print("=" * 55)
print(f"Harga perolehan alat 1 (property read-only): {rp(alat1.harga_perolehan)}")
print(f"Nilai alat 1 sekarang (setelah {alat1.total_jam_pakai} jam): {rp(alat1.nilai_sekarang())}")
try:
    print(alat1.__harga_perolehan)
except AttributeError as e:
    print(f"Akses langsung ke atribut private gagal: {e}")

print("\n" + "=" * 55)
print("CEK RELASI PEWARISAN")
print("=" * 55)
print(f"isinstance(alat1, AlatBerat)  : {isinstance(alat1, AlatBerat)}")
print(f"isinstance(alat1, DumpTruck)  : {isinstance(alat1, DumpTruck)}")
print(f"issubclass(DumpTruck, AlatBerat): {issubclass(DumpTruck, AlatBerat)}")

print("\n" + "=" * 55)
print("REKAP DATA")
print("=" * 55)
print(f"Total alat terdaftar    : {AlatBerat.total_alat}")
print(f"Total operator terdaftar: {Operator.total_operator}")