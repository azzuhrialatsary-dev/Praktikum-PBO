from abc import ABC, abstractmethod


def rp(angka):
    """Format angka menjadi Rupiah, contoh: Rp 1.200.000"""
    return f"Rp {angka:,}".replace(",", ".")


# =====================================================================
# KOMPOSISI: CatatanPerawatan hanya hidup di dalam AlatBerat
# =====================================================================
class CatatanPerawatan:

    def __init__(self, id_catatan, tipe, keterangan):
        self.id_catatan = id_catatan
        self.tipe = tipe
        self.keterangan = keterangan

    def __str__(self):
        return f"[{self.id_catatan}] {self.tipe:<10} | {self.keterangan}"


# =====================================================================
# ABSTRAKSI: AlatBerat adalah Abstract Base Class
# =====================================================================
class AlatBerat(ABC):

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

    # ---------- Abstract method (wajib di-implementasi subclass) ----------
    @abstractmethod
    def hitung_tarif(self, tarif_dasar):
        """Tarif per jam alat."""

    @abstractmethod
    def bekerja(self, beban):
        """Aksi kerja utama alat (menggali / mengangkut / mendorong)."""

    # ---------- Property & validasi ----------
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

    # ---------- Method konkret (dipakai bersama semua subclass) ----------
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

    def jalankan(self, beban):
        """Template method: cek status dulu, lalu serahkan aksi ke subclass."""
        if self._status != "Baik":
            print(f"[GAGAL] {self.kode} rusak, tidak bisa bekerja.")
            return False
        self.bekerja(beban)
        return True

    def info(self):
        print(f"{self.kode} - {self.jenis} | Status: {self._status} | "
            f"Jam pakai: {self._total_jam_pakai} jam")

    # ---------- OPERATOR OVERLOADING ----------
    def __str__(self):
        return f"{self.jenis} {self.kode} ({self._status}, {self._total_jam_pakai} jam)"

    def __eq__(self, other):
        if not isinstance(other, AlatBerat):
            return NotImplemented
        return self.kode == other.kode

    def __hash__(self):
        return hash(self.kode)

    def __lt__(self, other):
        return self._total_jam_pakai < other._total_jam_pakai


# =====================================================================
# SUBCLASS (implementasi seluruh abstract method)
# =====================================================================
class Excavator(AlatBerat):

    def __init__(self, kode, status, harga_perolehan, kapasitas_bucket):
        super().__init__(kode, "Excavator", status, harga_perolehan)
        self.kapasitas_bucket = kapasitas_bucket

    def hitung_tarif(self, tarif_dasar):
        return tarif_dasar + int(self.kapasitas_bucket * 25000)

    def bekerja(self, volume):
        print(f"{self.kode} menggali tanah sebanyak {volume} m3.")

    def info(self):
        super().info()
        print(f"   Kapasitas bucket: {self.kapasitas_bucket} m3")


class DumpTruck(AlatBerat):

    def __init__(self, kode, status, harga_perolehan, kapasitas_ton):
        super().__init__(kode, "Dump Truck", status, harga_perolehan)
        self.kapasitas_ton = kapasitas_ton

    def hitung_tarif(self, tarif_dasar):
        return tarif_dasar + self.kapasitas_ton * 5000

    def bekerja(self, ton):
        if ton > self.kapasitas_ton:
            print(f"[GAGAL] Muatan {ton} ton melebihi kapasitas {self.kapasitas_ton} ton.")
        else:
            print(f"{self.kode} mengangkut muatan {ton} ton.")

    def info(self):
        super().info()
        print(f"   Kapasitas muatan: {self.kapasitas_ton} ton")


# Bukti OCP: kelas baru ditambahkan TANPA mengubah AlatBerat, Operator,
# JadwalOperasional, maupun Perusahaan.
class Bulldozer(AlatBerat):

    def __init__(self, kode, status, harga_perolehan, lebar_blade):
        super().__init__(kode, "Bulldozer", status, harga_perolehan)
        self.lebar_blade = lebar_blade

    def hitung_tarif(self, tarif_dasar):
        return tarif_dasar + int(self.lebar_blade * 30000)

    def bekerja(self, luas):
        print(f"{self.kode} meratakan lahan seluas {luas} m2.")

    def info(self):
        super().info()
        print(f"   Lebar blade: {self.lebar_blade} m")


# =====================================================================
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

    # DUCK TYPING: method ringkasan() juga dimiliki Perusahaan
    def ringkasan(self):
        return f"Operator {self.id_operator} - {self.nama} (SIM: {self.__no_sim})"

    def __str__(self):
        return f"{self.id_operator} {self.nama}"


# AGREGASI: Perusahaan memiliki alat & operator, tetapi mereka tetap
# bisa ada tanpa Perusahaan (dibuat di luar, hanya dimasukkan ke daftar).
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

    def alat_terurut(self):
        """Urut berdasarkan jam pakai, memakai __lt__ milik AlatBerat."""
        return sorted(self._daftar_alat)

    # DUCK TYPING: method ringkasan() juga dimiliki Operator
    def ringkasan(self):
        return (f"Perusahaan {self.nama} | {len(self._daftar_alat)} alat, "
                f"{len(self._daftar_operator)} operator")

    # OPERATOR OVERLOADING
    def __len__(self):
        return len(self._daftar_alat)


