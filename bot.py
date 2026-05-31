import os
import time
import requests

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

def enviar_telegram(mensagem):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "HTML"},
            timeout=10
        )
    except Exception as e:
        print(f"Erro Telegram: {e}")

def verificar_vfs(url, portal):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "pt-PT,pt;q=0.9",
        }
        r = requests.get(url, headers=headers, timeout=15)
        texto = r.text.lower()

        if "not possible to proceed" in texto or "verification failed" in texto:
            print(f"[{portal}] Facial indisponivel")
            return False
        elif r.status_code == 200:
            print(f"[{portal}] Site acessivel!")
            enviar_telegram(
                f"✅ <b>VFS {portal}</b>\n"
                f"O site esta a responder!\n"
                f"Verifica manualmente agora!\n"
                f"🔗 {url}"
            )
            return True
    except Exception as e:
        print(f"[{portal}] Erro: {e}")
    return False

portais = [
    ("https://visa.vfsglobal.com/ago/pt/prt/", "Angola"),
    ("https://visa.vfsglobal.com/bra/pt/prt/", "Brasil"),
]

enviar_telegram("🤖 <b>VFS Monitor iniciado!</b>\nA monitorizar Angola e Brasil.")

while True:
    for url, portal in portais:
