import os
import time
import requests
from playwright.sync_api import sync_playwright

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
VFS_EMAIL = os.environ['VFS_EMAIL']
VFS_PASSWORD = os.environ['VFS_PASSWORD']

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": mensagem,
        "parse_mode": "HTML"
    })

def verificar_vfs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto("https://visa.vfsglobal.com/ago/pt/prt/")
            page.wait_for_load_state("networkidle")
            page.fill('input[type="email"]', VFS_EMAIL)
            page.fill('input[type="password"]', VFS_PASSWORD)
            page.click('button[type="submit"]')
            page.wait_for_timeout(5000)
            conteudo = page.inner_text("body")
            if "not possible to proceed" in conteudo or "Verification Failed" in conteudo:
                print("Indisponível")
                return False
            else:
                enviar_telegram("✅ VFS DISPONÍVEL! Abre já o site!")
                return True
        except Exception as e:
            print(f"Erro: {e}")
            return False
        finally:
            browser.close()

while True:
    verificar_vfs()
    time.sleep(300)
