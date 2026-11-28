EKSKUL = (
    ("FUT", "Futsal", 20, 150000),
    ("BAN", "Basket", 20, 150000),
    ("PMR", "PMR", 30, 100000),
    ("ROB", "Robotik", 15, 250000),
)

KODE_EKSKUL = {"FUT", "BAN", "PMR", "ROB"}

AKUN = (
    ("admin", "admin123", "admin"),
    ("user", "user123", "user"),
)

data_pendaftaran = []

def lihat_ekskul(data):
    print("DAFTAR EKSTRAKURIKULER")
    print("KODE| NAMA | KUOTA | TERISI | SISA | BIAYA")
    for kode, nama, kuota, biaya in EKSKUL:
        terisi = hitung_pendaftar(data, kode)
        sisa = kuota - terisi
        if sisa == 0:
            status = "PENUH"
        else:
            status = "tersedia"
        print(kode, "|", nama, "|", kuota, "|", terisi, "|", sisa, "|", "Rp" + str(biaya), "|", status)


def lihat_data(data):
    print("DATA PENDAFTARAN")
    if len(data) == 0:
        print("Belum ada data pendaftaran.")
        return

    print("ID| NIS   | NAMA    | KELAS   | EKSKUL  | BIAYA")
    total = 0
    for pendaftaran in data:
        ekskul = cari_ekskul(pendaftaran["ekskul"])
        total = total + pendaftaran["biaya"]
        print(pendaftaran["id"], "|", pendaftaran["nis"], "|", pendaftaran["nama"], "|",
              pendaftaran["kelas"], "|", ekskul[1], "|", "Rp" + str(pendaftaran["biaya"]))
    print("Jumlah data :", len(data))
    print("Total biaya :", "Rp" + str(total))


def tampilkan_menu(role):
    print()
    print("SISTEM PENDAFTARAN EKSTRAKURIKULER")
    print("Login sebagai :", role)
    if role == "admin":
        print("1. Lihat semua pendaftaran")
        print("2. Tambah pendaftaran")
        print("3. Ubah pendaftaran")
        print("4. Hapus pendaftaran")
        print("5. Cari pendaftaran")
        print("0. Logout")
        print("9. Keluar program")
    else:
        print("1. Lihat semua pendaftaran")
        print("2. Daftar ekstrakurikuler")
        print("3. Cari pendaftaran")
        print("0. Logout")
        print("9. Keluar program")


def baca_angka(pesan, minimal, maksimal):
    while True:
        try:
            angka = int(input(pesan))
        except ValueError:
            print("Input salah: harus berupa angka.")
            continue

        if angka < minimal or angka > maksimal:
            print("Input salah: pilih angka", minimal, "sampai", maksimal)
        else:
            return angka


def baca_pilihan(pesan, pilihan):
    while True:
        try:
            angka = int(input(pesan))
        except ValueError:
            print("Input salah: harus berupa angka.")
            continue

        if angka not in pilihan:
            print("Input salah: pilihan yang tersedia", sorted(pilihan))
        else:
            return angka


def validasi_nis(nis):
    nis = nis.strip()
    if nis == "":
        raise ValueError("NIS tidak boleh kosong.")
    if not nis.isdigit():
        raise ValueError("NIS harus berupa angka.")
    if len(nis) != 5:
        raise ValueError("NIS harus 5 digit.")
    if nis in [pendaftaran["nis"] for pendaftaran in data_pendaftaran]:
        raise ValueError("NIS sudah terdaftar.")
    return nis


def validasi_nama(nama):
    nama = nama.strip()
    if len(nama) < 3:
        raise ValueError("Nama minimal 3 huruf.")
    if not nama.replace(" ", "").isalpha():
        raise ValueError("Nama hanya boleh huruf dan spasi.")
    return nama


def validasi_kelas(kelas):
    kelas = kelas.strip().upper()
    bagian = kelas.split("-")
    if len(bagian) != 2:
        raise ValueError("Format kelas harus TINGKAT-JURUSAN, contoh: XI-RPL")
    if bagian[0] not in ("X", "XI", "XII"):
        raise ValueError("Tingkat kelas harus X, XI, atau XII.")
    if bagian[1] not in ("RPL", "TKJ", "TBSM"):
        raise ValueError("Pilihan jurusan tidak valid, pilih antara RPL, TKJ, atau TBSM.")
    return kelas


