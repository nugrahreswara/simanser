# SIMANSER - Sistem Informasi Manajemen Administrasi dan Monitoring Server
## 1. Deskripsi Singkat
SIMANSER adalah program simulasi peran **Systems Administrator** untuk mengelola sekumpulan server (Web, Database, File). Fitur utama mencakup CRUD data server, monitoring resource, pencatatan insiden, log aktivitas, dan pengelolaan akun admin. Program ditulis dengan pendekatan OOP murni menggunakan Python.

## 2. Struktur Class

| Class | Jenis | Peran |
|---|---|---|
| `Monitorable` | Interface (ABC) | Kontrak method `monitor()` |
| `Manageable` | Interface (ABC) | Kontrak method `start_service()` |
| `Server` | Abstract Class | Blueprint server (hostname, IP, CPU, RAM, status, lokasi, uptime) |
| `WebServer` | Subclass | Menambah `port` + `total_request` |
| `DatabaseServer` | Subclass | Menambah `nama_database` + `ukuran_gb` |
| `FileServer` | Subclass | Menambah `kapasitas_gb` + `terpakai_gb` |
| `CatatanInsiden` | Class mandiri | Bagian dari Server (komposisi) |
| `Admin` | Class mandiri | Akun admin + method restart server |
| `LogAktivitas` | Class mandiri | Mencatat aksi admin |
| `ServerManager` | Class mandiri | CRUD server + monitoring |

## 3. Penerapan 4 Pilar OOP
- **Abstraction**: `Server` dibuat abstract, ditambah interface `Monitorable` & `Manageable`.
- **Encapsulation**: Atribut private (`__status`, `__password`, `__daftar_server`, `__catatan_insiden`) diakses via `@property` / `@<nama>.setter` dengan validasi.
- **Inheritance**: `WebServer`, `DatabaseServer`, `FileServer` mewarisi `Server` melalui `super().__init__()`.
- **Polymorphism**: `ServerManager` memanggil `monitor()` pada `List<Server>` tanpa peduli tipe konkretnya (dynamic dispatch).

## 4. Relasi UML yang Diterapkan

### a. Asosiasi (`menggunakan`)
`Admin` menggunakan `Server` sebagai parameter method `restart_server(server)`. Server tidak disimpan permanen sebagai atribut Admin, jadi kedua objek berdiri independen.

```python
def restart_server(self, server):
    server.stop()
    server.start()
```

### b. Agregasi (memiliki)
ServerManager menyimpan __daftar_server yang menampung objek Server yang dibuat di luar. Jika ServerManager dihapus, objek Server tetap ada di memori.

```python
def tambah_server(self, server):
    self.__daftar_server.append(server)
```

### c. Komposisi (terdiri dari)
Server memiliki __catatan_insiden yang berisi objek CatatanInsiden yang dibuat di dalam method catat_insiden(). Jika Server dimusnahkan, seluruh riwayat insidennya ikut hilang.

``` python
def catat_insiden(self, kode, deskripsi, tingkat="INFO"):
    insiden = CatatanInsiden(kode, deskripsi, tingkat)
    self.__catatan_insiden.append(insiden)
```

## 5. Penerapan Inheritance (Modul 5)
- Superclass: Server.Subclass: WebServer, DatabaseServer, FileServer.

- super().__init__(...) dipanggil di setiap konstruktor subclass.

- Atribut unik subclass:

  - WebServer → port, __total_request

  - DatabaseServer → nama_database, __ukuran_gb

  - FileServer → kapasitas_gb, __terpakai_gb

  - Method Overriding: monitor() dan start_service() di-override di setiap subclass dengan logika berbeda.

- Hak Akses:

  - Protected _lokasi, _uptime_jam → dipakai bersama dengan subclass.

  - Private __status, __catatan_insiden, __hostname → eksklusif milik Server.

## 6. Penerapan Polimorfisme & Abstraksi (Modul 6)
- ABC (Monitorable, Manageable) memaksa subclass mengimplementasikan monitor() dan start_service().

- Dynamic dispatch: manager.monitor_semua_server() memanggil monitor() pada List<Server> — hasilnya otomatis berbeda untuk WebServer, DatabaseServer, dan FileServer.

- Duck typing: ServerManager.monitor_semua_server() cukup memanggil s.monitor() tanpa peduli tipe konkretnya.

- isinstance() dipakai di __main__ untuk memverifikasi hierarki kelas.

## 7. Penerapan Materi Modul 1-3 (dari tugas sebelumnya)
- Modul 1 (Class & Object): Semua entitas dibuat sebagai class dan diinstansiasi di main.

- Modul 2 (Atribut & Method): Atribut kelas (total_server, nama_instansi, max_cpu_threshold, versi_sistem, min_password_length), atribut instance via __init__, instance method, @classmethod (get_total_server(), ubah_versi(), dari_dict()), dan @staticmethod (validasi_hostname(), validasi_port(), validasi_username()).

- Modul 3 (Encapsulation): Semua atribut sensitif memakai __nama, diakses via @property / @<nama>.setter dengan validasi raise ValueError.

## 8. Panduan Pengujian
### Jalankan program:

``` bash
python simanser.py
```

## Program akan menjalankan 16 skenario pengujian:

- Pembuatan 2 objek Admin (manual & via @classmethod dari_dict).

- Pembuatan 6 objek Server (Web, DB, File).

- Registrasi server ke dua ServerManager (agregasi).

- Monitoring semua server (membuktikan polymorphism).

- Menjalankan service tiap jenis server.

- Update server via CRUD.

- Cari server via CRUD.

- Hapus server via CRUD.

- Asosiasi: Admin.restart_server(server).

- Komposisi: Server mencatat CatatanInsiden sendiri.

- Uji validasi setter (data invalid → ValueError, data valid → diterima).

- Uji @classmethod.

- Uji @staticmethod.

- Menampilkan log aktivitas.

- Uji login admin.

- Uji isinstance() & issubclass().

## 9. Repositori Github
```text
https://github.com/nugrahreswara/simanser
```

## 10. Ringkasan Perubahan dari Versi Sebelumnya
| Aspek | Sebelum | Sesudah |
|---|---|---|
| **Relasi UML** | Hanya implisit | Eksplisit: Asosiasi, Agregasi, Komposisi |
| **Class baru** | — | `CatatanInsiden` (sebagai komposisi Server) |
| **Protected attribute** | Tidak ada | `_lokasi`, `_uptime_jam` pada `Server` |
| **Private attribute** | Sudah ada | Ditambah `__catatan_insiden` |
| **Overriding** | `monitor()` & `start_service()` | Sama, tapi kini memicu `catat_insiden()` otomatis |
| **Asosiasi** | Belum jelas | `Admin.restart_server(server)` — parameter, bukan atribut |
| **Agregasi** | Sudah ada (`__daftar_server`) | Ditandai eksplisit di komentar & README |
| **Komposisi** | Belum ada | `Server` membuat `CatatanInsiden` di dalam dirinya |
| **Pengujian** | 13 skenario | 16 skenario (+asosiasi, komposisi, isinstance) |