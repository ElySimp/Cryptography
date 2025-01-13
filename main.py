import tkinter as tk
from tkinter import messagebox

NilaiN, NilaiE, NilaiD = None, None, None
Ciphertext = None

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    e = e % phi
    for x in range(1, phi):
        if (e * x) % phi == 1:
            return x
    raise ValueError("Tidak ditemukan invers modulo untuk e dan phi.")

def HitungRSA(p, q):
    if p <= 1 or q <= 1:
        raise ValueError("Nilai p dan q harus bilangan prima lebih dari 1.")
    if not (is_prima(p) and is_prima(q)):
        raise ValueError("Nilai p dan q harus bilangan prima.")
    if p == q:
        raise ValueError("Nilai p dan q tidak boleh sama.")

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 2
    while e < phi and gcd(e, phi) != 1:
        e += 1

    if e >= phi:
        raise ValueError("Tidak ditemukan nilai e yang relatif prima dengan phi.")

    d = mod_inverse(e, phi)
    return n, phi, e, d

def is_prima(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def HalamanUtama():
    for widget in root.winfo_children():
        widget.destroy()
    

    tk.Label(root, text="Pilih Operasi",width=500, height=2, font=("Montserrat", 18, "bold"), bg="#12100E", fg="#F0F0F0").pack(pady=(0,20))
    tk.Label(root, text="Silahkan pilih operasi yang ingin dilakukan", font=("Montserrat", 12, "bold")).pack(pady=30)
    tk.Button(root, text="🔒 Enkripsi", font=("Montserrat", 16, "bold"), bg="#788488", fg="#F0F0F0", command=HalamanEnkripsi).pack(pady=20)
    tk.Button(root, text="🔓 Dekripsi", font=("Montserrat", 16, "bold"), bg="#788488", fg="#F0F0F0", command=HalamanDekripsi).pack(pady=10)

# Halaman untuk enkripsi
def HalamanEnkripsi():
    def ProsesEnkripsi():
        try:
            p = int(EntryP.get())
            q = int(EntryQ.get())
            plaintext = EntryPlaintext.get()

            if p < 7 or q < 7:
                raise ValueError("Nilai p dan q harus minimal 7.")
                
            n, phi, e, d = HitungRSA(p, q)
            global NilaiN, NilaiE, NilaiD, Ciphertext
            NilaiN, NilaiE, NilaiD = n, e, d

            Ciphertext = []
            print("\n=== Perhitungan RSA ===")
            print(f"p = {p}, q = {q}")
            print(f"n = p * q = {n}")
            print(f"phi = (p-1) * (q-1) = {phi}")
            print(f"e dipilih sebagai bilangan terkecil yang relatif prima dengan phi: e = {e}")
            print(f"d adalah invers modulo dari e dan phi: d = {d}")
            print(f"Kunci Publik: ({e}, {n})")
            print(f"Kunci Privat: ({d}, {n})")

            for char in plaintext:
                m = ord(char)
                cipher = pow(m, e, n)
                Ciphertext.append(cipher)
                print(f"Karakter '{char}' -> ASCII {m} -> (m^e) mod n = ({m}^{e}) mod {n} = {cipher}")

            print(f"Ciphertext (hasil enkripsi): {Ciphertext}")
            HasilEnkripsi.set(f"Ciphertext : {Ciphertext}")

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

    tk.Label(root, text="Halaman Enkripsi",width=500, height=2, font=("Montserrat", 18, "bold"), bg="#12100E", fg="#F0F0F0").pack(pady=(0,20))

    tk.Label(root, text="Masukkan nilai p :", font=("Montserrat", 12, "bold")).pack(pady=10)
    EntryP = tk.Entry(root, width=25)
    EntryP.pack()

    tk.Label(root, text="Masukkan nilai q :",  font=("Montserrat", 12, "bold")).pack(pady=10)
    EntryQ = tk.Entry(root, width=25)
    EntryQ.pack()

    tk.Label(root, text="Masukkan plaintext:",  font=("Montserrat", 12, "bold")).pack(pady=10)
    EntryPlaintext = tk.Entry(root, width=25)
    EntryPlaintext.pack()

    HasilEnkripsi = tk.StringVar()
    tk.Button(root, text="Enkripsi",  font=("Montserrat", 12, "bold"), bg="#788488", fg="#F0F0F0", command=ProsesEnkripsi).pack(pady=20)
    tk.Label(root, textvariable=HasilEnkripsi).pack()

    tk.Button(root, text="Salin Ciphertext",  font=("Montserrat", 12, "bold"), bg="#788488", fg="#F0F0F0", command=SalinCiphertext).pack(pady=10)
    tk.Button(root, text="Kembali",  font=("Montserrat", 12, "bold"), bg="#788488", fg="#F0F0F0", command=HalamanUtama).pack(pady=5)

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
            HasilDekripsi.set(f"Plaintext : {plaintext}")

        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Halaman Dekripsi",width=500, height=2, font=("Montserrat", 18, "bold"), bg="#12100E", fg="#F0F0F0").pack(pady=(0,20))

    tk.Label(root, text="Masukkan ciphertext :", font=("Montserrat", 12, "bold")).pack(pady=10)
    EntryCiphertext = tk.Entry(root, width=25)
    EntryCiphertext.pack()

    tk.Label(root, text="Masukkan kunci publik (e) :",  font=("Montserrat", 12, "bold")).pack(pady=10)
    EntryPublicE = tk.Entry(root, width=25)
    EntryPublicE.pack()

    tk.Label(root, text="Masukkan kunci privat (d) :",  font=("Montserrat", 12, "bold")).pack(pady=10)
    EntryPrivateD = tk.Entry(root, width=25)
    EntryPrivateD.pack()

    tk.Label(root, text="Masukkan nilai n :",  font=("Montserrat", 12, "bold")).pack(pady=10)
    EntryN = tk.Entry(root, width=25)
    EntryN.pack()

    HasilDekripsi = tk.StringVar()
    tk.Button(root, text="Dekripsi",  font=("Montserrat", 12, "bold"), bg="#788488", fg="#F0F0F0", command=ProsesDekripsi).pack(pady=20)
    tk.Label(root, textvariable=HasilDekripsi).pack()

    tk.Button(root, text="Kembali",  font=("Montserrat", 12, "bold"), bg="#788488", fg="#F0F0F0", command=HalamanUtama).pack(pady=10)

# Root Tkinter
root = tk.Tk()
root.title("RSA Encryption/Decryption")
root.geometry("500x525")
root.configure(bg="#F0F0F0")
HalamanUtama()
root.mainloop()