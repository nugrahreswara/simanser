from abc import ABC, abstractmethod
from datetime import datetime

# === Abstraction: Interface (ISP) ===
class Monitorable(ABC):
    @abstractmethod
    def monitor(self):
        pass

class Manageable(ABC):
    @abstractmethod
    def start_service(self):
        pass

class Notifier(ABC):
    @abstractmethod
    def kirim_alert(self, pesan):
        pass

# === Komposisi ===
class CatatanInsiden:
    def __init__(self, kode, deskripsi, tingkat):
        self.kode = kode
        self.deskripsi = deskripsi
        self.tingkat = tingkat
        self.__waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def waktu(self):
        return self.__waktu

    def __str__(self):
        return f"[{self.__waktu}] {self.kode} ({self.tingkat}): {self.deskripsi}"

# === Abstract Class Server ===
class Server(Monitorable, Manageable):
    total_server = 0
    default_status = "OFFLINE"
    max_cpu_threshold = 80

    def __init__(self, hostname, ip_address, cpu_usage=0, ram_usage=0):
        self.hostname = hostname
        self.ip_address = ip_address
        self.cpu_usage = cpu_usage
        self.ram_usage = ram_usage
        self._lokasi = "Data Center Utama"
        self._uptime_jam = 0
        self.__status = Server.default_status
        self.__catatan_insiden = []
        Server.total_server += 1

    @property
    def hostname(self):
        return self.__hostname

    @hostname.setter
    def hostname(self, value):
        if not value or not value.strip():
            raise ValueError("Hostname tidak boleh kosong")
        self.__hostname = value

    @property
    def ip_address(self):
        return self.__ip_address

    @ip_address.setter
    def ip_address(self, value):
        if not value or value.count(".") != 3:
            raise ValueError("Format IP tidak valid")
        self.__ip_address = value

    @property
    def cpu_usage(self):
        return self.__cpu_usage

    @cpu_usage.setter
    def cpu_usage(self, value):
        if value < 0 or value > 100:
            raise ValueError("CPU usage harus 0-100")
        self.__cpu_usage = value

    @property
    def ram_usage(self):
        return self.__ram_usage

    @ram_usage.setter
    def ram_usage(self, value):
        if value < 0 or value > 100:
            raise ValueError("RAM usage harus 0-100")
        self.__ram_usage = value

    @property
    def status(self):
        return self.__status

    @property
    def daftar_insiden(self):
        return list(self.__catatan_insiden)

    def start(self):
        self.__status = "ONLINE"

    def stop(self):
        self.__status = "OFFLINE"

    def catat_insiden(self, kode, deskripsi, tingkat="INFO"):
        insiden = CatatanInsiden(kode, deskripsi, tingkat)
        self.__catatan_insiden.append(insiden)
        return insiden

    def jalankan(self):
        self.start()
        self._uptime_jam += 1
        return f"[{self.hostname}] {self.start_service()} | Status: {self.monitor()}"

    def __str__(self):
        return f"[{self.__status}] {self.hostname} ({self.ip_address}) CPU:{self.__cpu_usage}%"

    @abstractmethod
    def monitor(self):
        pass

    @abstractmethod
    def start_service(self):
        pass

    @classmethod
    def get_total_server(cls):
        return cls.total_server

    @classmethod
    def ubah_threshold_cpu(cls, nilai_baru):
        if 0 <= nilai_baru <= 100:
            cls.max_cpu_threshold = nilai_baru

    @staticmethod
    def validasi_hostname(hostname):
        return bool(hostname) and " " not in hostname and len(hostname) >= 3

# === Inheritance & Polimorfisme via Pewarisan ===
class WebServer(Server):
    def __init__(self, hostname, ip_address, port=80, cpu_usage=0, ram_usage=0):
        super().__init__(hostname, ip_address, cpu_usage, ram_usage)
        self.port = port
        self.__total_request = 0

    def monitor(self):
        if self.cpu_usage > Server.max_cpu_threshold:
            self.catat_insiden("WEB-CPU", f"CPU tinggi {self.cpu_usage}%", "WARNING")
            return f"WebServer {self.hostname} CPU tinggi"
        return f"WebServer {self.hostname} normal"

    def start_service(self):
        return f"Web service aktif di port {self.port}"

