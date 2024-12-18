# Tugas-API
Ini adalah dokumentasi API untuk mengelola tugas dan otentifikasi pengguna menggunakan python Flask

## Daftar Isi
- [Instalasi](#instalasi)
- [Menjalankan API](#menjalankan-api)
- [Cara Penggunaan di Postman](#cara-penggunaan-di-postman)


## Instalasi

1. **Clone repositori ini/Copy file app.py**:
    ```bash
    git clone https://github.com/AryaNurRazzaq/Tugas-API.git
    ```

2. **Arahkan ke direktori proyek**:
    ```bash
    cd tugas-api
    ```

3. **Install dependensi Python yang dibutuhkan dengan menggunakan `pip` atau `pipenv`:**
    ```bash
    pip install flask flask_sqlalchemy flask_jwt_extended flask_bcrypt
    ```

## Menjalankan API

1. Pastikan Python 3.x sudah terinstal.

2. Jalankan aplikasi Flask:
    ```bash
    python app.py
    ```
3. API akan tersedia di `http://127.0.0.1:5000/`.

## Cara Penggunaan di Postman
Coba API ini menggunakan aplikasi Postman

### 1. **Mendaftar Pengguna Baru**

- Buka Postman dan pilih metode **POST**.
- Pada Headers tambahkan key "Content-type" dengan value "application/json"
- Masukkan URL `http://127.0.0.1:5000/daftar`.
- Di tab **Body**, pilih **raw** dan pilih **JSON**.
- Masukkan data pengguna yang ingin didaftarkan:
    ```json
    {
      "username": "penggunaBaru",
      "password": "password123"
    }
    ```
- Klik **Send** untuk mengirim permintaan.
- Response:
   - berhasil:
    ```json
    {
      "pesan": "Pengguna berhasil ditambahkan"
    }
    ```
    - jika terdapat username yang sudah terdaftar:
    ```json
    {
      "pesan": "Username sudah terdaftar"
    }
    ```

    ### 2. **Login Pengguna**

- Pilih metode **POST** dan masukkan URL `http://127.0.0.1:5000/masuk`.
- Di tab **Body**, pilih **raw** dan pilih **JSON**.
- Masukkan kredensial pengguna:
    ```json
    {
      "username": "penggunaBaru",
      "password": "password123"
    }
    ```
- Klik **Send** untuk mengirim permintaan.
- Response:
    - berhasil:
    ```json
    {
      "token": "jwt.token"
    }
    ```
    - jika username atau password salah:
    ```json
    {
      "pesan": "Username atau password salah"
    }
    ```

    ### 3. **Menambahkan Tugas**
- Pada headers tambahkan key "Authorization" dengan Value Bearer <token>
- Pilih metode **POST** dan masukkan URL `http://127.0.0.1:5000/tugas`.
- Di tab **Body**, pilih **raw** dan pilih **JSON**.
- 
- Masukkan data tugas yang ingin ditambahkan:
    ```json
    {
      "judul": "Tugas Baru",
      "deskripsi": "Deskripsi tugas baru"
    }
    ```
- Di tab **Authorization**, pilih **Bearer Token** dan masukkan token JWT.
- Klik **Send** untuk mengirim permintaan.
- Response:
    ```json
    {
      "pesan": "Tugas berhasil ditambahkan",
      "id": 1
    }
    ```

    ### 4. **Mengambil Daftar Tugas**

- Pilih metode **GET** dan masukkan URL `http://127.0.0.1:5000/tugas`.
- Di tab **Authorization**, pilih **Bearer Token** dan masukkan token JWT yang Anda terima dari login.
- Klik **Send** untuk mengirim permintaan.
- Response:
    ```json
    [
      {
        "id": 1,
        "judul": "Tugas 1",
        "deskripsi": "Deskripsi tugas 1",
        "selesai": false,
        "tanggal": "tanggal pembuatan"
      }
    ]
    ```

### 5. **Memperbarui Tugas (PUT /tugas/{id})**

- Pilih metode **PUT** dan masukkan URL `http://127.0.0.1:5000/tugas/{id}` (Ganti `{id}` dengan ID tugas yang ingin diperbarui).
- Di tab **Body**, pilih **raw** dan pilih **JSON**.
- Masukkan data tugas yang ingin diperbarui:
    ```json
    {
      "judul": "Tugas yang Diperbarui",
      "deskripsi": "Deskripsi tugas yang diperbarui",
      "selesai": true
    }
    ```
- Di tab **Authorization**, pilih **Bearer Token** dan masukkan token JWT.
- Klik **Send** untuk mengirim permintaan.
- Response:
   - berhasil: 
    ```json
    {
      "pesan": "Tugas berhasil diperbarui"
    }
    ```
    - Jika tugas tidak ditemukan: 
    ```json
    {
      "pesan": "Tugas tidak ditemukan"
    }
    ```

### 6. **Menghapus Tugas (DELETE /tugas/{id})**

- Pilih metode **DELETE** dan masukkan URL `http://127.0.0.1:5000/tugas/{id}` (Gantilah `{id}` dengan ID tugas yang ingin dihapus).
- Di tab **Authorization**, pilih **Bearer Token** dan masukkan token JWT.
- Klik **Send** untuk mengirim permintaan.
- Response:
   - berhasil: 
    ```json
    {
      "pesan": "Tugas berhasil dihapus"
    }
    ```
    - Jika tugas tidak ditemukan: 
    ```json
    {
      "pesan": "Tugas tidak ditemukan"
    }
    ```