def minta_nis():
    while True:
        try:
            return validasi_nis(input("NIS (5 angka): "))
        except ValueError as salah:
            print("Input salah:", salah)


def minta_nama():
    while True:
        try:
            return validasi_nama(input("Nama siswa: "))
        except ValueError as salah:
            print("Input salah:", salah)


def minta_kelas():
    while True:
        try:
            return validasi_kelas(input("Kelas (KELAS-JURUSAN): "))
        except ValueError as salah:
            print("Input salah:", salah)


def minta_ekskul(data):
    lihat_ekskul(data)
    while True:
        kode = input("Kode ekskul: ").upper()
        if kode not in KODE_EKSKUL:
            print("Input salah: kode tidak ada. Pilihan:", sorted(KODE_EKSKUL))
        elif kuota_penuh(data, kode):
            print("Input salah: kuota ekskul ini sudah penuh.")
        else:
            return kode


def cari_ekskul(kode):
    # mengembalikan tuple (kode, nama, kuota, biaya)
    for data_ekskul in EKSKUL:
        if data_ekskul[0] == kode:
            return data_ekskul
    return None


def hitung_pendaftar(data, kode):
    jumlah = 0
    for pendaftaran in data:
        if pendaftaran["ekskul"] == kode:
            jumlah = jumlah + 1
    return jumlah


def kuota_penuh(data, kode):
    ekskul = cari_ekskul(kode)
    terisi = hitung_pendaftar(data, kode)
    if terisi >= ekskul[2]:
        return True
    else:
        return False


def sudah_daftar(data, nis, kode):
    for pendaftaran in data:
        if pendaftaran["nis"] == nis and pendaftaran["ekskul"] == kode:
            return True
    return False


def cari_id(data, id_cari):
    for pendaftaran in data:
        if pendaftaran["id"] == id_cari:
            return pendaftaran
    return None


def ambil_id_baru(data):
    if len(data) == 0:
        return 1
    id_terbesar = 0
    for pendaftaran in data:
        if pendaftaran["id"] > id_terbesar:
            id_terbesar = pendaftaran["id"]
    return id_terbesar + 1


def tambah_data(data):
    print("TAMBAH PENDAFTARAN")

    nis = minta_nis()
    nama = minta_nama()
    kelas = minta_kelas()
    kode = minta_ekskul(data)

    if sudah_daftar(data, nis, kode):
        print("Gagal: siswa ini sudah terdaftar di ekskul tersebut.")
        return

    ekskul = cari_ekskul(kode)
    pendaftaran_baru = {
        "id": ambil_id_baru(data),
        "nis": nis,
        "nama": nama,
        "kelas": kelas,
        "ekskul": kode,
        "biaya": ekskul[3],
    }
    data.append(pendaftaran_baru)
    print("Berhasil: pendaftaran nomor", pendaftaran_baru["id"], "ditambahkan.")


def cari_data(data):
    print("CARI PENDAFTARAN")
    if len(data) == 0:
        print("Belum ada data pendaftaran.")
        return

    kata_kunci = input("Masukkan NIS atau nama: ").strip().lower()
    if kata_kunci == "":
        print("Input salah: kata kunci tidak boleh kosong.")
        return

    hasil = []
    for pendaftaran in data:
        if kata_kunci in pendaftaran["nis"].lower() or kata_kunci in pendaftaran["nama"].lower():
            hasil.append(pendaftaran)

    if len(hasil) == 0:
        print("Data tidak ditemukan.")
    else:
        print("Ditemukan", len(hasil), "data:")
        lihat_data(hasil)


