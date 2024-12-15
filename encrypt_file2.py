import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
import base64
import os
import py_compile
import marshal

class FileEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Encryptor/Decryptor")
        
        # INI WM
        # Generate RSA keys
        self.private_key = RSA.generate(2048)
        self.public_key = self.private_key.publickey()

        self.encrypt_button = tk.Button(root, text="Encrypt File", command=self.encrypt_file)
        self.encrypt_button.pack(pady=10)

        self.encrypt_executable_button = tk.Button(root, text="Encrypt Executable File", command=self.encrypt_executable_file)
        self.encrypt_executable_button.pack(pady=10)
        
        self.decrypt_button = tk.Button(root, text="Decrypt File", command=self.decrypt_file)
        self.decrypt_button.pack(pady=10)

    def encrypt_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'rb') as file:
                file_data = file.read()

            aes_key = os.urandom(32)
            cipher_aes = AES.new(aes_key, AES.MODE_EAX)
            ciphertext, tag = cipher_aes.encrypt_and_digest(file_data)

            cipher_rsa = PKCS1_OAEP.new(self.public_key)
            encrypted_key = cipher_rsa.encrypt(aes_key)

            encrypted_data = base64.b64encode(encrypted_key + cipher_aes.nonce + tag + ciphertext).decode('utf-8')
            encrypted_file_path = file_path + ".encrypted"
            with open(encrypted_file_path, 'w') as file:
                file.write(encrypted_data)

            # Generate a one-time use password for decryption
            password = base64.b64encode(aes_key).decode('utf-8')
            
            # Copy password to clipboard
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Success", f"File encrypted successfully. One-time password for decryption (copied to clipboard):\n\n{password}")

    def encrypt_executable_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            # Compile to bytecode
            compiled_path = file_path + "c"
            py_compile.compile(file_path, cfile=compiled_path)
            
            # Read bytecode
            with open(compiled_path, 'rb') as file:
                bytecode = file.read()
            
            aes_key = os.urandom(32)
            cipher_aes = AES.new(aes_key, AES.MODE_EAX)
            ciphertext, tag = cipher_aes.encrypt_and_digest(bytecode)

            cipher_rsa = PKCS1_OAEP.new(self.public_key)
            encrypted_key = cipher_rsa.encrypt(aes_key)

            encrypted_data = base64.b64encode(encrypted_key + cipher_aes.nonce + tag + ciphertext).decode('utf-8')
            encrypted_file_path = file_path + ".encrypted_exec"
            with open(encrypted_file_path, 'w') as file:
                file.write(encrypted_data)

            os.remove(compiled_path)  # remove temporary compiled bytecode file

            # Generate a one-time use password for decryption
            password = base64.b64encode(aes_key).decode('utf-8')
            
            # Copy password to clipboard
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Success", f"File encrypted successfully as executable. One-time password for decryption (copied to clipboard):\n\n{password}")

    def decrypt_file(self):
        file_path = filedialog.askopenfilename()
        if file_path and (file_path.endswith('.encrypted') or file_path.endswith('.encrypted_exec')):
            # Ask user for one-time password
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

            aes_key = base64.b64decode(password.encode('utf-8'))
            cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
            try:
                decrypted_data = cipher_aes.decrypt_and_verify(ciphertext, tag)

                if file_path.endswith('.encrypted'):
                    output_file = file_path.replace(".encrypted", "")
                    with open(output_file, 'wb') as file:
                        file.write(decrypted_data)
                elif file_path.endswith('.encrypted_exec'):
                    # Execute the decrypted bytecode
                    exec(marshal.loads(decrypted_data))
                
                # Delete the encrypted file after successful decryption
                os.remove(file_path)
                messagebox.showinfo("Success", "File decrypted successfully and encrypted file deleted")
            except (ValueError, KeyError):
                messagebox.showerror("Error", "Failed to decrypt file. Invalid password or corrupted file.")
        else:
            messagebox.showerror("Error", "Failed to decrypt file or invalid file type")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileEncryptorApp(root)
    root.mainloop()