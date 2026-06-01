import time
import requests

TELEGRAM_TOKEN = "8613306426:AAHP9sHNegN3J0MQOO8LQtBnHZAS_4vwzRw"
CHAT_ID = "6088313374"

def enviar_telegram(mensagem):
    try:
        requests.post(
            "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage",
            json={"chat_id": CHAT_ID, "text": mensagem},
            timeout=10
        )
    except Exception as e:
        print("Erro: " + str(e))

def verificar(url, nome):
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        print(nome + " OK " + str(r.status_code))
    except Exception as e:
        print(nome + " erro: " + str(e))

enviar_telegram("VFS Monitor v3 iniciado!")

while True:
    verificar("https://visa.vfsglobal.com/ago/pt/prt/", "Angola")
    time.sleep(5)
    verificar("https://visa.vfsglobal.com/bra/pt/prt/", "Brasil")
    time.sleep(295)
