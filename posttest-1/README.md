# SIMANSER - Sistem Informasi Manajemen Administrasi dan Monitoring Server
#### Project Praktikum Pemrograman Berbasis Objek (PBO)  
#### Program Studi Informatika - Semester 3

## 1. Deskripsi Singkat
SIMANSER adalah program simulasi peran **Systems Administrator** untuk mengelola sekumpulan server (Web, Database, File). Fitur utama mencakup CRUD data server, monitoring resource, pencatatan log aktivitas, dan pengelolaan akun admin. Program ditulis dengan pendekatan Object-Oriented Programming (OOP) murni menggunakan bahasa pemrograman Python.

## 2. Struktur Class

| Class | Jenis | Peran |
|---|---|---|
| `Monitorable` | Interface (ABC) | Kontrak method `monitor()` |
| `Manageable` | Interface (ABC) | Kontrak method `start_service()` |
| `Server` | Abstract Class | Blueprint server, menyimpan hostname, IP, CPU, RAM, status |
| `WebServer` | Subclass | Server web dengan port & total request |
| `DatabaseServer` | Subclass | Server DB dengan nama database & ukuran |
| `FileServer` | Subclass | Server file dengan kapasitas & pemakaian |
| `Admin` | Class mandiri | Akun admin (username, password, role) |
| `LogAktivitas` | Class mandiri | Mencatat setiap aksi admin |
| `ServerManager` | Class mandiri | Mengelola list Server (CRUD + monitoring) |

## 3. Penerapan 4 Pilar OOP
- **Abstraction**: `Server` dibuat abstract, ditambah interface `Monitorable` & `Manageable`.
- **Encapsulation**: Atribut private pada `Server`, `Admin`, `LogAktivitas`, `ServerManager` diakses via `@property` dan `@<nama>.setter`.
- **Inheritance**: `WebServer`, `DatabaseServer`, `FileServer` mewarisi `Server`.
- **Polymorphism**: `ServerManager` memanggil `monitor()` pada `List<Server>` tanpa tahu jenis spesifik servernya.

## 4. Penerapan Materi Modul
- **Modul 1 (Class & Object):** Semua entitas dibuat sebagai class, diinstansiasi di main.  
- **Modul 2 (Atribut & Method):** Ada atribut kelas (`total_server`, `nama_instansi`, `max_cpu_threshold`, `versi_sistem`, dll), atribut instance via `__init__`, instance method, `@classmethod`, dan `@staticmethod`.
- **Modul 3 (Encapsulation):** Semua atribut sensitif memakai `__nama`, diakses via `@property` dan `@<nama>.setter` dengan validasi (raise `ValueError`).

## 5. Panduan Pengujian
Jalankan simanser.py:
```bash
python simanser.py
```

### Program akan menjalankan 13 skenario pengujian:
#### 1. Pembuatan 2 objek Admin (manual & via classmethod).
#### 2. Pembuatan 6 objek Server (Web, DB, File).
#### 3. Registrasi server ke dua ServerManager.
#### 4. Monitoring semua server (membuktikan polymorphism).
#### 5. Menjalankan service tiap jenis server.
#### 6. Update server via CRUD.
#### 7. Cari server via CRUD.
#### 8. Hapus server via CRUD.
#### 9. Uji validasi setter (data invalid → ValueError, data valid → diterima).
#### 10. Uji @classmethod.
#### 11. Uji @staticmethod.
#### 12. Menampilkan log aktivitas.
#### 13. Uji login admin.