class DatabaseServer(Server):
    def __init__(self, hostname, ip_address, nama_database, cpu_usage=0, ram_usage=0):
        super().__init__(hostname, ip_address, cpu_usage, ram_usage)
        self.nama_database = nama_database
        self.__ukuran_gb = 0

    def monitor(self):
        if self.ram_usage > Server.max_cpu_threshold:
            self.catat_insiden("DB-RAM", f"RAM tinggi {self.ram_usage}%", "WARNING")
            return f"DatabaseServer {self.hostname} RAM tinggi"
        return f"DatabaseServer {self.hostname} normal"

    def start_service(self):
        return f"Database service {self.nama_database} aktif"

class FileServer(Server):
    def __init__(self, hostname, ip_address, kapasitas_gb=100, cpu_usage=0, ram_usage=0):
        super().__init__(hostname, ip_address, cpu_usage, ram_usage)
        self.kapasitas_gb = kapasitas_gb
        self.__terpakai_gb = 0

    def monitor(self):
        persen = (self.__terpakai_gb / self.kapasitas_gb) * 100
        if persen > 90:
            self.catat_insiden("FS-PENUH", f"Disk {persen:.1f}% terpakai", "CRITICAL")
            return f"FileServer {self.hostname} hampir penuh"
        return f"FileServer {self.hostname} normal"

    def start_service(self):
        return f"File service aktif"

# === Duck Typing (Kelas tidak berhubungan) ===
class EmailNotifier:
    def kirim_alert(self, pesan):
        return f"[EMAIL] {pesan}"

class SMSNotifier:
    def kirim_alert(self, pesan):
        return f"[SMS] {pesan}"

# === Admin (Asosiasi) ===
class Admin:
    nama_instansi = "SIMANSER"
    min_password_length = 8

    def __init__(self, username, password, role="admin"):
        self.username = username
        self.password = password
        self.role = role
        self.__login_attempt = 0

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        if len(value) < 3:
            raise ValueError("Username minimal 3 karakter")
        self.__username = value

    @property
    def password(self):
        return "*" * len(self.__password)

    @password.setter
    def password(self, value):
        if len(value) < Admin.min_password_length:
            raise ValueError("Password terlalu pendek")
        self.__password = value

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, value):
        if value not in ("admin", "superadmin", "operator"):
            raise ValueError("Role tidak valid")
        self.__role = value

    def login(self, password):
        if password == self.__password:
            self.__login_attempt = 0
            return True
        self.__login_attempt += 1
        return False

    def info(self):
        return f"Admin: {self.__username} | Role: {self.__role}"

    # Asosiasi: Admin menggunakan Server sebagai parameter, tidak disimpan permanen
    def restart_server(self, server):
        server.stop()
        server.start()
        return f"Server {server.hostname} di-restart oleh {self.__username}"

    @classmethod
    def dari_dict(cls, data):
        return cls(data["username"], data["password"], data.get("role", "admin"))

    @staticmethod
    def validasi_username(username):
        return bool(username) and username.isalnum() and len(username) >= 3

# === Log Aktivitas ===
class LogAktivitas:
    total_log = 0
    riwayat = []

    def __init__(self, username, aksi):
        self.username = username
        self.aksi = aksi
        self.__waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        LogAktivitas.total_log += 1
        LogAktivitas.riwayat.append(self)

    def info(self):
        return f"[{self.__waktu}] {self.username} -> {self.aksi}"

    @classmethod
    def tampilkan_semua(cls):
        for log in cls.riwayat:
            print(log.info())

