from abc import ABC, abstractmethod
from datetime import datetime


# === Abstraction: Interface ===
class Monitorable(ABC):
    @abstractmethod
    def monitor(self):
        pass


class Manageable(ABC):
    @abstractmethod
    def start_service(self):
        pass


# === Komposisi: CatatanInsiden hanya hidup di dalam Server ===
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
    # Class attributes
    total_server = 0
    default_status = "OFFLINE"
    max_cpu_threshold = 80

    def __init__(self, hostname, ip_address, cpu_usage=0, ram_usage=0):
        self.hostname = hostname
        self.ip_address = ip_address
        self.cpu_usage = cpu_usage
        self.ram_usage = ram_usage
        self._lokasi = "Data Center Utama"      # Protected
        self._uptime_jam = 0                     # Protected
        self.__status = Server.default_status    # Private
        self.__catatan_insiden = []              # Private + Komposisi
        Server.total_server += 1

    # Getter & Setter
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
            raise ValueError("Format IP tidak valid (contoh: 192.168.1.1)")
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
    def lokasi(self):
        return self._lokasi

    @property
    def uptime_jam(self):
        return self._uptime_jam

    @property
    def daftar_insiden(self):
        return list(self.__catatan_insiden)

    # Instance method
    def start(self):
        self.__status = "ONLINE"

    def stop(self):
        self.__status = "OFFLINE"

    def catat_insiden(self, kode, deskripsi, tingkat="INFO"):
        # Komposisi: objek CatatanInsiden dibuat di dalam Server
        insiden = CatatanInsiden(kode, deskripsi, tingkat)
        self.__catatan_insiden.append(insiden)
        return insiden

    def tampilkan_info(self):
        return (f"[{self.__status}] {self.hostname} ({self.ip_address}) "
                f"CPU:{self.__cpu_usage}% RAM:{self.__ram_usage}% "
                f"Lokasi:{self._lokasi} Uptime:{self._uptime_jam}j")

    @abstractmethod
    def monitor(self):
        pass

    @abstractmethod
    def start_service(self):
        pass

    # Class method
    @classmethod
    def get_total_server(cls):
        return cls.total_server

    @classmethod
    def ubah_threshold_cpu(cls, nilai_baru):
        if nilai_baru < 0 or nilai_baru > 100:
            raise ValueError("Threshold harus 0-100")
        cls.max_cpu_threshold = nilai_baru

    # Static method
    @staticmethod
    def validasi_hostname(hostname):
        return bool(hostname) and " " not in hostname and len(hostname) >= 3


# === Inheritance + Polymorphism ===
class WebServer(Server):
    def __init__(self, hostname, ip_address, port=80, cpu_usage=0, ram_usage=0):
        super().__init__(hostname, ip_address, cpu_usage, ram_usage)
        self.port = port                    # Atribut unik WebServer
        self.__total_request = 0

    @property
    def total_request(self):
        return self.__total_request

    def tambah_request(self, jumlah=1):
        if jumlah < 0:
            raise ValueError("Jumlah request tidak boleh negatif")
        self.__total_request += jumlah

    def monitor(self):                      # Override
        if self.cpu_usage > Server.max_cpu_threshold:
            self.catat_insiden("WEB-CPU", f"CPU tinggi {self.cpu_usage}%", "WARNING")
            return f"[WARNING] WebServer {self.hostname} CPU tinggi: {self.cpu_usage}%"
        return f"[OK] WebServer {self.hostname} normal (request: {self.__total_request})"

    def start_service(self):                # Override
        self.start()
        self._uptime_jam += 1
        return f"Web service {self.hostname} aktif di port {self.port}"


class DatabaseServer(Server):
    def __init__(self, hostname, ip_address, nama_database, cpu_usage=0, ram_usage=0):
        super().__init__(hostname, ip_address, cpu_usage, ram_usage)
        self.nama_database = nama_database  # Atribut unik DatabaseServer
        self.__ukuran_gb = 0

    @property
    def ukuran_gb(self):
        return self.__ukuran_gb

    @ukuran_gb.setter
    def ukuran_gb(self, value):
        if value < 0:
            raise ValueError("Ukuran database tidak boleh negatif")
        self.__ukuran_gb = value

    def monitor(self):                      # Override
        if self.ram_usage > Server.max_cpu_threshold:
            self.catat_insiden("DB-RAM", f"RAM tinggi {self.ram_usage}%", "WARNING")
            return f"[WARNING] DatabaseServer {self.hostname} RAM tinggi: {self.ram_usage}%"
        return f"[OK] DatabaseServer {self.hostname} normal ({self.nama_database})"

    def start_service(self):                # Override
        self.start()
        self._uptime_jam += 1
        return f"Database service {self.nama_database} pada {self.hostname} aktif"


