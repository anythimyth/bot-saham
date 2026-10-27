import yfinance as yf
import requests

def kirim_pesan_telegram(pesan):
    token = "8560539448:AAFV1SH85rDUl65ffy6V9qzrvZ9uB-MOHIY"
    chat_id = "7178778686"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": pesan, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def cek_harga_saham(ticker_symbol):
    try:
        # Mengambil data menggunakan yfinance (contoh: "GOTO.JK" untuk GoTo atau "AAPL" untuk Apple)
        saham = yf.Ticker(ticker_symbol)
        data_historis = saham.history(period="2d")
        
        if len(data_historis) >= 2:
            harga_kemarin = data_historis['Close'].iloc[-2]
            harga_hari_ini = data_historis['Close'].iloc[-1]
            perubahan = ((harga_hari_ini - harga_kemarin) / harga_kemarin) * 100
            
            pesan = (
                f"📊 *Laporan Pemantauan Pasar*\n"
                f"Ticker: `{ticker_symbol}`\n"
                f"Harga Terakhir: `{harga_hari_ini:.2f}`\n"
                f"Perubahan: `{perubahan:.2f}%`"
            )
            kirim_pesan_telegram(pesan)
        else:
            print("Data tidak cukup.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    # Contoh memantau saham (bisa diganti kode saham lain, misal 'TLKM.JK' atau 'BBCA.JK')
    cek_harga_saham("GOTO.JK")