# === Server Manager (Agregasi & DIP) ===
class ServerManager:
    versi_sistem = "1.0.0"

    # DIP: Notifier (abstraksi) disuntikkan dari luar
    def __init__(self, admin, notifier: Notifier):
        self.admin = admin
        self.notifier = notifier
        self.__daftar_server = []

    @property
    def daftar_server(self):
        return list(self.__daftar_server)

    def tambah_server(self, server):
        if not Server.validasi_hostname(server.hostname):
            raise ValueError("Hostname tidak valid")
        if self.cari_server(server.hostname):
            raise ValueError("Server sudah terdaftar")
        self.__daftar_server.append(server)
        LogAktivitas(self.admin.username, f"Tambah server {server.hostname}")

    def get_all_server(self):
        return list(self.__daftar_server)

    def cari_server(self, hostname):
        for s in self.__daftar_server:
            if s.hostname == hostname:
                return s
        return None

    def update_server(self, hostname, ip_baru, cpu, ram):
        server = self.cari_server(hostname)
        if not server:
            raise ValueError("Server tidak ditemukan")
        server.ip_address = ip_baru
        server.cpu_usage = cpu
        server.ram_usage = ram
        LogAktivitas(self.admin.username, f"Update server {hostname}")

    def hapus_server(self, hostname):
        server = self.cari_server(hostname)
        if not server:
            raise ValueError("Server tidak ditemukan")
        self.__daftar_server.remove(server)
        LogAktivitas(self.admin.username, f"Hapus server {hostname}")

    def monitor_semua_server(self):
        # Anti-pattern dihindari: tidak ada if isinstance()
        for s in self.__daftar_server:
            status = s.monitor()
            print(status)
            if "tinggi" in status or "penuh" in status:
                # DIP: Memanggil abstraksi notifier
                print(self.notifier.kirim_alert(f"Peringatan di {s.hostname}"))

    # Operator Overloading
    def __len__(self):
        return len(self.__daftar_server)

# === MAIN ===
if __name__ == "__main__":
    print("=" * 60)
    print(f"{Admin.nama_instansi} - Sistem Informasi Manajemen Server")
    print("=" * 60)

    # 1. Bukti Abstraksi (Abstract Class tidak bisa diinstansiasi)
    print("\n[1] Bukti Abstraksi")
    try:
        server_abstrak = Server("dummy", "1.1.1.1")
    except TypeError as e:
        print(f"Error (Terbukti abstrak): {e}")

    # 2. Instansiasi Class
    admin1 = Admin("sysadmin", "P@ssw0rd_025", "superadmin")
    web1 = WebServer("web-01", "192.168.1.10", port=80)
    db1 = DatabaseServer("db-01", "192.168.1.20", "produksi", ram_usage=85)
    fs1 = FileServer("fs-01", "192.168.1.30", kapasitas_gb=100)

    # DIP: Mengirimkan EmailNotifier ke dalam ServerManager
    manager = ServerManager(admin1, EmailNotifier())
    manager.tambah_server(web1)
    manager.tambah_server(db1)
    manager.tambah_server(fs1)

    # 3. Polimorfisme via Pewarisan (Looping)
    print("\n[2] Polimorfisme via Pewarisan")
    manager.monitor_semua_server()

    # 4. Duck Typing
    print("\n[3] Duck Typing")
    def proses_notifikasi(notifier, pesan):
        print(notifier.kirim_alert(pesan))
    
    sms = SMSNotifier()
    proses_notifikasi(manager.notifier, "Sistem Normal")
    proses_notifikasi(sms, "Sistem Normal") # Fungsi sama, objek beda

    # 5. Operator Overloading
    print("\n[4] Operator Overloading")
    print(f"Jumlah server di Manager: {len(manager)}")
    print(str(db1))

    # 6. Asosiasi
    print("\n[5] Asosiasi")
    print(admin1.restart_server(web1))

    # 7. Komposisi
    print("\n[6] Komposisi (Insiden otomatis dibuat oleh Server)")
    print(f"Insiden DB: {[str(i) for i in db1.daftar_insiden]}")
