# 🚀 DermanDPI v1.0.0

DermanDPI, kernel (çekirdek) seviyesinde paket manipülasyonu yaparak internet üzerindeki sansürleri, yavaşlatmaları ve engelleri (DPI - Deep Packet Inspection) aşmanızı sağlayan, modern ve kullanıcı dostu bir Windows arayüzüdür. 

Güçlü **GoodbyeDPI** motorunu temel alır, tamamen kişiselleştirilmiş ve arka planda sessizce çalışacak şekilde optimize edilmiştir.

---

## ✨ Özellikler

* 🛡️ **Kernel Seviyesi Koruma:** `WinDivert` sürücüsü ile paketleri yerinde işler, proxy veya VPN gibi internetinizi yavaşlatmaz.
* 🎨 **Modern ve Şık Arayüz:** `CustomTkinter` ile geliştirilmiş, göz yormayan karanlık mod desteği.
* 📥 **Sistem Tepsisi (System Tray) Desteği:** Programı kapattığınızda tamamen kapanmaz, sağ alttaki gizli simgelere küçülür.
* 🟢🔴 **Dinamik Durum Işığı:** Sağ alttaki simgeye bakarak motorun aktif (Yeşil) mi yoksa pasif (Kırmızı) mi olduğunu anında görebilirsiniz.
* ⚙️ **Otomatik Başlatma:** Windows açıldığında otomatik olarak arka planda başlama seçeneği.

---

## 🛠️ Nasıl Kullanılır?

1. Projenin **[Releases](https://github.com/dermandertsiz1/DermanDPI/releases)** sayfasından en güncel `DermanDPI.exe` dosyasını indirin.
2. İndirdiğiniz `.exe` dosyasına **sağ tıklayın** ve **"Yönetici Olarak Çalıştır"** seçeneğini seçin *(Sürücü yükleyebilmesi için yönetici yetkisi şarttır)*.
3. **BAŞLAT** butonuna basarak özgür internetin tadını çıkarın! Discord, Roblox ve diğer engelli platformlara anında erişim sağlayın.
4. Programı gizlemek için sağ üstteki **X** butonuna basmanız yeterlidir. Tamamen kapatmak isterseniz sağ alttaki renkli daireye sağ tıklayıp **"Tamamen Kapat"** diyebilirsiniz.

---

## 💻 Geliştiriciler İçin (Kaynak Koddan Çalıştırma)

Eğer projeyi kaynak koddan çalıştırmak veya geliştirmek isterseniz:

```bash
# Projeyi bilgisayarınıza indirin
git clone [https://github.com/dermandertsiz1/DermanDPI.git](https://github.com/dermandertsiz1/DermanDPI.git)

# Gerekli kütüphaneleri yükleyin
pip install customtkinter pystray pillow pyinstaller
