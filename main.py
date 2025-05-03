import requests
from bs4 import BeautifulSoup
import time
from flask import Flask
import threading
import os

URL = 'https://hypervision.gg/checkout/?prod=1'
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHECK_INTERVAL = 60
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot attivo su Render!"

def send_telegram(msg):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': msg}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Errore invio notifica: {e}")

def check_slot():
    try:
        r = requests.get(URL, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        return "No slot left" not in soup.text
    except Exception as e:
        print(f"Errore durante il controllo: {e}")
        return False

def run_bot():
    notificato = False
    while True:
        if not notificato and check_slot():
            send_telegram("✅ SLOT DISPONIBILE SU HYPERVISION! CORRI!")
            notificato = True
        time.sleep(CHECK_INTERVAL)

def start_bot():
    t = threading.Thread(target=run_bot)
    t.start()

if __name__ == '__main__':
    start_bot()
    app.run(host='0.0.0.0', port=10000)
