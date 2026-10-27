import os
import yfinance as yf
import requests

TOKEN = os.getenv("TELEGRAM_TOKEN", "TOKEN_ANDA_JIKA_DI_LOKAL")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "CHAT_ID_ANDA_JIKA_DI_LOKAL")

def kirim_pesan_telegram(pesan):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": pesan, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error Telegram: {e}")

def pantau_dan_analisis_saham(ticker_symbol, batas_persen=1.5):
    try:
        saham = yf.Ticker(ticker_symbol)
        # Mengambil data 5 hari ke belakang untuk analisis tren mingguan
        data_historis = saham.history(period="5d")
        
        if len(data_historis) >= 5:
            harga_kemarin = data_historis['Close'].iloc[-2]
            harga_hari_ini = data_historis['Close'].iloc[-1]
            perubahan_harian = ((harga_hari_ini - harga_kemarin) / harga_kemarin) * 100
            
            # Hitung juga perubahan dalam 5 hari terakhir (tren jangka pendek)
            harga_5_hari_lalu = data_historis['Close'].iloc[0]
            perubahan_mingguan = ((harga_hari_ini - harga_5_hari_lalu) / harga_5_hari_lalu) * 100
            
            pesan = (
                f"📊 *Analisis Pasar: {ticker_symbol}*\n"
                f"• Harga Terakhir: `{harga_hari_ini:,.2f}`\n"
                f"• Perubahan Harian: `{perubahan_harian:+.2f}%`\n"
                f"• Tren 5 Hari: `{perubahan_mingguan:+.2f}%`"
            )
            
            # Logika Alert Multi-Kondisi
            status_alert = False
            if perubahan_harian <= -batas_persen:
                pesan += f"\n\n🚨 *ALERT HARIAN:* Penurunan tajam harian mencapai {perubahan_harian:.2f}%!"
                status_alert = True
            elif perubahan_harian >= batas_persen:
                pesan += f"\n\n🚀 *ALERT HARIAN:* Lonjakan harian mencapai {perubahan_harian:.2f}%!"
                status_alert = True
                
            if perubahan_mingguan <= -4.0:
                pesan += f"\n\n⚠️ *TREN MINGGUAN:* Tekanan jual kuat dalam 5 hari terakhir ({perubahan_mingguan:.2f}%)!"
                status_alert = True

            # Kirim pesan jika ada kondisi alert, atau Anda bisa mengatur agar laporan rutin tetap masuk
            if status_alert:
                kirim_pesan_telegram(pesan)
            else:
                print(f"{ticker_symbol}: Pergerakan stabil, tidak ada alert mendesak.")
        else:
            print(f"Data {ticker_symbol} tidak mencukupi.")
    except Exception as e:
        print(f"Error pada {ticker_symbol}: {e}")

if __name__ == "__main__":
    daftar_saham = ["GOTO.JK", "BBCA.JK"]
    for kode in daftar_saham:
        pantau_dan_analisis_saham(kode, batas_persen=1.5)