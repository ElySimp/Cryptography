import tkinter as tk
from tkinter import filedialog, messagebox
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
import base64
import os


class FileEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enkripsi/Dekripsi File")
        self.root.geometry("400x300")

        # Generate RSA keys
        self.private_key = RSA.generate(2048)
        self.public_key = self.private_key.publickey()

        # Labels and buttons
        tk.Label(root, text="Enkripsi/Dekripsi File", font=("Helvetica", 16)).pack(pady=10)

        self.encrypt_button = tk.Button(root, text="Enkripsi File", width=20, command=self.encrypt_file)
        self.encrypt_button.pack(pady=10)

        self.decrypt_button = tk.Button(root, text="Dekripsi File", width=20, command=self.decrypt_file)
        self.decrypt_button.pack(pady=10)

    def generate_encryption_key(self):
        return os.urandom(32)  # Kunci 256-bit

    def encrypt_file(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        # Baca file dalam binary mode
        with open(file_path, 'rb') as file:
            original_content = file.read()

        key = self.generate_encryption_key()
        cipher = AES.new(key, AES.MODE_EAX)
        encrypted_content, tag = cipher.encrypt_and_digest(original_content)

        # Encode hasil enkripsi ke Base64
        nonce = base64.b64encode(cipher.nonce).decode('utf-8')
        tag_encoded = base64.b64encode(tag).decode('utf-8')
        encrypted_data = base64.b64encode(encrypted_content).decode('utf-8')
        key_encoded = base64.b64encode(key).decode('utf-8')

        # Simpan file terenkripsi
        encrypted_file_path = file_path + '.enc'
        with open(encrypted_file_path, 'w', encoding='utf-8') as file:
            file.write(f"{nonce}\n{tag_encoded}\n{encrypted_data}")

        self.root.clipboard_clear()
        self.root.clipboard_append(key_encoded)

        messagebox.showinfo("Berhasil!",
                            f"File berhasil dienkripsi!\n\n"
                            f"File asli: {file_path}\n"
                            f"File terenkripsi: {encrypted_file_path}\n\n"
                            f"Kunci enkripsi: {key_encoded} (sudah disalin ke clipboard)")

    def decrypt_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.enc")])
        if not file_path:
            return

        # Buka file terenkripsi
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.read().split('\n')
                if len(lines) < 3:  # Validasi jumlah baris
                    messagebox.showerror("Error", "File terenkripsi tidak valid atau rusak.")
                    return

                # Ambil data terenkripsi
                nonce = base64.b64decode(lines[0])
                tag = base64.b64decode(lines[1])
                encrypted_data = base64.b64decode(lines[2])

        except Exception as e:
            messagebox.showerror("Error", f"Gagal membaca file: {str(e)}")
            return

        # Minta kunci dekripsi
        key_encoded = self.ask_for_key()
        if not key_encoded:
            return

        try:
            key = base64.b64decode(key_encoded)
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            decrypted_content = cipher.decrypt_and_verify(encrypted_data, tag)

            # Simpan hasil dekripsi dalam binary mode
            decrypted_file_path = file_path.replace('.enc', '_decrypted')
            with open(decrypted_file_path, 'wb') as file:
                file.write(decrypted_content)

            messagebox.showinfo("Berhasil!",
                                f"File berhasil didekripsi!\n\n"
                                f"File dekripsi: {decrypted_file_path}")
        except (ValueError, KeyError):
            messagebox.showerror("Error", "Kunci dekripsi salah atau file rusak.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

    def ask_for_key(self):
        # Membuat dialog sederhana untuk memasukkan kunci dekripsi
        root = tk.Toplevel()
        root.geometry("300x150")
        root.title("Masukkan Kunci Dekripsi")

        tk.Label(root, text="Masukkan Kunci Dekripsi:").pack(pady=10)
        key_var = tk.StringVar()
        tk.Entry(root, textvariable=key_var, show="*").pack(pady=5)

        def submit_key():
            root.destroy()

        tk.Button(root, text="Submit", command=submit_key).pack(pady=10)
        root.wait_window()

        return key_var.get()


if __name__ == "__main__":
    root = tk.Tk()
    app = FileEncryptorApp(root)
    root.mainloop()
