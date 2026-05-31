import os
import time
import requests

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

def enviar_telegram(mensagem):
    try:
        requests.post(
            "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage",
            json={"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "HTML"},
            timeout=10
        )
    except Exception as e:
        print("Erro Telegram: " + str(e))

def verificar_vfs(url, portal):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        texto = r.text.lower()
        if "not possible to proceed" in texto:
            print(portal + " indisponivel")
        else:
            print(portal + " disponivel!")
            enviar_telegram("VFS " + portal + " disponivel!\n" + url)
    except Exception as e:
        print(portal + " erro: " + str(e))

portais = [
    ("https://visa.vfsglobal.com/ago/pt/prt/", "Angola"),
    ("https://visa.vfsglobal.com/bra/pt/prt/", "Brasil"),
]

enviar_telegram("VFS Monitor iniciado!")

while True:
    for url, portal in portais:
        verificar_vfs(url, portal)
        time.sleep(5)
    time.sleep(300)
