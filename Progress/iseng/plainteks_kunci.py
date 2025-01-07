import tkinter as tk
from tkinter import filedialog, messagebox
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

def generate_keys():
    """Fungsi untuk membuat kunci RSA"""
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    
    with open("private.pem", "wb") as priv_file:
        priv_file.write(private_key)

    with open("public.pem", "wb") as pub_file:
        pub_file.write(public_key)
    
    messagebox.showinfo("Info", "Kunci RSA berhasil dibuat!")

def encrypt_message():
    """Fungsi untuk mengenkripsi pesan dari input pengguna"""
    message = entry_message.get()
    if not message:
        messagebox.showwarning("Peringatan", "Masukkan pesan untuk dienkripsi!")
        return

    public_key = RSA.import_key(open("public.pem").read())
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher_rsa.encrypt(message.encode('utf-8'))

    with open("encrypted_message.bin", "wb") as enc_file:
        enc_file.write(encrypted_message)
    
    messagebox.showinfo("Info", "Pesan berhasil dienkripsi! Disimpan di encrypted_message.bin")

def decrypt_message():
    """Fungsi untuk mendekripsi file encrypted_message.bin"""
    private_key = RSA.import_key(open("private.pem").read())
    cipher_rsa = PKCS1_OAEP.new(private_key)
    
    try:
        with open("encrypted_message.bin", "rb") as enc_file:
            encrypted_message = enc_file.read()
        
        decrypted_message = cipher_rsa.decrypt(encrypted_message)
        messagebox.showinfo("Info", f"Pesan setelah didekripsi: {decrypted_message.decode('utf-8')}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal mendekripsi pesan: {str(e)}")

# Buat tampilan GUI menggunakan Tkinter
root = tk.Tk()
root.title("Aplikasi Enkripsi RSA")
root.geometry("400x300")

label = tk.Label(root, text="Masukkan Pesan", font=("Helvetica", 12))
label.pack(pady=10)

entry_message = tk.Entry(root, width=50)
entry_message.pack(pady=5)

btn_generate_keys = tk.Button(root, text="Buat Kunci RSA", command=generate_keys)
btn_generate_keys.pack(pady=5)

btn_encrypt = tk.Button(root, text="Enkripsi Pesan", command=encrypt_message)
btn_encrypt.pack(pady=5)

btn_decrypt = tk.Button(root, text="Dekripsi Pesan", command=decrypt_message)
btn_decrypt.pack(pady=5)

root.mainloop()