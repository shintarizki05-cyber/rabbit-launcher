import sys
import os
import subprocess
import minecraft_launcher_lib
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QTextEdit, QMessageBox
)

class MinecraftLauncherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rabbit Launcher - All Versions & Loaders")
        self.resize(600, 450)

        # Path direktori Minecraft (.minecraft)
        self.minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()

        self.init_ui()
        self.load_versions()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input Username
        user_layout = QHBoxLayout()
        user_label = QLabel("Username:")
        self.username_input = QLineEdit("PlayerRabbit")
        user_layout.addWidget(user_label)
        user_layout.addWidget(self.username_input)
        layout.addLayout(user_layout)

        # Dropdown Versi Minecraft
        version_layout = QHBoxLayout()
        version_label = QLabel("Pilih Versi:")
        self.version_combo = QComboBox()
        version_layout.addWidget(version_label)
        version_layout.addWidget(self.version_combo)
        layout.addLayout(version_layout)

        # Tombol Install & Launch
        btn_layout = QHBoxLayout()
        self.install_btn = QPushButton("Install / Download")
        self.install_btn.clicked.connect(self.install_game)
        self.launch_btn = QPushButton("Launch Minecraft")
        self.launch_btn.clicked.connect(self.launch_game)
        btn_layout.addWidget(self.install_btn)
        btn_layout.addWidget(self.launch_btn)
        layout.addLayout(btn_layout)

        # Log Console
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        layout.addWidget(QLabel("Log Status:"))
        layout.addWidget(self.console_output)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def log(self, message):
        self.console_output.append(message)

    def load_versions(self):
        self.log("Memuat daftar versi Minecraft...")
        try:
            versions = minecraft_launcher_lib.utils.get_version_list(self.minecraft_directory)
            for version in versions:
                self.version_combo.addItem(version['id'], version['type'])
            self.log("Daftar versi berhasil dimuat!")
        except Exception as e:
            self.log(f"Gagal memuat versi: {str(e)}")

    def install_game(self):
        version_id = self.version_combo.currentText()
        self.log(f"Memulai instalasi versi: {version_id}...")

        try:
            # Callback untuk memantau progress unduhan
            def set_status(status):
                self.log(status)

            callback = {
                "setStatus": set_status,
                "setProgress": lambda progress: self.log(f"Progress: {progress}%"),
                "setMax": lambda max_val: None
            }

            minecraft_launcher_lib.install.install_minecraft_version(
                version_id=version_id,
                minecraft_directory=self.minecraft_directory,
                callback=callback
            )
            QMessageBox.information(self, "Sukses", f"Versi {version_id} berhasil diinstal!")
            self.log(f"Instalasi {version_id} selesai.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menginstal: {str(e)}")
            self.log(f"Error instalasi: {str(e)}")

    def launch_game(self):
        username = self.username_input.text()
        version_id = self.version_combo.currentText()

        if not username:
            QMessageBox.warning(self, "Peringatan", "Masukkan username terlebih dahulu!")
            return

        self.log(f"Menyiapkan peluncuran untuk {username} pada versi {version_id}...")

        try:
            # Pengaturan akun offline/cracked sederhana
            options = {
                "username": username,
                "uuid": "12345678-1234-1234-1234-123456789012",
                "token": "123456",
            }

            minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(
                version=version_id,
                minecraft_directory=self.minecraft_directory,
                options=options
            )

            self.log("Menjalankan Minecraft...")
            subprocess.Popen(minecraft_command)
            self.log("Minecraft berhasil diluncurkan!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menjalankan game: {str(e)}")
            self.log(f"Error launch: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = MinecraftLauncherApp()
    launcher.show()
    sys.exit(app.exec_())
      