class FileServer(Server):
    def __init__(self, hostname, ip_address, kapasitas_gb=100, cpu_usage=0, ram_usage=0):
        super().__init__(hostname, ip_address, cpu_usage, ram_usage)
        self.kapasitas_gb = kapasitas_gb    # Atribut unik FileServer
        self.__terpakai_gb = 0

    @property
    def terpakai_gb(self):
        return self.__terpakai_gb

    @terpakai_gb.setter
    def terpakai_gb(self, value):
        if value < 0:
            raise ValueError("Pemakaian tidak boleh negatif")
        if value > self.kapasitas_gb:
            raise ValueError("Pemakaian melebihi kapasitas")
        self.__terpakai_gb = value

    def monitor(self):                      # Override
        persen = (self.__terpakai_gb / self.kapasitas_gb) * 100
        if persen > 90:
            self.catat_insiden("FS-PENUH", f"Disk {persen:.1f}% terpakai", "CRITICAL")
            return f"[WARNING] FileServer {self.hostname} hampir penuh ({persen:.1f}%)"
        return f"[OK] FileServer {self.hostname} normal ({persen:.1f}% terpakai)"

    def start_service(self):                # Override
        self.start()
        self._uptime_jam += 1
        return f"File service {self.hostname} aktif"


# === Admin ===
class Admin:
    # Class attributes
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
        if not value or len(value) < 3:
            raise ValueError("Username minimal 3 karakter")
        self.__username = value

    @property
    def password(self):
        return "*" * len(self.__password)

    @password.setter
    def password(self, value):
        if not value or len(value) < Admin.min_password_length:
            raise ValueError(f"Password minimal {Admin.min_password_length} karakter")
        self.__password = value

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, value):
        if value not in ("admin", "superadmin", "operator"):
            raise ValueError("Role tidak valid")
        self.__role = value

    @property
    def login_attempt(self):
        return self.__login_attempt

    def login(self, password):
        if password == self.__password:
            self.__login_attempt = 0
            return True
        self.__login_attempt += 1
        return False

    def info(self):
        return f"Admin: {self.__username} | Role: {self.__role} | Instansi: {Admin.nama_instansi}"

    # Asosiasi: Server diterima sebagai parameter dan digunakan sesaat
    def restart_server(self, server):
        server.stop()
        server.start()
        LogAktivitas(self.__username, f"Restart server {server.hostname}")
        return f"Server {server.hostname} berhasil di-restart oleh {self.__username}"

    @classmethod
    def ubah_min_password(cls, nilai_baru):
        if nilai_baru < 4:
            raise ValueError("Panjang minimum password tidak boleh < 4")
        cls.min_password_length = nilai_baru

    @classmethod
    def dari_dict(cls, data):
        return cls(data["username"], data["password"], data.get("role", "admin"))

    @staticmethod
    def validasi_username(username):
        return bool(username) and username.isalnum() and len(username) >= 3


# === Log Aktivitas ===
class LogAktivitas:
    # Class attributes
    total_log = 0
    riwayat = []

    def __init__(self, username, aksi):
        self.username = username
        self.aksi = aksi
        self.__waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        LogAktivitas.total_log += 1
        LogAktivitas.riwayat.append(self)

    @property
    def waktu(self):
        return self.__waktu

    def info(self):
        return f"[{self.__waktu}] {self.username} -> {self.aksi}"

    @classmethod
    def tampilkan_semua(cls):
        if not cls.riwayat:
            print("Belum ada log aktivitas.")
            return
        for log in cls.riwayat:
            print(log.info())

    @classmethod
    def reset(cls):
        cls.riwayat.clear()
        cls.total_log = 0

    @staticmethod
    def format_aksi(username, aksi):
        return f"{username}:: {aksi}"


