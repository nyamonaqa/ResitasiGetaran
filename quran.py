import os
import random
import time
import requests
import datetime

def kirim_ntfy(pesan):
    # Diambil dari GitHub Secrets
    topic = os.getenv("NTFY_TOPIC")
    if topic:
        try:
            requests.post(f"https://ntfy.sh/{topic}", 
                          data=pesan.encode('utf-8'),
                          headers={"Title": "Khatam Qur'an Digital"})
        except:
            print("Gagal kirim notifikasi, lanjut...")

def main():
    # 1. Melacak Juz (Simpan di file progres)
    statusfile = "progres.txt"
    if not os.path.exists(statusfile):
        juzsekarang = 1
    else:
        with open(statusfile, "r") as f:
            try:
                juzsekarang = int(f.read().strip())
            except:
                juzsekarang = 1

    niat = "Tuan Ahmad Syafruddin sekeluarga, Mahmud Nur sekeluarga, dan adinda Muhammad Ikram"
    
    # 2. Ambil data teks asli
    print(f"Mengambil data teks Juz {juzsekarang}...")
    try:
        response = requests.get(f"https://api.alquran.cloud/v1/juz/{juzsekarang}/quran-uthmani")
        data = response.json()
        ayatlist = data['data']['ayahs']
    except Exception as e:
        print(f"Error koneksi API: {e}")
        return

    # 3. Simulasi Getaran Manusiawi
    print(f"Niat: Pembacaan Juz {juzsekarang} untuk {niat}")
    for ayat in ayatlist:
        # Jeda sejenak per ayat agar tidak robotik
        time.sleep(random.uniform(0.5, 1.5))
        
    waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    laporan = f"Alhamdulillah, Juz {juzsekarang} selesai untuk {niat} pada {waktu}."
    
    # 4. Generate 2 File Laporan (Nama satu kata)
    with open("kehadiran.txt", "a") as f:
        f.write(f"Hadir: {waktu}\n")
    
    with open("riwayat.txt", "a") as f:
        f.write(laporan + "\n")
    
    # 5. Update Progres Juz
    juzbesok = juzsekarang + 1 if juzsekarang < 30 else 1
    with open(statusfile, "w") as f:
        f.write(str(juzbesok))
    
    # 6. Lapor ke HP
    kirim_ntfy(laporan)
    print("Selesai dikerjakan.")

if __name__ == "__main__":
    # Delay acak 0-10 menit sebelum mulai agar natural
    time.sleep(random.randint(0, 600))
    main()
