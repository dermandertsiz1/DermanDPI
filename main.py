import customtkinter as ctk
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import threading
import subprocess
import os
import sys
import winreg  # Windows Başlangıç ayarlarına erişmek için ekledik

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class DermanDPIApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DermanDPI v1.0")
        self.geometry("450x400")
        self.resizable(False, False)

        self.icon_path = resource_path("app_icon.ico")
        if os.path.exists(self.icon_path):
            self.wm_iconbitmap(self.icon_path)

        self.is_running = False
        self.dpi_process = None
        self.tray_icon = None

        self.protocol('WM_DELETE_WINDOW', self.minimize_to_tray)

        # --- SEKMELER ---
        self.tabview = ctk.CTkTabview(self, width=420, height=380)
        self.tabview.pack(padx=15, pady=15)
        
        self.tabview.add("Ana Sayfa")
        self.tabview.add("Ayarlar")
        self.tabview.add("Hakkında")

        # --- 1. ANA SAYFA ---
        self.status_label = ctk.CTkLabel(self.tabview.tab("Ana Sayfa"), text="DURUM: PASİF", font=("Arial", 16, "bold"), text_color="#FF3B30")
        self.status_label.pack(pady=(40, 20))

        self.power_button = ctk.CTkButton(
            self.tabview.tab("Ana Sayfa"), 
            text="BAŞLAT", 
            font=("Arial", 18, "bold"),
            width=200, 
            height=60, 
            corner_radius=30, 
            fg_color="#34C759", 
            hover_color="#28A745",
            command=self.toggle_dpi
        )
        self.power_button.pack(pady=20)

        # --- 2. AYARLAR ---
        self.settings_label = ctk.CTkLabel(self.tabview.tab("Ayarlar"), text="DermanDPI Gelişmiş Mod", font=("Arial", 14, "bold"))
        self.settings_label.pack(pady=20)
        
        # Switch butonuna fonksiyonumuzu bağladık (command=self.toggle_startup)
        self.startup_switch = ctk.CTkSwitch(
            self.tabview.tab("Ayarlar"), 
            text="Windows Açılışında Otomatik Başlat",
            command=self.toggle_startup
        )
        self.startup_switch.pack(pady=10, padx=20, anchor="w")
        
        # Program her açıldığında mevcut Windows ayarına bakıp switch'i açık veya kapalı konumlandırır
        self.check_startup_status()

        # --- 3. HAKKINDA ---
        self.about_label = ctk.CTkLabel(
            self.tabview.tab("Hakkında"), 
            text="DermanDPI v1.0\n\nBu proje internet özgürlüğü için\naçık kaynaklı olarak geliştirilmiştir.\n\nKernel Seviyesi Paket Manipülasyonu\n\nGitHub: github.com/suprsh", 
            font=("Arial", 14),
            justify="center"
        )
        self.about_label.pack(pady=40)

    # --- WINDOWS BAŞLANGIÇ KONTROL FONKSİYONLARI ---
    def toggle_startup(self):
        # Kayıt defterindeki "Run" anahtarının yolu
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "DermanDPI"
        
        # PyInstaller ile derlendiğinde asıl .exe yolunu, yoksa .py yolunu alır
        if getattr(sys, 'frozen', False):
            app_path = sys.executable
        else:
            app_path = os.path.abspath(sys.argv[0])

        if self.startup_switch.get() == 1:
            try:
                # Windows Kayıt Defterine uygulamayı ekle
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, f'"{app_path}"')
                winreg.CloseKey(key)
                print("[DermanDPI] Windows başlangıcına başarıyla eklendi.")
            except Exception as e:
                print(f"Başlangıca eklenirken hata oluştu: {e}")
        else:
            try:
                # Windows Kayıt Defterinden uygulamayı sil
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
                winreg.DeleteValue(key, app_name)
                winreg.CloseKey(key)
                print("[DermanDPI] Windows başlangıcından kaldırıldı.")
            except FileNotFoundError:
                pass # Zaten yoksa hata verme
            except Exception as e:
                print(f"Başlangıçtan silinirken hata oluştu: {e}")

    def check_startup_status(self):
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "DermanDPI"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            winreg.QueryValueEx(key, app_name)
            winreg.CloseKey(key)
            self.startup_switch.select() # Eğer kayıt varsa switch'i açık yap
        except FileNotFoundError:
            self.startup_switch.deselect() # Yoksa kapalı yap
        except Exception:
            self.startup_switch.deselect()

    def create_tray_icon_image(self):
        image = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
        dc = ImageDraw.Draw(image)
        color = '#34C759' if self.is_running else '#FF3B30'
        dc.ellipse([12, 12, 52, 52], fill=color)
        return image

    def minimize_to_tray(self):
        self.withdraw()
        if not self.tray_icon:
            menu = (
                item('Göster', self.show_window, default=True),
                item('Başlat / Durdur', self.toggle_dpi_from_tray),
                item('Tamamen Kapat', self.quit_application)
            )
            current_image = self.create_tray_icon_image()
            self.tray_icon = pystray.Icon("DermanDPI", current_image, "DermanDPI", menu)
            threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def show_window(self):
        if self.tray_icon:
            self.tray_icon.stop()
            self.tray_icon = None
        self.deiconify()

    def quit_application(self):
        self.stop_dpi_engine()
        if self.tray_icon:
            self.tray_icon.stop()
        self.destroy()

    def toggle_dpi_from_tray(self):
        self.toggle_dpi()
        if self.tray_icon:
            self.tray_icon.icon = self.create_tray_icon_image()

    def toggle_dpi(self):
        if not self.is_running:
            self.start_dpi_engine()
        else:
            self.stop_dpi_engine()
        
        if self.tray_icon:
            self.tray_icon.icon = self.create_tray_icon_image()

    def start_dpi_engine(self):
        exe_path = resource_path("dermandpi_core.exe")
        
        if not os.path.exists(exe_path):
            self.status_label.configure(text="HATA: Motor dosyası bulunamadı!", text_color="#FF3B30")
            return

        try:
            self.is_running = True
            self.status_label.configure(text="DURUM: AKTİF", text_color="#34C759")
            self.power_button.configure(text="DURDUR", fg_color="#FF3B30", hover_color="#C73E3A")

            self.dpi_process = subprocess.Popen(
                [exe_path, "-9"],
                creationflags=subprocess.CREATE_NO_WINDOW,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("[DermanDPI] Güçlü motor arka planda başlatıldı.")
        except Exception as e:
            print(f"Motor başlatılamadı: {e}")

    def stop_dpi_engine(self):
        self.is_running = False
        self.status_label.configure(text="DURUM: PASİF", text_color="#FF3B30")
        self.power_button.configure(text="BAŞLAT", fg_color="#34C759", hover_color="#28A745")

        if self.dpi_process:
            subprocess.Popen(f"taskkill /F /T /PID {self.dpi_process.pid}", creationflags=subprocess.CREATE_NO_WINDOW)
            self.dpi_process = None
            print("[DermanDPI] Güçlü motor durduruldu.")

if __name__ == "__main__":
    app = DermanDPIApp()
    app.mainloop()