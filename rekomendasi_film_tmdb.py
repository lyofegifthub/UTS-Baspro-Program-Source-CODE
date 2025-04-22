import requests
from prettytable import PrettyTable
from urllib.parse import quote_plus
import time

API_KEY = "64cce12440c495196fd586d7b70bdb29"

mood_genres = {
    "happy": "35",       # Comedy
    "sad": "18",         # Drama
    "chill": "10749",    # Romance
    "energetic": "28"    # Action
}

def cek_idlix_tersedia(judul):
    link = f"https://tv2.idlixvip.asia/?s={quote_plus(judul)}"
    try:
        r = requests.get(link, timeout=10)
        if "tidak tersedia" in r.text.lower() or "tidak ditemukan" in r.text.lower():
            return False
        return True
    except:
        return False

def ambil_film(mood, page=1):
    genre_id = mood_genres.get(mood)
    if not genre_id:
        print("❌ Mood tidak dikenali. Pilih: happy, sad, chill, energetic.")
        return []

    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": API_KEY,
        "with_genres": genre_id,
        "sort_by": "popularity.desc",
        "language": "id-ID",
        "page": page
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data.get("results", [])
    except Exception as e:
        print("❌ Gagal mengambil data dari TMDB:", e)
        return []

def tampilkan_rekomendasi(results):
    table = PrettyTable()
    table.field_names = ["Judul", "Tanggal Rilis", "Deskripsi Singkat"]
    table.align["Judul"] = "l"
    table.align["Tanggal Rilis"] = "c"
    table.align["Deskripsi Singkat"] = "l"

    count = 0
    for movie in results:
        judul = movie.get("title", "-")
        if cek_idlix_tersedia(judul):
            tanggal = movie.get("release_date", "-")
            overview = movie.get("overview", "Tidak tersedia")[:80] + "..."
            link_tmdb = f"https://www.themoviedb.org/movie/{movie['id']}"
            link_idlix = f"https://tv2.idlixvip.asia/?s={quote_plus(judul)}"

            table.add_row([judul, tanggal, overview])
            print(table)
            print(f"🔗 TMDB  : {link_tmdb}")
            print(f"🎞️ IDLIX : {link_idlix}")
            print("-" * 100)
            table.clear_rows()

            count += 1
            if count >= 5:
                break
            time.sleep(1)

    if count == 0:
        print("❌ Tidak ada film yang tersedia di IDLIX dari hasil ini.\n")

def main():
    print("🎥 Program Rekomendasi Film Berdasarkan Mood 🎥\n")
    
    while True:
        mood = input("Masukkan mood kamu (happy/sad/chill/energetic): ").strip().lower()
        if mood not in mood_genres:
            print("❌ Mood tidak valid.")
            continue

        page = 1
        while True:
            print(f"\n📃 Rekomendasi film untuk mood '{mood}' (halaman {page}):\n")
            results = ambil_film(mood, page)
            if not results:
                print("⚠️ Tidak ada film ditemukan.")
                break
            tampilkan_rekomendasi(results)

            aksi = input("\nKetik 'more' untuk rekomendasi tambahan, 'back' untuk ganti mood, atau 'exit' untuk keluar: ").strip().lower()
            if aksi == "more":
                page += 1
            elif aksi == "back":
                break
            elif aksi == "exit":
                print("👋 Terima kasih telah menggunakan program ini!")
                return
            else:
                print("❌ Perintah tidak dikenali.")

if __name__ == "__main__":
    main()
