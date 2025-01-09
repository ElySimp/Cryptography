import tkinter as tk
from tkinter import messagebox
from math import gcd
from sympy import mod_inverse, isprime

# Global variables to share between pages
NilaiN, NilaiE, NilaiD = None, None, None
Ciphertext = None

# Fungsi untuk menghitung nilai n, phi, dan kunci publik/privat
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

# Halaman utama untuk memilih enkripsi atau dekripsi
def HalamanUtama():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Pilih Operasi").pack(pady=20)
    tk.Button(root, text="Enkripsi", command=HalamanEnkripsi).pack(pady=10)
    tk.Button(root, text="Dekripsi", command=HalamanDekripsi).pack(pady=10)

# Halaman untuk enkripsi
def HalamanEnkripsi():
    def ProsesEnkripsi():
        try:
            p = int(EntryP.get())
            q = int(EntryQ.get())
            plaintext = EntryPlaintext.get()

            n, phi, e, d = HitungRSA(p, q)
            global NilaiN, NilaiE, NilaiD, Ciphertext
            NilaiN, NilaiE, NilaiD = n, e, d

            Ciphertext = [(ord(char) ** e) % n for char in plaintext]

            # Cetak perhitungan di terminal
            print("=== Perhitungan RSA ===")
            print(f"p = {p}, q = {q}")
            print(f"n = p * q = {n}")
            print(f"phi = (p-1) * (q-1) = {phi}")
            print(f"e dipilih sebagai bilangan terkecil yang relatif prima dengan phi: e = {e}")
            print(f"d adalah invers modulo dari e dan phi: d = {d}")
            print(f"Kunci Publik: ({e}, {n})")
            print(f"Kunci Privat: ({d}, {n})")
            print(f"Ciphertext (hasil enkripsi): {Ciphertext}")

            HasilEnkripsi.set(f"Ciphertext: {Ciphertext}")

        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def SalinCiphertext():
        if Ciphertext:
            root.clipboard_clear()
            root.clipboard_append(str(Ciphertext))
            root.update()
            messagebox.showinfo("Salin", "Ciphertext berhasil disalin ke clipboard.")
        else:
            messagebox.showwarning("Peringatan", "Tidak ada ciphertext untuk disalin.")

    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Halaman Enkripsi").pack(pady=10)

    tk.Label(root, text="Masukkan nilai p:").pack()
    EntryP = tk.Entry(root)
    EntryP.pack()

    tk.Label(root, text="Masukkan nilai q:").pack()
    EntryQ = tk.Entry(root)
    EntryQ.pack()

    tk.Label(root, text="Masukkan plaintext:").pack()
    EntryPlaintext = tk.Entry(root)
    EntryPlaintext.pack()

    HasilEnkripsi = tk.StringVar()
    tk.Button(root, text="Enkripsi", command=ProsesEnkripsi).pack(pady=10)
    tk.Label(root, textvariable=HasilEnkripsi).pack(pady=10)

    tk.Button(root, text="Salin Ciphertext", command=SalinCiphertext).pack(pady=5)
    tk.Button(root, text="Kembali", command=HalamanUtama).pack(pady=10)

# Halaman untuk dekripsi
def HalamanDekripsi():
    def ProsesDekripsi():
        try:
            ciphertext = EntryCiphertext.get()
            public_e = int(EntryPublicE.get())
            private_d = int(EntryPrivateD.get())
            n = int(EntryN.get())

            if public_e != NilaiE or private_d != NilaiD or n != NilaiN:
                raise ValueError("Kunci publik atau privat tidak cocok dengan ciphertext.")

            ciphertext = [int(x) for x in ciphertext.strip('[]').split(', ')]
            plaintext = ''.join([chr((char ** private_d) % n) for char in ciphertext])
            HasilDekripsi.set(f"Plaintext: {plaintext}")

        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Halaman Dekripsi").pack(pady=10)

    tk.Label(root, text="Masukkan ciphertext:").pack()
    EntryCiphertext = tk.Entry(root)
    EntryCiphertext.pack()

    tk.Label(root, text="Masukkan kunci publik (e):").pack()
    EntryPublicE = tk.Entry(root)
    EntryPublicE.pack()

    tk.Label(root, text="Masukkan kunci privat (d):").pack()
    EntryPrivateD = tk.Entry(root)
    EntryPrivateD.pack()

    tk.Label(root, text="Masukkan nilai n:").pack()
    EntryN = tk.Entry(root)
    EntryN.pack()

    HasilDekripsi = tk.StringVar()
    tk.Button(root, text="Dekripsi", command=ProsesDekripsi).pack(pady=10)
    tk.Label(root, textvariable=HasilDekripsi).pack(pady=10)

    tk.Button(root, text="Kembali", command=HalamanUtama).pack(pady=10)

# Root Tkinter
root = tk.Tk()
root.title("RSA Encryption/Decryption")
HalamanUtama()
root.mainloop()