def ubah_data(data):
    if len(data) == 0:
        print("Belum ada data yang bisa diubah.")
        return

    lihat_data(data)
    id_cari = baca_angka("Masukkan ID yang ingin diubah: ", 1, 9999)
    pendaftaran = cari_id(data, id_cari)
    if pendaftaran == None:
        print("ID tidak ditemukan.")
        return

    print("Data sekarang :", pendaftaran["nama"], "|", pendaftaran["kelas"], "|", pendaftaran["ekskul"])
    print("1. Ubah nama")
    print("2. Ubah kelas")
    print("3. Ubah ekskul")
    print("0. Batal")
    pilihan = baca_angka("Pilih : ", 0, 3)

    if pilihan == 0:
        print("Perubahan dibatalkan.")
        return
    elif pilihan == 1:
        pendaftaran["nama"] = minta_nama()
    elif pilihan == 2:
        pendaftaran["kelas"] = minta_kelas()
    elif pilihan == 3:
        kode = minta_ekskul(data)
        if kode != pendaftaran["ekskul"] and sudah_daftar(data, pendaftaran["nis"], kode):
            print("Gagal: siswa ini sudah terdaftar di ekskul tersebut.")
            return
        pendaftaran["ekskul"] = kode
        pendaftaran["biaya"] = cari_ekskul(kode)[3]

    print("Data berhasil diubah.")


def hapus_data(data):
    if len(data) == 0:
        print("Belum ada data yang bisa dihapus.")
        return

    lihat_data(data)
    id_cari = baca_angka("Masukkan ID yang ingin dihapus : ", 1, 9999)
    pendaftaran = cari_id(data, id_cari)
    if pendaftaran == None:
        print("ID tidak ditemukan.")
        return

    print("Data yang akan dihapus :", pendaftaran["nama"], "|", pendaftaran["kelas"], "|", pendaftaran["ekskul"])
    jawab = input("Yakin ingin menghapus? (y/n) : ").lower()
    if jawab == "y":
        data.remove(pendaftaran)
        print("Data berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")


def login():
    print("LOGIN SISTEM PENDAFTARAN EKSTRAKURIKULER")
    print("Akun admin : admin / admin123")
    print("Akun user  : user / user123")
    print("Ketik 0 pada username untuk keluar program.")

    percobaan = 0
    while percobaan < 3:
        username = input("Username : ").strip()
        if username == "0":
            return "keluar"

        password = input("Password : ").strip()

        for akun in AKUN:
            if akun[0] == username and akun[1] == password:
                print("Login berhasil. Selamat datang,", username)
                return akun[2]

        percobaan = percobaan + 1
        print("Login gagal. Sisa percobaan :", 3 - percobaan)

    return None


def menu_admin(data):
    # mengembalikan True jika memilih keluar program, False jika logout
    while True:
        tampilkan_menu("admin")
        pilihan = baca_pilihan("Pilih menu : ", {0, 1, 2, 3, 4, 5, 9})

        if pilihan == 0:
            print("Logout berhasil. Kembali ke halaman login.")
            return False
        elif pilihan == 9:
            print("Terima kasih. Program selesai.")
            return True
        elif pilihan == 1:
            lihat_data(data)
        elif pilihan == 2:
            tambah_data(data)
        elif pilihan == 3:
            ubah_data(data)
        elif pilihan == 4:
            hapus_data(data)
        elif pilihan == 5:
            cari_data(data)


def menu_user(data):
    # mengembalikan True jika memilih keluar program, False jika logout
    while True:
        tampilkan_menu("user")
        pilihan = baca_pilihan("Pilih menu : ", {0, 1, 2, 3, 9})

        if pilihan == 0:
            print("Logout berhasil. Kembali ke halaman login.")
            return False
        elif pilihan == 9:
            print("Terima kasih. Program selesai.")
            return True
        elif pilihan == 1:
            lihat_data(data)
        elif pilihan == 2:
            tambah_data(data)
        elif pilihan == 3:
            cari_data(data)


def jalankan_program():
    print("Selamat datang di Sistem Pendaftaran Ekstrakurikuler")

    while True:
        role = login()

        if role == "keluar":
            print("Terima kasih. Program selesai.")
            break

        if role == None:
            print("Login gagal 3 kali. Program berhenti.")
            break

        if role == "admin":
            keluar = menu_admin(data_pendaftaran)
        else:
            keluar = menu_user(data_pendaftaran)

        if keluar:
            break


jalankan_program()
