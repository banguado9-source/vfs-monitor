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

def verificar_vagas(pais, missao, nome):
    try:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "pt-AO,pt;q=0.9",
            "Origin": "https://visa.vfsglobal.com",
            "Referer": "https://visa.vfsglobal.com/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36"
        }
        url = "https://lift-api.vfsglobal.com/appointment/slot/checkslotavailable/" + pais + "/" + missao
        r = requests.get(url, headers=headers, timeout=15)
        print(nome + " status: " + str(r.status_code))
        print(nome + " resposta: " + r.text[:300])

        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and len(data) > 0:
                enviar_telegram("VAGA DISPONIVEL! VFS " + nome + "\nAbre ja o site!\nhttps://visa.vfsglobal.com/" + pais + "/pt/" + missao + "/")
                print(nome + " VAGAS ENCONTRADAS!")
            else:
                print(nome + " sem vagas")
        else:
            print(nome + " erro " + str(r.status_code))
    except Exception as e:
        print(nome + " erro: " + str(e))

portais = [
    ("ago", "prt", "Angola-Portugal"),
    ("bra", "prt", "Brasil-Portugal"),
]

enviar_telegram("VFS Monitor v4 iniciado!")

while True:
    for pais, missao, nome in portais:
        verificar_vagas(pais, missao, nome)
        time.sleep(5)
    time.sleep(300)
