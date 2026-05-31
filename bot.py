import os
import time
import requests

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

def enviar_telegram(mensagem):
    try:
        requests.post(
            "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage",
            json={"chat_id": CHAT_ID, "text": mensagem},
            timeout=10
        )
    except Exception as e:
        print("Erro Telegram: " + str(e))

def verificar_vfs(pais, portal):
    try:
        url = "https://lift.vfsglobal.com/prod/api/v1/appointment/get-available-slots"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://visa.vfsglobal.com/",
            "Origin": "https://visa.vfsglobal.com",
            "country": pais,
            "mission": "prt"
        }
        r = requests.get(url, headers=headers, timeout=15)
        print(portal + " status: " + str(r.status_code))
        print(portal + " resposta: " + r.text[:200])

        if r.status_code == 200:
            data = r.json()
            if data and len(data) > 0:
                enviar_telegram("VAGA DISPONIVEL! VFS " + portal + "\nAbre ja o site!\nhttps://visa.vfsglobal.com/" + pais + "/pt/prt/")
            else:
                print(portal + " sem vagas")
        else:
            print(portal + " erro " + str(r.status_code))
    except Exception as e:
        print(portal + " erro: " + str(e))

portais = [
    ("ago", "Angola"),
    ("bra", "Brasil"),
]

enviar_telegram("VFS Monitor v2 iniciado!")

while True:
    for pais, portal in portais:
        verificar_vfs(pais, portal)
        time.sleep(5)
    time.sleep(300)
