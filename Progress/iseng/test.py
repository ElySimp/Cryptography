import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from Cryptodome.Cipher import AES
import os
import base64

class FileEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python File Encryptor")
        
        self.encrypt_button = tk.Button(root, text="Encrypt Python File", command=self.encrypt_python_file)
        self.encrypt_button.pack(pady=10)

    def generate_encryption_key(self):
        return os.urandom(32)  # 256-bit key

    def encrypt_python_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if not file_path:
            return

        # Baca isi file
        with open(file_path, 'r', encoding='utf-8') as file:
            original_content = file.read()

        # Generate kunci enkripsi
        key = self.generate_encryption_key()
        
        # Buat cipher AES
        cipher = AES.new(key, AES.MODE_EAX)
        
        # Enkripsi konten
        encrypted_content, tag = cipher.encrypt_and_digest(original_content.encode('utf-8'))
        
        # Encode data
        nonce = base64.b64encode(cipher.nonce).decode('utf-8')
        tag_encoded = base64.b64encode(tag).decode('utf-8')
        encrypted_data = base64.b64encode(encrypted_content).decode('utf-8')
        key_encoded = base64.b64encode(key).decode('utf-8')

        # Template dekriptor
        decryptor_template = f'''
import base64
from Cryptodome.Cipher import AES

def decrypt_and_run():
    key = base64.b64decode("{key_encoded}")
    nonce = base64.b64decode("{nonce}")
    tag = base64.b64decode("{tag_encoded}")
    encrypted_data = base64.b64decode("{encrypted_data}")
    
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted_content = cipher.decrypt_and_verify(encrypted_data, tag).decode('utf-8')
    
    # Jalankan konten yang didekripsi
    exec(decrypted_content)

if __name__ == "__main__":
    decrypt_and_run()
'''
        
        # Simpan file terenkripsi
        encrypted_file_path = file_path.replace('.py', '_encrypted.py')
        with open(encrypted_file_path, 'w', encoding='utf-8') as file:
            file.write(decryptor_template)
        
        # Salin password ke clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(key_encoded)
        
        messagebox.showinfo("Sukses", 
            f"File Python berhasil dienkripsi!\n\n"
            f"File asli: {file_path}\n"
            f"File terenkripsi: {encrypted_file_path}\n\n"
            f"Kunci rahasia sudah disalin ke clipboard.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileEncryptorApp(root)
    root.mainloop()