# === Server Manager: Agregasi Server, Asosiasi Admin ===
class ServerManager:
    # Class attribute
    versi_sistem = "1.0.0"

    def __init__(self, admin):
        self.admin = admin                  # Asosiasi: admin dibuat di luar
        self.__daftar_server = []           # Agregasi: menampung referensi Server

    @property
    def daftar_server(self):
        return list(self.__daftar_server)

    # CREATE
    def tambah_server(self, server):
        if not Server.validasi_hostname(server.hostname):
            raise ValueError("Hostname tidak valid")
        if self.cari_server(server.hostname) is not None:
            raise ValueError(f"Server {server.hostname} sudah terdaftar")
        self.__daftar_server.append(server)
        LogAktivitas(self.admin.username, f"Tambah server {server.hostname}")

    # READ
    def get_all_server(self):
        return list(self.__daftar_server)

    def cari_server(self, hostname):
        for s in self.__daftar_server:
            if s.hostname == hostname:
                return s
        return None

    # UPDATE
    def update_server(self, hostname, ip_baru, cpu, ram):
        server = self.cari_server(hostname)
        if server is None:
            raise ValueError("Server tidak ditemukan")
        server.ip_address = ip_baru
        server.cpu_usage = cpu
        server.ram_usage = ram
        LogAktivitas(self.admin.username, f"Update server {hostname}")

    # DELETE
    def hapus_server(self, hostname):
        server = self.cari_server(hostname)
        if server is None:
            raise ValueError("Server tidak ditemukan")
        self.__daftar_server.remove(server)
        LogAktivitas(self.admin.username, f"Hapus server {hostname}")

    def monitor_semua_server(self):
        if not self.__daftar_server:
            print("Tidak ada server terdaftar.")
            return
        for s in self.__daftar_server:
            print(s.monitor())

    @classmethod
    def ubah_versi(cls, versi_baru):
        cls.versi_sistem = versi_baru

    @staticmethod
    def validasi_port(port):
        return isinstance(port, int) and 1 <= port <= 65535


