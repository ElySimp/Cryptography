def fpb_euclidean(a, b):
    """Mencari FPB menggunakan algoritma Euclidean."""
    while b:
        a, b = b, a % b
    return a


def enkripsi_rsa():
    p = input("Masukkan P (bilangan prima): ")
    q = input("Masukkan Q (bilangan prima): ")

    try:
        p = int(p)
        q = int(q)
        if not (is_prime(p) and is_prime(q)):  # Memastikan input adalah bilangan prima
            raise ValueError("P dan Q harus bilangan prima.")
        if p == q:  # Memastikan p dan q berbeda
            raise ValueError("P dan Q tidak boleh sama.")
    except ValueError as e:
        print(f"Input tidak valid: {e}")
        return

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 2  # Mulai dari angka terkecil yang mungkin
    while True:
        if fpb_euclidean(e, phi) == 1:
            break
        e += 1
        if e >= phi:  # mencegah infinite loop jika tidak ada e yang memenuhi
            print("Tidak ditemukan nilai e yang memenuhi.")
            return

    # hitung d
    d = cari_invers_modular(e, phi)
    if d is None:
        print("Tidak dapat menemukan invers modular.")
        return

    print(f"n = {n}")
    print(f"phi(n) = {phi}")
    print(f"Kunci Publik (n, e): ({n}, {e})")
    print(f"Kunci Privat (n, d): ({n}, {d})")
    return n, e, d


def is_prime(num):
    """Memeriksa apakah angka adalah bilangan prima."""
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


def cari_invers_modular(a, m):
    """Mencari invers modular menggunakan Extended Euclidean Algorithm."""
    m_asli = m
    y = 0
    x = 1

    if (m == 1):
        return 0

    while (a > 1):
        q = a // m
        t = m

        m = a % m
        a = t
        t = y

        y = x - q * y
        x = t

    if (x < 0):
        x = x + m_asli

    return x


# Contoh penggunaan
n, e, d = enkripsi_rsa()
if n is not None:
    pesan = input("Masukkan pesan yang akan dienkripsi: ")
    pesan_numerik = [ord(char) for char in pesan]
    print("Pesan numerik:", pesan_numerik)

    enkripsi = [(m ** e) % n for m in pesan_numerik]
    print("Pesan terenkripsi:", enkripsi)

    dekripsi = [(c ** d) % n for c in enkripsi]
    print("Pesan dekripsi numerik:", dekripsi)

    pesan_dekripsi = "".join([chr(num) for num in dekripsi])
    print("Pesan dekripsi:", pesan_dekripsi)

