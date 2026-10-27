import os
import yfinance as yf
import requests

# Mengambil token dari Environment Variables (GitHub Secrets)
TOKEN = os.getenv("TELEGRAM_TOKEN", "TOKEN_ANDA_JIKA_DI_LOKAL")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "CHAT_ID_ANDA_JIKA_DI_LOKAL")

def kirim_pesan_telegram(pesan):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": pesan, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Gagal kirim Telegram: {response.text}")
    except Exception as e:
        print(f"Error koneksi Telegram: {e}")

def cek_pasar():
    # 1. Pantau IHSG terlebih dahulu (^JKSE adalah kode ticker IHSG di Yahoo Finance)
    laporan_gabungan = "📈 *LAPORAN HARIAN PASAR SAHAM*\n" + "—" * 22 + "\n"
    
    try:
        ihsg = yf.Ticker("^JKSE")
        data_ihsg = ihsg.history(period="2d")
        if len(data_ihsg) >= 2:
            h_kemarin = data_ihsg['Close'].iloc[-2]
            h_hari_ini = data_ihsg['Close'].iloc[-1]
            perubahan_ihsg = ((h_hari_ini - h_kemarin) / h_kemarin) * 100
            
             arah_ihsg = "🟢" if perubahan_ihsg >= 0 else "🔴"
            laporan_gabungan += f"🇮🇩 *IHSG:* `{h_hari_ini:,.2f}` ({arah_ihsg} `{perubahan_ihsg:+.2f}%`)\n\n"
    except Exception as e:
        print(f"Error mengambil data IHSG: {e}")

    # 2. Daftar Saham yang Dipantau (IHSG + Saham Tren/Blue-Chip)
    # Anda bisa menambah atau mengganti kode saham di dalam daftar ini (.JK wajib untuk saham Indonesia)
    daftar_saham = {
        "GOTO.JK": "GoTo Gojek Tokopedia",
        "BBCA.JK": "Bank Central Asia",
        "BBRI.JK": "Bank Rakyat Indonesia",
        "BMRI.JK": "Bank Mandiri",
        "ASII.JK": "Astra International"
    }

    laporan_gabungan += "📊 *WATCHLIST SAHAM TERPILIH:*\n"
    
    for ticker, nama in daftar_saham.items():
        try:
            saham = yf.Ticker(ticker)
            data_historis = saham.history(period="2d")
            
            if len(data_historis) >= 2:
                harga_kemarin = data_historis['Close'].iloc[-2]
                harga_hari_ini = data_historis['Close'].iloc[-1]
                perubahan = ((harga_hari_ini - harga_kemarin) / harga_kemarin) * 100
                
                simbol_arah = "🟢" if perubahan >= 0 else "🔴"
                laporan_gabungan += (
                    f"• *{nama}* (`{ticker}`)\n"
                    f"  Harga: `{harga_hari_ini:,.2f}` | Perubahan: {simbol_arah} `{perubahan:+.2f}%`\n"
                )
        except Exception as e:
            print(f"Gagal memproses {ticker}: {e}")

    # Kirim seluruh laporan ringkasan ke Telegram Anda
    kirim_pesan_telegram(laporan_gabungan)

if __name__ == "__main__":
    cek_pasar()