# === MAIN ===
if __name__ == "__main__":
    print("=" * 60)
    print(f"{Admin.nama_instansi} - Sistem Informasi Manajemen Server")
    print(f"Versi: {ServerManager.versi_sistem} | Instansi: {Admin.nama_instansi}")
    print("=" * 60)

    # 1. Objek Admin
    print("\n[1] Admin")
    admin1 = Admin("sysadmin", "P@ssw0rd_025", "superadmin")
    admin2 = Admin.dari_dict({"username": "operator1", "password": "P@ssw0rd_OP", "role": "operator"})
    print(admin1.info())
    print(admin2.info())

    # 2. Objek Server
    print("\n[2] Server")
    web1 = WebServer("web-01", "192.168.1.10", port=80)
    web2 = WebServer("web-02", "192.168.1.11", port=8080, cpu_usage=85, ram_usage=70)
    db1 = DatabaseServer("db-01", "192.168.1.20", "produksi")
    db2 = DatabaseServer("db-02", "192.168.1.21", "backup")
    fs1 = FileServer("fs-01", "192.168.1.30", kapasitas_gb=500)
    fs2 = FileServer("fs-02", "192.168.1.31", kapasitas_gb=1000)
    db1.ukuran_gb = 50
    fs1.terpakai_gb = 480

    print(web1.tampilkan_info())
    print(web2.tampilkan_info())
    print(db1.tampilkan_info())
    print(fs1.tampilkan_info())

    # 3. ServerManager
    print("\n[3] ServerManager")
    manager1 = ServerManager(admin1)
    manager2 = ServerManager(admin2)

    manager1.tambah_server(web1)
    manager1.tambah_server(web2)
    manager1.tambah_server(db1)
    manager2.tambah_server(db2)
    manager2.tambah_server(fs1)
    manager2.tambah_server(fs2)

    print(f"Total server terdaftar: {Server.get_total_server()}")
    print(f"Manager 1: {[s.hostname for s in manager1.daftar_server]}")
    print(f"Manager 2: {[s.hostname for s in manager2.daftar_server]}")

    # 4. Polymorphism: List<Server> memanggil monitor()
    print("\n[4] Monitoring Semua Server (Polymorphism)")
    manager1.monitor_semua_server()
    manager2.monitor_semua_server()

    # 5. Start service
    print("\n[5] Start Service")
    print(web1.start_service())
    print(db1.start_service())
    print(fs1.start_service())

    # 6. Update
    print("\n[6] Update Server")
    manager1.update_server("web-01", "10.0.0.5", 45, 50)
    print(web1.tampilkan_info())

    # 7. Cari
    print("\n[7] Cari Server")
    found = manager1.cari_server("db-01")
    print(f"Ditemukan: {found.tampilkan_info() if found else 'Tidak ditemukan'}")

    # 8. Hapus
    print("\n[8] Hapus Server")
    manager2.hapus_server("fs-02")
    print(f"Sisa server manager2: {[s.hostname for s in manager2.daftar_server]}")

    # 9. Asosiasi: Admin memakai Server sebagai parameter
    print("\n[9] Asosiasi (Admin -> Server via parameter)")
    print(admin1.restart_server(web1))
    print(admin2.restart_server(db2))

    # 10. Komposisi: CatatanInsiden dibuat di dalam Server
    print("\n[10] Komposisi (Server -> CatatanInsiden)")
    web2.monitor()
    db1.monitor()
    fs1.monitor()
    print(f"Insiden web2  : {[str(i) for i in web2.daftar_insiden]}")
    print(f"Insiden db1   : {[str(i) for i in db1.daftar_insiden]}")
    print(f"Insiden fs1   : {[str(i) for i in fs1.daftar_insiden]}")

    # 11. Uji validasi setter (data tidak valid)
    print("\n[11] Uji Validasi Setter")
    try:
        web1.cpu_usage = -10
    except ValueError as e:
        print(f"Error: {e}")

    try:
        db1.ip_address = "999"
    except ValueError as e:
        print(f"Error: {e}")

    try:
        admin2.password = "123"
    except ValueError as e:
        print(f"Error: {e}")

    try:
        admin1.username = "ab"
    except ValueError as e:
        print(f"Error: {e}")

    try:
        fs1.terpakai_gb = 99999
    except ValueError as e:
        print(f"Error: {e}")

    web1.cpu_usage = 60
    admin2.password = "P@ssw0rd_025"
    print(f"CPU web-01 sekarang: {web1.cpu_usage}%")
    print(f"Password admin2 (masked): {admin2.password}")

    # 12. Class Method
    print("\n[12] Class Method")
    print(f"Total server: {Server.get_total_server()}")
    Server.ubah_threshold_cpu(90)
    print(f"Threshold CPU baru: {Server.max_cpu_threshold}")
    ServerManager.ubah_versi("1.1.0")
    print(f"Versi sistem: {ServerManager.versi_sistem}")
    Admin.ubah_min_password(10)
    print(f"Min password sekarang: {Admin.min_password_length}")

    # 13. Static Method
    print("\n[13] Static Method")
    print(f"validasi_hostname('web-01'): {Server.validasi_hostname('web-01')}")
    print(f"validasi_hostname('web 01'): {Server.validasi_hostname('web 01')}")
    print(f"validasi_username('operator1'): {Admin.validasi_username('operator1')}")
    print(f"validasi_username('operator2'): {Admin.validasi_username('operator2')}")
    print(f"validasi_port(8080): {ServerManager.validasi_port(8080)}")
    print(f"validasi_port(70000): {ServerManager.validasi_port(70000)}")
    print(f"format_aksi: {LogAktivitas.format_aksi('sysadmin', 'login')}")

    # 14. Log Aktivitas
    print("\n[14] Log Aktivitas")
    LogAktivitas.tampilkan_semua()
    print(f"Total log: {LogAktivitas.total_log}")

    # 15. Login Admin
    print("\n[15] Uji Login Admin")
    print(f"Login 'salah': {admin1.login('salah')}")
    print(f"Login 'P@ssw0rd_025': {admin1.login('P@ssw0rd_025')}")
    print(f"Attempt admin1: {admin1.login_attempt}")

    # 16. Isinstance (mengenali hierarki)
    print("\n[16] isinstance()")
    print(f"web1 isinstance WebServer    : {isinstance(web1, WebServer)}")
    print(f"web1 isinstance Server       : {isinstance(web1, Server)}")
    print(f"web1 isinstance DatabaseServer: {isinstance(web1, DatabaseServer)}")
    print(f"issubclass(WebServer, Server): {issubclass(WebServer, Server)}")