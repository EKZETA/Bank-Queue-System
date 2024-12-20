import uuid
from datetime import datetime
from typing import List, Optional

class Nasabah:
    def __init__(self, nama: str, nomor_antrian: int):
        self.id = str(uuid.uuid4())
        self.nama = nama
        self.nomor_antrian = nomor_antrian
        self.waktu_kedatangan = datetime.now()

class Loket:
    def __init__(self, nomor: int, kategori: str):
        # Generate kode unik loket berdasarkan kategori
        self.kode_loket = f"{'A' if kategori == 'teller' else 'B'}{nomor:02d}"
        self.nomor = nomor
        self.kategori = kategori
        self.nasabah_saat_ini: Optional[Nasabah] = None

class SistemAntrianBank:
    def __init__(self):
        # Inisialisasi loket dengan kode unik
        self.loket_teller = [Loket(i+1, 'teller') for i in range(4)]
        self.loket_cs = [Loket(i+1, 'cs') for i in range(3)]
        
        # Antrian
        self.antrian_teller: List[Nasabah] = []
        self.antrian_cs: List[Nasabah] = []
        
        # Nomor antrian terakhir
        self.nomor_antrian_teller = 0
        self.nomor_antrian_cs = 0

    def tambah_nasabah(self, nama: str, kategori: str):
        # Menentukan kategori dan antrian
        if kategori == 'teller':
            self.nomor_antrian_teller += 1
            nomor_antrian = self.nomor_antrian_teller
            antrian = self.antrian_teller
            loket = self.loket_teller
        else:
            self.nomor_antrian_cs += 1
            nomor_antrian = self.nomor_antrian_cs
            antrian = self.antrian_cs
            loket = self.loket_cs

        # Buat nasabah baru
        nasabah_baru = Nasabah(nama, nomor_antrian)
        
        # Periksa apakah ada loket kosong
        loket_kosong = next((l for l in loket if l.nasabah_saat_ini is None), None)
        
        if loket_kosong:
            # Langsung layani di loket kosong
            loket_kosong.nasabah_saat_ini = nasabah_baru
            print(f"Nasabah {nama} langsung dilayani di {kategori.capitalize()} {loket_kosong.kode_loket}")
            return nomor_antrian
        else:
            # Tambahkan ke antrian
            antrian.append(nasabah_baru)
            print(f"Nasabah {nama} menunggu di antrian {kategori.capitalize()}. Nomor Antrian: {nomor_antrian}")
            return nomor_antrian

    def update_antrian(self, kategori: str):
        # Menentukan kategori dan antrian
        if kategori == 'teller':
            antrian = self.antrian_teller
            loket = self.loket_teller
        else:
            antrian = self.antrian_cs
            loket = self.loket_cs

        # Cari loket kosong
        loket_kosong = next((l for l in loket if l.nasabah_saat_ini is None), None)
        
        # Jika ada loket kosong dan ada antrian
        if loket_kosong and antrian:
            # Ambil nasabah pertama dalam antrian (FIFO)
            nasabah_berikutnya = min(antrian, key=lambda n: n.nomor_antrian)
            
            # Tempatkan di loket kosong
            loket_kosong.nasabah_saat_ini = nasabah_berikutnya
            
            # Hapus dari antrian
            antrian.remove(nasabah_berikutnya)
            
            print(f"Nasabah {nasabah_berikutnya.nama} (Nomor Antrian: {nasabah_berikutnya.nomor_antrian}) "
                  f"dipanggil di {kategori.capitalize()} {loket_kosong.kode_loket}")

    def tampilkan_status_antrian(self, kategori: str):
        if kategori == 'teller':
            antrian = self.antrian_teller
            loket = self.loket_teller
        else:
            antrian = self.antrian_cs
            loket = self.loket_cs

        print(f"\nStatus Antrian {kategori.capitalize()}:")
        
        # Tampilkan status loket
        for l in loket:
            if l.nasabah_saat_ini:
                print(f"Loket {l.kode_loket}: Sedang melayani {l.nasabah_saat_ini.nama} "
                      f"(Nomor Antrian: {l.nasabah_saat_ini.nomor_antrian})")
            else:
                print(f"Loket {l.kode_loket}: Kosong")
        
        # Tampilkan antrian
        if antrian:
            print("Nasabah dalam Antrian:")
            for n in sorted(antrian, key=lambda x: x.nomor_antrian):
                print(f"- {n.nama} (Nomor Antrian: {n.nomor_antrian})")
        else:
            print("Tidak ada nasabah dalam antrian.")

def main():
    sistem_antrian = SistemAntrianBank()

    while True:
        print("\n--- SISTEM ANTRIAN BANK ---")
        print("1. Loket Teller")
        print("2. Customer Service")
        print("3. Keluar")
        
        pilihan = input("Pilih layanan (1/2/3): ")

        if pilihan == '3':
            print("Terima kasih. Selamat tinggal!")
            break

        if pilihan not in ['1', '2']:
            print("Pilihan tidak valid. Silakan coba lagi.")
            continue

        kategori = 'teller' if pilihan == '1' else 'cs'
        
        while True:
            print(f"\n--- MENU {kategori.upper()} ---")
            print("1. Ambil Nomor Antrian")
            print("2. Lihat Status Antrian")
            print("3. Kembali ke Menu Utama")
            
            sub_pilihan = input("Pilih opsi: ")
            
            if sub_pilihan == '3':
                break
            
            if sub_pilihan == '1':
                nama = input("Masukkan nama Anda: ")
                sistem_antrian.tambah_nasabah(nama, kategori)
                sistem_antrian.update_antrian(kategori)
            
            elif sub_pilihan == '2':
                sistem_antrian.tampilkan_status_antrian(kategori)
            
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()