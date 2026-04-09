import sys
import os
import threading
import time
import webbrowser

# PyInstaller ile paketlendiğinde dosya yollarını düzelt
if getattr(sys, 'frozen', False):
    # EXE olarak çalışıyor
    BASE_DIR = sys._MEIPASS
    # instance klasörünü EXE'nin yanına koy
    INSTANCE_DIR = os.path.join(os.path.dirname(sys.executable), 'instance')
    STATIC_DIR  = os.path.join(BASE_DIR, 'app', 'static')
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'app', 'templates')
else:
    # Normal Python ortamı
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')

# instance klasörünü oluştur
os.makedirs(INSTANCE_DIR, exist_ok=True)

# Ortam değişkenlerini elle ayarla (.env dosyasına gerek kalmasın)
os.environ.setdefault('SECRET_KEY', 'fitmarket-super-secret-key-2024')
os.environ.setdefault('DATABASE_URL', f'sqlite:///{os.path.join(INSTANCE_DIR, "fitmarket.db")}')
os.environ.setdefault('FLASK_ENV', 'production')
os.environ.setdefault('FLASK_DEBUG', '0')

sys.path.insert(0, BASE_DIR)

from app import create_app

PORT = 5000
URL  = f'http://localhost:{PORT}'


def open_browser():
    """Sunucu hazır olunca tarayıcıyı aç"""
    time.sleep(1.5)
    webbrowser.open(URL)


app = create_app('production')

if __name__ == '__main__':
    print("=" * 50)
    print("  FitMarket başlatılıyor...")
    print(f"  Adres: {URL}")
    print("  Kapatmak için bu pencereyi kapatın.")
    print("=" * 50)

    # Tarayıcıyı arka planda aç
    t = threading.Thread(target=open_browser, daemon=True)
    t.start()

    # Flask'ı başlat
    app.run(debug=False, host='127.0.0.1', port=PORT, use_reloader=False)
