class AlatBerat:

    total_alat = 0

    def __init__(self, kode, jenis, status):
        self.kode = kode
        self.jenis = jenis
        self.__status = status

        AlatBerat.total_alat += 1

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status_baru):
        if self.validasi_status(status_baru):
            self.__status = status_baru
        else:
            print(f"[GAGAL] Status '{status_baru}' tidak valid. Harus 'Baik' atau 'Rusak'.")

    @staticmethod
    def validasi_status(status):
        return status in ["Baik", "Rusak"]


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

    def total_biaya(self):
        return self.__durasi_jam * JadwalOperasional.tarif_per_jam

    @classmethod
    def ubah_tarif(cls, tarif_baru):
        cls.tarif_per_jam = tarif_baru
        print(f"Tarif per jam berhasil diubah menjadi Rp {cls.tarif_per_jam:,}".replace(",", "."))

alat1 = AlatBerat("A001", "Excavator", "Baik")
alat2 = AlatBerat("A002", "Dump Truck", "Baik")

operator1 = Operator("O001", "Rizal", "1234567890")
operator2 = Operator("O002", "Putri", "0987654321")

jadwal1 = JadwalOperasional("J001", alat1, operator1, 8)
jadwal2 = JadwalOperasional("J002", alat2, operator2, 5)

print("=" * 50)
print("DATA AWAL")
print("=" * 50)
print(f"Alat 1     : {alat1.kode} - {alat1.jenis} ({alat1.status})")
print(f"Alat 2     : {alat2.kode} - {alat2.jenis} ({alat2.status})")
print(f"Operator 1 : {operator1.id_operator} - {operator1.nama} (SIM: {operator1.no_sim})")
print(f"Operator 2 : {operator2.id_operator} - {operator2.nama} (SIM: {operator2.no_sim})")

print("\n" + "=" * 50)
print("TOTAL BIAYA & VALIDASI")
print("=" * 50)
print(f"Total biaya jadwal 1 ({jadwal1.alat.jenis} - {jadwal1.operator.nama})")
print(f"  = Rp {jadwal1.total_biaya():,}".replace(",", "."))
print(f"Validasi nomor SIM {operator1.nama} = {operator1.validasi_no_sim(operator1.no_sim)}")
JadwalOperasional.ubah_tarif(200000)

print("\n" + "=" * 50)
print("UJI DATA TIDAK VALID")
print("=" * 50)
alat1.status = "Rusak Parah"
operator1.no_sim = "abc123"
jadwal1.durasi_jam = -3

print("\n" + "=" * 50)
print("UJI DATA VALID")
print("=" * 50)
alat1.status = "Rusak"
operator1.no_sim = "1122334455"
jadwal1.durasi_jam = 10
print("Semua perubahan data valid berhasil disimpan.")

print("\n" + "=" * 50)
print("DATA AKHIR SETELAH PERUBAHAN")
print("=" * 50)
print(f"Status alat 1 baru       : {alat1.status}")
print(f"Nomor SIM operator 1 baru: {operator1.no_sim}")
print(f"Durasi jadwal 1 baru     : {jadwal1.durasi_jam} jam")
print(f"Total biaya jadwal 1 baru: Rp {jadwal1.total_biaya():,}".replace(",", "."))

print("\n" + "=" * 50)
print("REKAP DATA")
print("=" * 50)
print(f"Total alat terdaftar    : {AlatBerat.total_alat}")
print(f"Total operator terdaftar: {Operator.total_operator}")