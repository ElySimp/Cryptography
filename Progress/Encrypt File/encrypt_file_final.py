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
        self.root.title("File Encryptor/Decryptor")
        self.root.geometry("500x425")
        self.root.configure(bg="#97c7e0")

        self.private_key = RSA.generate(2048)
        self.public_key = self.private_key.publickey()

        tk.Label(root, text="Enkripsi/Dekripsi File",width=300, height=2, font=("Montserrat", 24, "bold"), bg="#5AA6CF").pack(pady=(0,25))

        self.encrypt_button = tk.Button(root, text="🔒 Encrypt File", font=(16), width=25, command=self.encrypt_file)
        self.encrypt_button.pack(pady=10)

        self.encrypt_python_button = tk.Button(root, text="🔒🐍 Encrypt Python File", font=(16), width=25,  command=self.encrypt_python_file)
        self.encrypt_python_button.pack(pady=10)

        self.decrypt_button = tk.Button(root, text="🔓 Decrypt File", font=(16), width=25, command=self.decrypt_file)
        self.decrypt_button.pack(pady=10)

        self.decrypt_python_button = tk.Button(root, text="🔓🐍 Decrypt Python File", font=(16), width=25, command=self.decrypt_python_file)
        self.decrypt_python_button.pack(pady=10)

        print("private key:", self.private_key.export_key().decode('utf-8'))   
        print("p key:", self.public_key.export_key().decode('utf-8'))   

    def generate_encryption_key(self):
        return os.urandom(32)  # 256-bit AES key

    def encrypt_file(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        with open(file_path, 'rb') as file:
            original_content = file.read()

        aes_key = self.generate_encryption_key()
        
        cipher = AES.new(aes_key, AES.MODE_EAX)
        encrypted_content, tag = cipher.encrypt_and_digest(original_content)

        rsa_cipher = PKCS1_OAEP.new(self.public_key)
        encrypted_aes_key = rsa_cipher.encrypt(aes_key)

        nonce = base64.b64encode(cipher.nonce).decode('utf-8')
        tag_encoded = base64.b64encode(tag).decode('utf-8')
        encrypted_data = base64.b64encode(encrypted_content).decode('utf-8')
        encrypted_aes_key_encoded = base64.b64encode(encrypted_aes_key).decode('utf-8')

        encrypted_file_path = file_path + '.enc'
        with open(encrypted_file_path, 'w', encoding='utf-8') as file:
            file.write(f"{nonce}\n{tag_encoded}\n{encrypted_data}\n{encrypted_aes_key_encoded}")

        self.root.clipboard_clear()
        self.root.clipboard_append(encrypted_aes_key_encoded)

        messagebox.showinfo("Success", 
            f"File encrypted successfully!\n\n"
            f"Original file: {file_path}\n"
            f"Encrypted file: {encrypted_file_path}\n\n"
            f"Encryption key: {encrypted_aes_key_encoded} (copied to clipboard)")

    def decrypt_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.enc")])
        if not file_path:
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            nonce, tag_encoded, encrypted_data, encrypted_aes_key_encoded = file.read().split('\n')
        
        key_encoded = simpledialog.askstring("Decryption Key", "Enter the decryption key:")
        if not key_encoded:
            messagebox.showerror("Error", "Decryption key is required")
            return

        try:
            encrypted_aes_key = base64.b64decode(encrypted_aes_key_encoded)
            rsa_cipher = PKCS1_OAEP.new(self.private_key)
            aes_key = rsa_cipher.decrypt(encrypted_aes_key)

            nonce = base64.b64decode(nonce)
            tag = base64.b64decode(tag_encoded)
            encrypted_data = base64.b64decode(encrypted_data)
            
            cipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
            decrypted_content = cipher.decrypt_and_verify(encrypted_data, tag)
            
            decrypted_file_path = file_path.replace('.enc', '.dec')
            with open(decrypted_file_path, 'wb') as file:
                file.write(decrypted_content)
            
            messagebox.showinfo("Success", 
                f"File decrypted successfully!\n\n"
                f"Decrypted file: {decrypted_file_path}")
        except (ValueError, KeyError) as e:
            messagebox.showerror("Error", f"Decryption failed. The decryption key might be incorrect or the file might be corrupted. Error: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def encrypt_python_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if not file_path:
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            original_content = file.read()

        aes_key = self.generate_encryption_key()
        
        cipher = AES.new(aes_key, AES.MODE_EAX)
        encrypted_content, tag = cipher.encrypt_and_digest(original_content.encode('utf-8'))

        rsa_cipher = PKCS1_OAEP.new(self.public_key)
        encrypted_aes_key = rsa_cipher.encrypt(aes_key)

        nonce = base64.b64encode(cipher.nonce).decode('utf-8')
        tag_encoded = base64.b64encode(tag).decode('utf-8')
        encrypted_data = base64.b64encode(encrypted_content).decode('utf-8')
        encrypted_aes_key_encoded = base64.b64encode(encrypted_aes_key).decode('utf-8')

        private_key_pem = self.private_key.export_key().decode('utf-8')

        decryptor_template = f'''
import base64
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA

def decrypt_and_run():
    encrypted_aes_key_encoded = "{encrypted_aes_key_encoded}"
    encrypted_aes_key = base64.b64decode(encrypted_aes_key_encoded)

    # Load RSA private key
    private_key_pem = \"\"\"{private_key_pem}\"\"\"
    private_key = RSA.import_key(private_key_pem)

    # Decrypt AES key using RSA private key
    rsa_cipher = PKCS1_OAEP.new(private_key)
    aes_key = rsa_cipher.decrypt(encrypted_aes_key)

    # Decrypt file content
    nonce = base64.b64decode("{nonce}")
    tag = base64.b64decode("{tag_encoded}")
    encrypted_data = base64.b64decode("{encrypted_data}")
    
    cipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
    decrypted_content = cipher.decrypt_and_verify(encrypted_data, tag).decode('utf-8')

    # Execute the decrypted content
    exec(decrypted_content)

if __name__ == "__main__":
    decrypt_and_run()
'''

        encrypted_file_path = file_path.replace('.py', '_encrypted.py')
        with open(encrypted_file_path, 'w', encoding='utf-8') as file:
            file.write(decryptor_template)

        self.root.clipboard_clear()
        self.root.clipboard_append(encrypted_aes_key_encoded)

        messagebox.showinfo("Success", 
            f"Python file encrypted successfully!\n\n"
            f"Original file: {file_path}\n"
            f"Encrypted file: {encrypted_file_path}\n\n"
            f"Encryption key: {encrypted_aes_key_encoded} (copied to clipboard)")


    def decrypt_python_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Encrypted Files", "*_encrypted.py")])
        if not file_path:
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            encrypted_content = file.read()

        key_encoded = simpledialog.askstring("Decryption Key", "Enter the decryption key:")
        if not key_encoded:
            messagebox.showerror("Error", "Decryption key is required")
            return

        try:
            encrypted_aes_key = base64.b64decode(key_encoded)
            
            rsa_cipher = PKCS1_OAEP.new(self.private_key)
            aes_key = rsa_cipher.decrypt(encrypted_aes_key)

            nonce = re.search(r'nonce = base64.b64decode\("(.*?)"\)', encrypted_content).group(1)
            nonce = base64.b64decode(nonce)
            
            tag = re.search(r'tag = base64.b64decode\("(.*?)"\)', encrypted_content).group(1)
            tag = base64.b64decode(tag)
            
            encrypted_data = re.search(r'encrypted_data = base64.b64decode\("(.*?)"\)', encrypted_content).group(1)
            encrypted_data = base64.b64decode(encrypted_data)

            cipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
            decrypted_content = cipher.decrypt_and_verify(encrypted_data, tag).decode('utf-8')

            decrypted_file_path = file_path.replace("_encrypted.py", "_decrypted.py")
            with open(decrypted_file_path, 'w', encoding='utf-8') as file:
                file.write(decrypted_content)

            messagebox.showinfo("Success", 
                f"Python file decrypted successfully!\n\n"
                f"Decrypted file: {decrypted_file_path}")
        except (ValueError, KeyError) as e:
            messagebox.showerror("Error", f"Decryption failed. The decryption key might be incorrect or the file might be corrupted. Error: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileEncryptorApp(root)
    root.mainloop()