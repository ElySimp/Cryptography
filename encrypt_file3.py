import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
import base64
import os

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
        
        self.decrypt_button = tk.Button(root, text="Decrypt File", command=self.decrypt_file)
        self.decrypt_button.pack(pady=10)
        
        self.decrypt_python_button = tk.Button(root, text="Decrypt Python File", command=self.decrypt_python_file)
        self.decrypt_python_button.pack(pady=10)
    
    def generate_encryption_key(self):
        return os.urandom(32)  # 256-bit key

    def encrypt_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'rb') as file:
                file_data = file.read()

            aes_key = self.generate_encryption_key()
            cipher_aes = AES.new(aes_key, AES.MODE_EAX)
            ciphertext, tag = cipher_aes.encrypt_and_digest(file_data)

            cipher_rsa = PKCS1_OAEP.new(self.public_key)
            encrypted_key = cipher_rsa.encrypt(aes_key)

            encrypted_data = base64.b64encode(encrypted_key + cipher_aes.nonce + tag + ciphertext).decode('utf-8')
            encrypted_file_path = file_path + ".encrypted"
            with open(encrypted_file_path, 'w') as file:
                file.write(encrypted_data)

            password = base64.b64encode(aes_key).decode('utf-8')
            
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Success", f"File encrypted successfully. One-time password for decryption (copied to clipboard):\n\n{password}")
    
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

    def decrypt_file(self):
        file_path = filedialog.askopenfilename()
        if file_path and file_path.endswith('.encrypted'):
            password = simpledialog.askstring("Password", "Enter the one-time password provided during encryption:")
            if not password:
                messagebox.showerror("Error", "Password is required")
                return

            with open(file_path, 'r') as file:
                encrypted_data = base64.b64decode(file.read())

            encrypted_key = encrypted_data[:self.private_key.size_in_bytes()]
            nonce = encrypted_data[self.private_key.size_in_bytes():self.private_key.size_in_bytes()+16]
            tag = encrypted_data[self.private_key.size_in_bytes()+16:self.private_key.size_in_bytes()+32]
            ciphertext = encrypted_data[self.private_key.size_in_bytes()+32:]

            try:
                aes_key = base64.b64decode(password.encode('utf-8'))
                cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
                decrypted_data = cipher_aes.decrypt_and_verify(ciphertext, tag)
                with open(file_path.replace(".encrypted", ""), 'wb') as file:
                    file.write(decrypted_data)
                os.remove(file_path)
                messagebox.showinfo("Success", "File decrypted successfully and encrypted file deleted")
            except (ValueError, KeyError):
                messagebox.showerror("Error", "Failed to decrypt file. Invalid password or corrupted file.")
        else:
            messagebox.showerror("Error", "Failed to decrypt file or invalid file type")
    
    def decrypt_python_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Encrypted Files", "*_encrypted.py")])
        if not file_path:
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            encrypted_content = file.read()
        
        key_encoded = simpledialog.askstring("Password", "Enter the decryption key:")
        if not key_encoded:
            messagebox.showerror("Error", "Decryption key is required")
            return
        
        try:
            key = base64.b64decode(key_encoded)
            
            start_nonce = encrypted_content.find("base64.b64decode(") + len("base64.b64decode(") + 1
            end_nonce = encrypted_content.find("\")", start_nonce)
            nonce_encoded = encrypted_content[start_nonce:end_nonce]
            nonce = base64.b64decode(nonce_encoded)
            
            start_tag = encrypted_content.find("base64.b64decode(", end_nonce) + len("base64.b64decode(") + 1
            end_tag = encrypted_content.find("\")", start_tag)
            tag_encoded = encrypted_content[start_tag:end_tag]
            tag = base64.b64decode(tag_encoded)
            
            start_data = encrypted_content.find("base64.b64decode(", end_tag) + len("base64.b64decode(") + 1
            end_data = encrypted_content.find("\")", start_data)
            encrypted_data_encoded = encrypted_content[start_data:end_data]
            encrypted_data = base64.b64decode(encrypted_data_encoded)
            
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            decrypted_content = cipher.decrypt_and_verify(encrypted_data, tag).decode('utf-8')
            
            decrypted_file_path = file_path.replace("_encrypted.py", "_decrypted.py")
            with open(decrypted_file_path, 'w', encoding='utf-8') as file:
                file.write(decrypted_content)
            
            messagebox.showinfo("Success", 
                f"Python file decrypted successfully!\n\n"
                f"Decrypted file: {decrypted_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decrypt Python file. Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileEncryptorApp(root)
    root.mainloop()