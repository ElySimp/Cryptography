import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
import base64
import os
import re

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
        
        self.encrypt_python_button = tk.Button(root, text="Enkripsi File Python", width=20, command=self.encrypt_python_file)
        self.encrypt_python_button.pack(pady=10)
        
        self.decrypt_button = tk.Button(root, text="Dekripsi File", width=20, command=self.decrypt_file)
        self.decrypt_button.pack(pady=10)
        
        self.decrypt_python_button = tk.Button(root, text="Dekripsi File Python", width=20, command=self.decrypt_python_file)
        self.decrypt_python_button.pack(pady=10)
    
    def generate_encryption_key(self):
        return os.urandom(32)  # Kunci 256-bit

    def encrypt_file(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        with open(file_path, 'rb') as file:
            original_content = file.read()

        key = self.generate_encryption_key()
        
        cipher = AES.new(key, AES.MODE_EAX)
        encrypted_content, tag = cipher.encrypt_and_digest(original_content)
        
        nonce = base64.b64encode(cipher.nonce).decode('utf-8')
        tag_encoded = base64.b64encode(tag).decode('utf-8')
        encrypted_data = base64.b64encode(encrypted_content).decode('utf-8')
        key_encoded = base64.b64encode(key).decode('utf-8')

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

        with open(file_path, 'r', encoding='utf-8') as file:
            nonce, tag_encoded, encrypted_data = file.read().split('\n')
        
        # Create a simple dialog for the decryption key with a fixed size
        root = tk.Toplevel()
        root.geometry("300x150")  # Fixed size for the decryption key dialog
        root.title("Masukkan Kunci Dekripsi")
        
        tk.Label(root, text="Masukkan Kunci Dekripsi:").pack(pady=10)
        key_var = tk.StringVar()
        tk.Entry(root, textvariable=key_var, show="*").pack(pady=5)
        
        def submit_key():
            key_encoded = key_var.get()
            root.destroy()
            if not key_encoded:
                messagebox.showerror("Error", "Kunci dekripsi diperlukan")
                return
            
            try:
                key = base64.b64decode(key_encoded)
                nonce = base64.b64decode(nonce)
                tag = base64.b64decode(tag_encoded)
                encrypted_data = base64.b64decode(encrypted_data)
                
                cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
                decrypted_content = cipher.decrypt_and_verify(encrypted_data, tag)
                
                decrypted_file_path = file_path.replace('.enc', '.dec')
                with open(decrypted_file_path, 'wb') as file:
                    file.write(decrypted_content)
                
                messagebox.showinfo("Berhasil!", 
                    f"File berhasil didekripsi!\n\n"
                    f"File dekripsi: {decrypted_file_path}")
            except (ValueError, KeyError) as e:
                messagebox.showerror("Error", f"Dekripsi gagal. Mungkin kunci dekripsi salah atau file rusak. Error: {str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan tak terduga: {str(e)}")
        
        tk.Button(root, text="Submit", command=submit_key).pack(pady=10)
        root.mainloop()

    def encrypt_python_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if not file_path:
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            original_content = file.read()

        key = self.generate_encryption_key()
        
        cipher = AES.new(key, AES.MODE_EAX)
        encrypted_content, tag = cipher.encrypt_and_digest(original_content.encode('utf-8'))
        
        nonce = base64.b64encode(cipher.nonce).decode('utf-8')
        tag_encoded = base64.b64encode(tag).decode('utf-8')
        encrypted_data = base64.b64encode(encrypted_content).decode('utf-8')
        key_encoded = base64.b64encode(key).decode('utf-8')

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
    
    exec(decrypted_content)

if __name__ == "__main__":
    decrypt_and_run()
'''
        
        encrypted_file_path = file_path.replace('.py', '_encrypted.py')
        with open(encrypted_file_path, 'w', encoding='utf-8') as file:
            file.write(decryptor_template)
        
        self.root.clipboard_clear()
        self.root.clipboard_append(key_encoded)
        
        messagebox.showinfo("Berhasil!", 
            f"File Python berhasil dienkripsi!\n\n"
            f"File asli: {file_path}\n"
            f"File terenkripsi: {encrypted_file_path}\n\n"
            f"Kunci enkripsi: {key_encoded} (sudah disalin ke clipboard)")

    def decrypt_python_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Encrypted Files", "*_encrypted.py")])
        if not file_path:
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            encrypted_content = file.read()
        
        # Buat dialog sederhana untuk memasukkan kunci dekripsi dengan ukuran tetap
        root = tk.Toplevel()
        root.geometry("300x150")  # Ukuran tetap untuk dialog kunci dekripsi
        root.title("Masukkan Kunci Dekripsi")
        
        tk.Label(root, text="Masukkan Kunci Dekripsi:").pack(pady=10)
        key_var = tk.StringVar()
        tk.Entry(root, textvariable=key_var, show="*").pack(pady=5)
        
        def submit_key():
            key_encoded = key_var.get()
            root.destroy()
            if not key_encoded:
                messagebox.showerror("Error", "Kunci dekripsi diperlukan")
                return
            
            try:
                key = base64.b64decode(key_encoded)
                
                # Ekstrak nonce, tag, dan encrypted_data dengan benar
                nonce = re.search(r'nonce = base64.b64decode\("(.*?)"\)', encrypted_content).group(1)
                nonce = base64.b64decode(nonce)
                
                tag = re.search(r'tag = base64.b64decode\("(.*?)"\)', encrypted_content).group(1)
                tag = base64.b64decode(tag)
                
                encrypted_data = re.search(r'encrypted_data = base64.b64decode\("(.*?)"\)', encrypted_content).group(1)
                encrypted_data = base64.b64decode(encrypted_data)
                
                cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
                decrypted_content = cipher.decrypt_and_verify(encrypted_data, tag).decode('utf-8')
                
                decrypted_file_path = file_path.replace("_encrypted.py", "_decrypted.py")
                with open(decrypted_file_path, 'w', encoding='utf-8') as file:
                    file.write(decrypted_content)
                
                messagebox.showinfo("Berhasil!", 
                    f"File Python berhasil didekripsi!\n\n"
                    f"File dekripsi: {decrypted_file_path}")
            except (ValueError, KeyError) as e:
                messagebox.showerror("Error", f"Dekripsi gagal. Mungkin kunci dekripsi salah atau file rusak. Error: {str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan tak terduga: {str(e)}")
        
        tk.Button(root, text="Submit", command=submit_key).pack(pady=10)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileEncryptorApp(root)
    root.mainloop()