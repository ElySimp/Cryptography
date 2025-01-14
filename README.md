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

Cara Kerja Pemilihan e Sekarang:

Program sekarang akan mencoba nilai e mulai dari 2. Untuk setiap nilai e, program akan menghitung FPB(e, φ(n)). Jika FPB-nya 1, maka nilai e tersebut valid dan loop berhenti. Jika tidak, e dinaikkan dan proses diulang.

Apa itu Tanda Tangan Digital?

Tanda tangan digital adalah nilai numerik yang dihasilkan menggunakan algoritma kriptografi, dan memiliki beberapa tujuan utama:

Autentikasi: Memastikan identitas pengirim pesan.

Integritas: Memastikan bahwa pesan tidak diubah sejak ditandatangani.

Non-repudiation: Mencegah pengirim menyangkal bahwa mereka telah mengirim pesan.

Esensi utama dari algoritma RSA adalah bahwa dekripsi dilakukan menggunakan kunci privat (𝑑 , 𝑛) saja. Kunci publik (𝑒 , 𝑛) digunakan untuk enkripsi, dan kunci privat (𝑑 , 𝑛) digunakan untuk dekripsi.

Namun, kunci publik (𝑒,𝑛) juga dapat digunakan untuk tujuan lain, seperti verifikasi tanda tangan digital. Mari kita jelaskan lebih lanjut:

Proses Enkripsi dan Dekripsi RSA
Enkripsi:

Menggunakan kunci publik (𝑒,𝑛):

𝐶 = 𝑀^e mod 𝑛

Di mana 𝑀 adalah plaintext (dalam bentuk numerik) dan 𝐶 adalah ciphertext yang dihasilkan.

Dekripsi:

Menggunakan kunci privat (𝑑 , 𝑛):

𝑀 = 𝐶^d mod 𝑛
Di mana 𝐶 adalah ciphertext dan 𝑀 adalah plaintext yang didekripsi.

Tanda Tangan Digital dengan RSA
RSA juga digunakan untuk tanda tangan digital, di mana kunci publik digunakan untuk verifikasi. Langkah-langkahnya adalah sebagai berikut:

Membuat Tanda Tangan Digital:

Pengirim menggunakan kunci privat (𝑑,𝑛) untuk membuat tanda tangan digital dari pesan atau hash pesan:

𝑆 =𝐻(𝑀)𝑑 mod 𝑛

Di mana 𝐻(𝑀) adalah hash dari pesan 𝑀 , dan 𝑆 adalah tanda tangan digital.

Verifikasi Tanda Tangan Digital:

Penerima menggunakan kunci publik (𝑒,𝑛) untuk memverifikasi tanda tangan digital:

𝐻(𝑀)= 𝑆^e mod 𝑛
Jika hasilnya sama dengan hash asli dari pesan, maka tanda tangan digital valid, menunjukkan bahwa pesan belum diubah dan memang berasal dari pengirim yang sah.

Inti RSA
Dekripsi: Menggunakan kunci privat (𝑑,𝑛) untuk mendapatkan kembali plaintext dari ciphertext.

Enkripsi: Menggunakan kunci publik (𝑒,𝑛) untuk mengenkripsi plaintext menjadi ciphertext.

Verifikasi Tanda Tangan: Menggunakan kunci publik (𝑒,𝑛)untuk memverifikasi tanda tangan digital.


Cara Menjalankan:

    Pastikan Anda telah menginstal Flet: pip install flet