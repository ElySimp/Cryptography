import flet as ft
import random


def fpb_euclidean(a, b):
    while b:
        a, b = b, a % b
    return a


def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


def cari_invers_modular(a, m):
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


def enkripsi_rsa(p, q):
    if not (is_prime(p) and is_prime(q)):
        return None, None, None, "P dan Q harus bilangan prima."
    if p == q:
        return None, None, None, "P dan Q tidak boleh sama."

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randint(2, phi - 1)  # Memilih e secara acak
    while fpb_euclidean(e, phi) != 1:
        e = random.randint(2, phi - 1)

    d = cari_invers_modular(e, phi)
    if d is None:
        return None, None, None, "Tidak dapat menemukan invers modular."

    return n, e, d, None


def main(page: ft.Page):
    page.title = "Enkripsi RSA"

    p_input = ft.TextField(label="Masukkan P (bilangan prima)", width=200)
    q_input = ft.TextField(label="Masukkan Q (bilangan prima)", width=200)
    pesan_input = ft.TextField(label="Masukkan pesan", multiline=True, min_lines=3, width=400)
    n_text = ft.Text()
    e_text = ft.Text()
    d_text = ft.Text()
    enkripsi_text = ft.Text()
    dekripsi_text = ft.Text()
    error_text = ft.Text(color=ft.colors.RED)

    def enkripsi_klik(e):
        try:
            p = int(p_input.value)
            q = int(q_input.value)
        except ValueError:
            error_text.value = "Input P dan Q harus berupa angka."
            page.update()
            return

        n, pub, priv, error = enkripsi_rsa(p, q)
        if error:
            error_text.value = error
            page.update()
            return

        n_text.value = f"n = {n}"
        e_text.value = f"Kunci Publik (n, e): ({n}, {pub})"
        d_text.value = f"Kunci Privat (n, d): ({n}, {priv})"

        pesan = pesan_input.value
        pesan_numerik = [ord(char) for char in pesan]
        enkripsi = [(m ** pub) % n for m in pesan_numerik]
        enkripsi_text.value = f"Pesan Terenkripsi: {enkripsi}"

        dekripsi = [(c ** priv) % n for c in enkripsi]
        pesan_dekripsi = "".join([chr(num) for num in dekripsi])
        dekripsi_text.value = f"Pesan Dekripsi: {pesan_dekripsi}"

        error_text.value = ""
        page.update()

    enkripsi_button = ft.ElevatedButton("Enkripsi", on_click=enkripsi_klik)

    page.add(
        p_input,
        q_input,
        ft.Row([enkripsi_button]),
        ft.Column([n_text, e_text, d_text]),
        pesan_input,
        ft.Column([enkripsi_text, dekripsi_text]),
        error_text
    )


ft.app(target=main)