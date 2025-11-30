import sys

# tempat penyimpanan variabel yang dibuat oleh user di .sulc
env = {}

def eval_expr(expr):
    """
    Fungsi ini mencoba mengubah text menjadi nilai Python.
    Contoh:
        "5" -> 5
        "nama" -> nilai variabel 'nama'
        "3 + 2" -> 5
    Kalau gagal, dia balikin stringnya apa adanya.
    """
    try:
        return eval(expr, {}, env)
    except:
        return expr

def run_line(line):
    line = line.strip()

    # perintah tulis = print
    if line.startswith("tulis "):
        konten = line.replace("tulis ", "", 1)

        # "dan" artinya gabungkan string/value
        if " dan " in konten:
            bagian = konten.split(" dan ")
            hasil = ""
            for b in bagian:
                hasil += str(eval_expr(b.strip()))
            print(hasil)
        else:
            print(eval_expr(konten))
        return

    # perintah set = membuat variabel
    if line.startswith("set "):
        try:
            nama, nilai = line.replace("set ", "", 1).split(" = ")
            env[nama.strip()] = eval_expr(nilai.strip())
        except:
            print("Error set variabel:", line)
        return

    # kalau baris IF, interpreter hanya mendeteksi dulu
    # eksekusi bloknya dilakukan di run_file()
    if line.startswith("jika "):
        kondisi = line[5:].split(" maka")[0].strip()
        return ("IF", kondisi)

    # pengecekan loop, formatnya:
    # ulang i dari 0 sampai 3:
    if line.startswith("ulang "):
        try:
            isi = line.split()
            variabel = isi[1]
            awal = int(isi[3])
            akhir = int(isi[5].replace(":", ""))

            # sama seperti IF, loop hanya dideteksi dulu
            return ("LOOP", variabel, awal, akhir)
        except:
            print("Error loop:", line)
        return


def run_file(lines):
    """
    Fungsi utama yang membaca semua baris program.
    Di sini kita handle blok IF dan LOOP.
    """
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        if not line or line.startswith("#"):
            i += 1
            continue

        hasil = run_line(line)

        # ======== HANDLE IF ==========
        if hasil and hasil[0] == "IF":
            kondisi = hasil[1]
            blok = []

            # ambil baris-barus yang indent 4 spasi
            i += 1
            while i < len(lines) and lines[i].startswith("    "):
                blok.append(lines[i].strip())
                i += 1

            # kalau kondisi benar -> jalankan blok
            if eval_expr(kondisi):
                for b in blok:
                    run_line(b)

            continue

        # ======== HANDLE LOOP ==========
        if hasil and hasil[0] == "LOOP":
            var, awal, akhir = hasil[1], hasil[2], hasil[3]
            blok = []

            i += 1
            while i < len(lines) and lines[i].startswith("    "):
                blok.append(lines[i].strip())
                i += 1

            # jalankan loop
            for x in range(awal, akhir + 1):
                env[var] = x   # update nilai variabel loop
                for b in blok:
                    run_line(b)

            continue

        i += 1


def repl():
    print("Sulacode REPL (ketik 'exit' buat keluar)")
    while True:
        cmd = input("> ")
        if cmd == "exit":
            break
        run_line(cmd)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        repl()
    else:
        with open(sys.argv[1], "r", encoding="utf8") as f:
            run_file(f.readlines())
