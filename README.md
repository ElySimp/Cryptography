# Cryptography

Enkripsi RSA adalah sebuah algoritma kriptografi kunci publik yang banyak digunakan untuk pengamanan data. Nama RSA sendiri diambil dari inisial nama penemunya, yaitu Ron Rivest, Adi Shamir, dan Leonard Adleman, yang menemukannya pada tahun 1977 di MIT.

Berikut penjelasan lebih detail mengenai enkripsi RSA:

Konsep Dasar:

RSA bekerja dengan menggunakan dua kunci:

    Kunci Publik (Public Key): Kunci ini disebarluaskan dan digunakan untuk mengenkripsi pesan. Siapa pun dapat menggunakan kunci publik ini untuk mengenkripsi pesan yang akan dikirimkan kepada pemilik kunci.
    Kunci Privat (Private Key): Kunci ini bersifat rahasia dan hanya diketahui oleh pemiliknya. Kunci privat digunakan untuk mendekripsi pesan yang telah dienkripsi dengan kunci publik.

Analogi sederhananya seperti kotak surat dengan gembok. Kunci publik ibarat gembok yang terpasang di kotak surat, siapa pun bisa memasukkan surat (enkripsi) ke dalam kotak tersebut, tetapi hanya pemilik kunci privat (pemilik rumah) yang memiliki kunci untuk membuka gembok dan mengambil suratnya (dekripsi).

Proses Enkripsi dan Dekripsi:

    Pembangkitan Kunci: Proses ini melibatkan pemilihan dua bilangan prima besar (biasanya ratusan digit), yang kemudian digunakan untuk menghasilkan kunci publik dan kunci privat.
    Enkripsi: Pesan yang akan dienkripsi diubah menjadi angka, kemudian diproses menggunakan kunci publik untuk menghasilkan ciphertext (teks terenkripsi).
    Dekripsi: Ciphertext kemudian diproses menggunakan kunci privat untuk mengembalikan pesan asli.

Keamanan RSA:

Keamanan RSA terletak pada sulitnya memfaktorkan bilangan besar menjadi faktor-faktor prima. Jika seseorang dapat memfaktorkan bilangan yang digunakan dalam pembangkitan kunci, maka mereka dapat memperoleh kunci privat dan mendekripsi pesan. Oleh karena itu, semakin besar bilangan prima yang digunakan, semakin sulit pula untuk dipecahkan.

Penggunaan RSA:

RSA banyak digunakan dalam berbagai aplikasi pengamanan data, antara lain:

    Tanda Tangan Digital (Digital Signature): Memastikan keaslian dan integritas dokumen elektronik.
    Enkripsi Data: Melindungi kerahasiaan data yang disimpan atau ditransmisikan.
    Protokol SSL/TLS: Mengamankan komunikasi di internet, seperti pada transaksi e-commerce.

Kelebihan RSA:

    Tingkat keamanan yang tinggi jika menggunakan kunci yang cukup panjang.
    Dapat digunakan untuk enkripsi dan tanda tangan digital.

Kekurangan RSA:

    Proses enkripsi dan dekripsi relatif lambat dibandingkan dengan algoritma simetris.
    Membutuhkan kunci yang panjang untuk mencapai tingkat keamanan yang tinggi.

Kesimpulan:

Enkripsi RSA merupakan salah satu algoritma kriptografi kunci publik yang paling penting dan banyak digunakan saat ini. Keamanannya yang didasarkan pada kesulitan faktorisasi bilangan prima menjadikannya pilihan yang tepat untuk melindungi data sensitif. Meskipun memiliki beberapa kekurangan, RSA tetap menjadi landasan penting dalam pengamanan informasi digital.

Perubahan dan Penjelasan:

    1. Validasi Input Prima: Ditambahkan fungsi is_prime() untuk memastikan input p dan q adalah bilangan prima. Ini sangat penting untuk keamanan RSA. Juga ditambahkan pengecekan apakah p dan q sama.
    2. Loop untuk Mencari e: Menggunakan while True loop untuk terus mencari e sampai kondisi FPB(e, φ(n)) == 1 terpenuhi. e dimulai dari 2 dan dinaikkan satu per satu.
    3. Pengamanan Loop e: Ditambahkan if e >= phi: untuk mencegah infinite loop jika ternyata tidak ada nilai e yang memenuhi kondisi (walaupun sangat jarang terjadi untuk bilangan prima yang besar). Ini penting untuk mencegah program hang.
    4. Fungsi cari_invers_modular(): Implementasi fungsi untuk mencari invers modular d menggunakan Extended Euclidean Algorithm. Ini jauh lebih efisien daripada brute force untuk angka yang besar.
    5. Penanganan Error: Ditambahkan blok try-except untuk menangani jika user memasukkan input yang bukan angka atau bukan bilangan prima.
    6. Penggunaan Fungsi ord() dan chr(): Menggunakan fungsi ord() untuk mengubah karakter menjadi representasi numeriknya (ASCII) dan fungsi chr() untuk mengembalikan angka ASCII ke karakter. Ini penting untuk enkripsi teks.
    7. Pesan numerik, enkripsi, dan dekripsi dalam bentuk list: pesan, enkripsi, dan dekripsi sekarang disimpan dalam bentuk list, agar bisa memproses pesan yang lebih dari satu karakter.
    8. Contoh penggunaan dan print out yang lebih informatif.

Cara Kerja Pemilihan e Sekarang:

Program sekarang akan mencoba nilai e mulai dari 2. Untuk setiap nilai e, program akan menghitung FPB(e, φ(n)). Jika FPB-nya 1, maka nilai e tersebut valid dan loop berhenti. Jika tidak, e dinaikkan dan proses diulang.

Dengan perbaikan ini, program Anda sekarang seharusnya berfungsi dengan benar untuk enkripsi dan dekripsi teks menggunakan RSA. Pastikan Anda menguji dengan bilangan prima yang relatif kecil terlebih dahulu untuk memverifikasi kebenaran implementasi sebelum menggunakan bilangan prima yang lebih besar untuk keamanan yang sesungguhnya.

Perubahan dan Penjelasan untuk GUI dengan Flet:

    1. Import flet: Mengimpor library Flet.
    2. Fungsi main(page: ft.Page): Fungsi utama untuk membangun antarmuka Flet.
    3. Input Fields: Membuat TextField untuk input p, q, dan pesan.
    4. Text untuk Output: Membuat Text untuk menampilkan n, kunci publik, kunci privat, pesan terenkripsi, dan pesan dekripsi.
    5. Tombol Enkripsi: Membuat ElevatedButton untuk memicu proses enkripsi.
    6. Fungsi enkripsi_klik(e): Fungsi yang dipanggil saat tombol enkripsi diklik. Fungsi ini mengambil nilai dari input fields, memanggil fungsi enkripsi_rsa(), melakukan enkripsi dan dekripsi, dan menampilkan hasilnya di Text fields.
    7. Pemilihan e secara acak: Untuk menghindari selalu memilih e yang sama, sekarang e dipilih secara acak antara 2 dan phi-1. Ini masih memastikan bahwa e berada dalam rentang yang valid. Loop while masih ada untuk memastikan FPB(e, phi) = 1.
    8. Penanganan Error dan Feedback ke User: Pesan error dan hasil perhitungan ditampilkan pada UI agar user mendapat feedback.
    9. Penggunaan ft.Column dan ft.Row: Digunakan untuk mengatur layout elemen-elemen GUI.

Cara Menjalankan:

    Pastikan Anda telah menginstal Flet: pip install flet