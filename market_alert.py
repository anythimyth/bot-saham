import os
import yfinance as yf
import requests

# Mengambil token dari Environment Variables (GitHub Secrets) atau fallback manual
TOKEN = os.getenv("TELEGRAM_TOKEN", "TOKEN_ANDA_JIKA_DI_LOKAL")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "CHAT_ID_ANDA_JIKA_DI_LOKAL")

def kirim_pesan_telegram(pesan):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": pesan, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error Telegram: {e}")

def pantau_dan_analisis_saham(ticker_symbol, batas_persen=1.0):
    try:
        saham = yf.Ticker(ticker_symbol)
        data_historis = saham.history(period="2d")
        
        if len(data_historis) >= 2:
            harga_kemarin = data_historis['Close'].iloc[-2]
            harga_hari_ini = data_historis['Close'].iloc[-1]
            perubahan = ((harga_hari_ini - harga_kemarin) / harga_kemarin) * 100
            
            pesan = (
                f"📊 *Update Pasar (GitHub Actions): {ticker_symbol}*\n"
                f"• Harga Terakhir: `{harga_hari_ini:,.2f}`\n"
                f"• Perubahan: `{perubahan:+.2f}%`"
            )
            
            if perubahan <= -batas_persen or perubahan >= batas_persen:
                pesan += f"\n\n🚨 *Alert:* Pergerakan signifikan melebihi {batas_persen}%!"
            
            kirim_pesan_telegram(pesan)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Bisa memantau beberapa saham sekaligus
    daftar_saham = ["GOTO.JK", "BBCA.JK"]
    for kode in daftar_saham:
        pantau_dan_analisis_saham(kode, batas_persen=1.0)