# ASOSIASI: JadwalOperasional menghubungkan Operator dengan AlatBerat.
# Alat diterima sebagai abstraksi AlatBerat (DIP via dependency injection).
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


# DUCK TYPING: fungsi ini tidak peduli tipe objek, asal punya ringkasan()
def cetak_ringkasan(sumber):
    print(f"  > {sumber.ringkasan()}")


def judul(teks):
    print("\n" + "=" * 60)
    print(teks)
    print("=" * 60)


def sub(teks):
    print(f"\n[{teks}]")


alat1 = Excavator("A001", "Baik", 1500000000, 1.5)
alat2 = DumpTruck("A002", "Baik", 900000000, 10)
alat3 = Bulldozer("A003", "Baik", 1200000000, 3.2)
daftar_alat = [alat1, alat2, alat3]

operator1 = Operator("O001", "Rizal", "1234567890")
operator2 = Operator("O002", "Putri", "0987654321")
operator3 = Operator("O003", "Dimas", "5566778899")

perusahaan = Perusahaan("PT Borneo Konstruksi")
for alat in daftar_alat:
    perusahaan.tambah_alat(alat)
for op in (operator1, operator2, operator3):
    perusahaan.tambah_operator(op)

jadwal1 = JadwalOperasional("J001", alat1, operator1, 8)
jadwal2 = JadwalOperasional("J002", alat2, operator2, 5)
jadwal3 = JadwalOperasional("J003", alat3, operator3, 6)

judul("1. RELASI UML")
print(f"Agregasi  : {perusahaan.nama} memiliki {len(perusahaan)} alat dan 3 operator")
print(f"Asosiasi  : jadwal {jadwal1.id_jadwal} menghubungkan {jadwal1.operator.nama} dan {jadwal1.alat.kode}")
jadwal1.jalankan()
print("Komposisi : riwayat perawatan dibuat di dalam AlatBerat")
alat1.tampilkan_riwayat()

judul("2. ABSTRAKSI")
sub("Abstract class")
print("AlatBerat(ABC)")
sub("Abstract method")
print(", ".join(sorted(AlatBerat.__abstractmethods__)))
sub("Subclass yang mengimplementasikan semua abstract method")
for kelas in AlatBerat.__subclasses__():
    print(f"{kelas.__name__:<10}: lengkap = {not kelas.__abstractmethods__}")
sub("Method konkret yang dipakai bersama: jalankan()")
for kelas in AlatBerat.__subclasses__():
    print(f"{kelas.__name__:<10}: memakai jalankan() milik AlatBerat = {kelas.jalankan is AlatBerat.jalankan}")
sub("Bukti abstract class tidak bisa diinstansiasi")
try:
    AlatBerat("X000", "Alat Abstrak", "Baik", 1000000)
except TypeError as e:
    print(f"TypeError: {e}")
sub("Inheritance: super().__init__(), atribut unik, Protected/Private")
print(f"Atribut unik : bucket {alat1.kapasitas_bucket} m3, truk {alat2.kapasitas_ton} ton, blade {alat3.lebar_blade} m")
print(f"Protected    : _status dibaca lewat property status = {alat1.status}")
try:
    print(alat1.__harga_perolehan)
except AttributeError:
    print(f"Private      : __harga_perolehan tidak bisa diakses langsung, lewat property = {rp(alat1.harga_perolehan)}")

judul("3. POLIMORFISME")
sub("Via pewarisan: satu loop, bekerja() & hitung_tarif() berbeda tiap subclass")
for alat, beban in zip(daftar_alat, (120, 8, 450)):
    alat.jalankan(beban)
    print(f"  tarif {alat.jenis:<10}: {rp(alat.hitung_tarif(JadwalOperasional.tarif_per_jam))}/jam")
alat2.jalankan(15)
sub("Duck typing: cetak_ringkasan() untuk Operator & Perusahaan")
for sumber in (operator1, perusahaan):
    cetak_ringkasan(sumber)
sub("Operator overloading")
print(f"__str__ : {alat1}")
print(f"__eq__  : alat1 == alat2 -> {alat1 == alat2}")
print(f"__lt__  : alat2 < alat1  -> {alat2 < alat1}")
print(f"__len__ : len(perusahaan) -> {len(perusahaan)}")

judul(" SOLID")
sub("OCP & DIP: jadwal menerima alat apa pun (termasuk Bulldozer yang ditambahkan belakangan)")
for jadwal in (jadwal1, jadwal2, jadwal3):
    print(f"{jadwal.id_jadwal} {jadwal.alat.jenis:<10}: {rp(jadwal.total_biaya())}")

judul("VALIDASI")
alat1.status = "Rusak Parah"
operator1.no_sim = "abc123"
jadwal1.durasi_jam = -3
alat1.status = "Rusak"
jadwal1.jalankan()