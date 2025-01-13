import flet as ft
from math import gcd
from sympy import mod_inverse, isprime


def HitungRSA(p, q):
    if not (isprime(p) and isprime(q)):
        raise ValueError("Nilai p dan q harus bilangan prima.")
    if p == q:
        raise ValueError("Nilai p dan q tidak boleh sama.")

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 2
    while e < phi and gcd(e, phi) != 1:
        e += 1

    d = mod_inverse(e, phi)
    return n, phi, e, d


def main(page: ft.Page):
    page.title = "RSA Encryption/Decryption"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    hasil_enkripsi = ft.Text()
    hasil_perhitungan = ft.Text()
    hasil_dekripsi = ft.Text()

    # Enkripsi UI
    p_input = ft.TextField(label="Nilai p", width=150)
    q_input = ft.TextField(label="Nilai q", width=150)
    plaintext_input = ft.TextField(label="Plaintext", width=300)

    def proses_enkripsi(e):
        try:
            p = int(p_input.value)
            q = int(q_input.value)
            plaintext = plaintext_input.value

            n, phi, e, d = HitungRSA(p, q)
            ciphertext = [pow(ord(char), e, n) for char in plaintext]

            hasil_perhitungan.value = (f"=== Perhitungan RSA ===\n"
                                       f"p = {p}, q = {q}\n"
                                       f"n = p * q = {n}\n"
                                       f"phi = (p-1) * (q-1) = {phi}\n"
                                       f"e dipilih sebagai bilangan relatif prima terhadap phi: e = {e}\n"
                                       f"d adalah invers modulo dari e dan phi: d = {d}\n"
                                       f"Kunci Publik: ({e}, {n})\n"
                                       f"Kunci Privat: ({d}, {n})\n")
            hasil_enkripsi.value = f"Ciphertext: {ciphertext}"
            page.update()
        except ValueError as ve:
            hasil_enkripsi.value = f"Error: {ve}"
            page.update()

    encrypt_button = ft.ElevatedButton("Enkripsi", on_click=proses_enkripsi)

    # Dekripsi UI
    ciphertext_input = ft.TextField(label="Ciphertext", width=300)
    d_input = ft.TextField(label="Kunci privat (d)", width=150)
    n_input = ft.TextField(label="Nilai n", width=150)

    def proses_dekripsi(e):
        try:
            ciphertext = [int(x) for x in ciphertext_input.value.strip('[]').split(',')]
            private_d = int(d_input.value)
            n = int(n_input.value)

            plaintext = ''.join([chr(pow(char, private_d, n)) for char in ciphertext])
            hasil_dekripsi.value = f"Plaintext: {plaintext}"
            page.update()
        except ValueError as ve:
            hasil_dekripsi.value = f"Error: {ve}"
            page.update()

    decrypt_button = ft.ElevatedButton("Dekripsi", on_click=proses_dekripsi)

    tab_enkripsi = ft.Column([
        ft.Row([p_input, q_input]),
        plaintext_input,
        encrypt_button,
        hasil_perhitungan,
        hasil_enkripsi,
    ])

    tab_dekripsi = ft.Column([
        ciphertext_input,
        ft.Row([d_input, n_input]),
        decrypt_button,
        hasil_dekripsi,
    ])

    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Enkripsi", content=tab_enkripsi),
            ft.Tab(text="Dekripsi", content=tab_dekripsi),
        ]
    )

    page.add(tabs)


ft.app(target=main)