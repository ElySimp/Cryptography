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
        
        # Generate RSA keys
        self.private_key = RSA.generate(2048)
        self.public_key = self.private_key.publickey()

        # Buttons for each feature
        self.encrypt_button = tk.Button(root, text="Encrypt File", command=self.encrypt_file)
        self.encrypt_button.pack(pady=10)
        
        self.encrypt_python_button = tk.Button(root, text="Encrypt Python File", command=self.encrypt_python_file)
        self.encrypt_python_button.pack(pady=10)
        
        self.decrypt_button = tk.Button(root, text="Decrypt File", command=self.decrypt_python_file)
        self.decrypt_button.pack(pady=10)
        
        self.decrypt_python_button = tk.Button(root, text="Decrypt Python File", command=self.decrypt_python_file)
        self.decrypt_python_button.pack(pady=10)
    
    def generate_encryption_key(self):
        return os.urandom(32)  # 256-bit key

    def encrypt_file(self):
        # Encryption logic for general files
        pass
    
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
        
        messagebox.showinfo("Success", 
            f"Python file encrypted successfully!\n\n"
            f"Original file: {file_path}\n"
            f"Encrypted file: {encrypted_file_path}\n\n"
            f"Encryption key: {key_encoded} (copied to clipboard)")

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
            key = base64.b64decode(key_encoded)
            
            nonce = re.search(r'base64.b64decode\("(.*?)"\)', encrypted_content).group(1)
            nonce = base64.b64decode(nonce)
            
            tag = re.search(r'base64.b64decode\("(.*?)"\)', encrypted_content[encrypted_content.find("tag") :]).group(1)
            tag = base64.b64decode(tag)
            
            encrypted_data = re.search(r'base64.b64decode\("(.*?)"\)', encrypted_content[encrypted_content.find("encrypted_data") :]).group(1)
            encrypted_data = base64.b64decode(encrypted_data)
            
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
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