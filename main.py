import json
import os
from datetime import datetime, timedelta

# ============================
# LOAD & SAVE DATA
# ============================

def load_data(file, default):
    if not os.path.exists(file):
        return default
    with open(file, "r") as f:
        try:
            return json.load(f)
        except:
            return default

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# Database
bacaan = load_data("bacaan.json", [])
nilai = load_data("nilai.json", {})

ADMIN_PASSWORD = "admin123"   # bisa diubah guru


# ============================
# LOGIN SISTEM
# ============================

def login():
    print("=== Sistem Literasi Digital ===")
    mode = input("Masuk sebagai (1=Siswa, 2=Admin): ")

    if mode == "2":
        pwd = input("Masukkan password admin: ")
        if pwd == ADMIN_PASSWORD:
            admin_menu()
        else:
            print("Password salah!")
        return None

    # Login siswa
    nama = input("Masukkan nama kamu: ").strip()

    if nama not in nilai:
        nilai[nama] = {
            "poin": 0,
            "riwayat": [],
            "streak": 0,
            "last_read": None
        }
    print(f"\nSelamat datang, {nama}!\n")
    return nama


# ============================
# FUNGSI STREAK
# ============================

def update_streak(nama):
    today = datetime.now().date()
    last = nilai[nama]["last_read"]

    if last:
        last_date = datetime.strptime(last, "%Y-%m-%d").date()

        if last_date == today - timedelta(days=1):
            nilai[nama]["streak"] += 1
        elif last_date == today:
            # Tidak meningkatkan streak jika sudah membaca hari ini
            pass
        else:
            nilai[nama]["streak"] = 1
    else:
        nilai[nama]["streak"] = 1

    nilai[nama]["last_read"] = str(today)

    # Bonus poin
    if nilai[nama]["streak"] % 5 == 0:
        print(f"🔥 BONUS! Kamu mencapai streak {nilai[nama]['streak']} hari!")
        nilai[nama]["poin"] += 20


# ============================
# PILIH BACAAN
# ============================

def pilih_bacaan():
    if not bacaan:
        print("Belum ada bacaan!")
        return None

    print("\n=== Daftar Bacaan ===")
    for i, b in enumerate(bacaan):
        print(f"{i+1}. {b['judul']}")
    print()

    try:
        pilih = int(input("Pilih nomor bacaan: ")) - 1
        return bacaan[pilih]
    except:
        print("Pilihan tidak valid!")
        return None


# ============================
# PROSES MEMBACA
# ============================

def kerjakan_bacaan(nama):
    data = pilih_bacaan()
    if not data:
        return

    print("\n=== Bacaan ===")
    print(data["teks"])
    input("\nTekan ENTER jika sudah selesai membaca...")

    print("\n=== Pertanyaan ===")
    jawab = input(data["pertanyaan"] + ": ").lower()

    if data["jawaban"] in jawab:
        print("✔ Jawaban benar! +10 poin")
        nilai[nama]["poin"] += 10
        hasil = "benar"
    else:
        print("✘ Jawaban salah. +0 poin")
        hasil = "salah"

    # Update streak harian
    update_streak(nama)

    # Simpan riwayat
    nilai[nama]["riwayat"].append({
        "judul": data["judul"],
        "hasil": hasil,
        "tanggal": str(datetime.now().date())
    })

    save_data("nilai.json", nilai)


# ============================
# MENU NILAI SISWA
# ============================

def lihat_nilai(nama):
    print("\n=== Nilai Kamu ===")
    print("Total poin :", nilai[nama]["poin"])
    print("Streak     :", nilai[nama]["streak"])
    print("\nRiwayat:")
    for r in nilai[nama]["riwayat"]:
        print(f"- {r['tanggal']} | {r['judul']} : {r['hasil']}")


# ============================
# ADMIN MODE
# ============================

def admin_menu():
    while True:
        print("\n=== ADMIN MODE ===")
        print("1. Tambah Bacaan")
        print("2. Lihat Semua Bacaan")
        print("3. Hapus Bacaan")
        print("4. Lihat Ranking Siswa")
        print("5. Keluar Admin")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            tambah_bacaan()
        elif pilih == "2":
            list_bacaan()
        elif pilih == "3":
            hapus_bacaan()
        elif pilih == "4":
            ranking()
        elif pilih == "5":
            break
        else:
            print("Pilihan tidak valid!")


def tambah_bacaan():
    print("\n=== Tambah Bacaan ===")
    judul = input("Judul bacaan: ")
    teks = input("Isi bacaan: ")
    pertanyaan = input("Pertanyaan: ")
    jawaban = input("Jawaban benar: ").lower()

    bacaan.append({
        "judul": judul,
        "teks": teks,
        "pertanyaan": pertanyaan,
        "jawaban": jawaban
    })

    save_data("bacaan.json", bacaan)
    print("Bacaan berhasil ditambahkan!")


def list_bacaan():
    print("\n=== Daftar Bacaan ===")
    for i, b in enumerate(bacaan):
        print(f"{i+1}. {b['judul']}")


def hapus_bacaan():
    list_bacaan()
    try:
        hapus = int(input("Nomor bacaan yang akan dihapus: ")) - 1
        del bacaan[hapus]
        save_data("bacaan.json", bacaan)
        print("Bacaan dihapus!")
    except:
        print("Pilihan tidak valid!")


def ranking():
    print("\n=== Ranking Siswa ===")
    urut = sorted(nilai.items(), key=lambda x: x[1]["poin"], reverse=True)

    for i, (nama, data) in enumerate(urut):
        print(f"{i+1}. {nama} - {data['poin']} poin | streak {data['streak']}")


# ============================
# MENU UTAMA
# ============================

def main():
    nama = login()
    if nama is None:
        return

    while True:
        print("\n=== Menu ===")
        print("1. Baca & Kerjakan")
        print("2. Lihat Nilai")
        print("3. Keluar")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            kerjakan_bacaan(nama)
        elif pilih == "2":
            lihat_nilai(nama)
        elif pilih == "3":
            print("Keluar...")
            break
        else:
            print("Pilihan salah!")


if __name__ == "__main__":
    main()
