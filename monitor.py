import os
import requests
from bs4 import BeautifulSoup

url = 'https://ticketplus.com.tw/activity/3abadeef4bf5bb33f25de89e9a49a3e0'
keywords = ['立即購票', '尚有票', '釋票']
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

def send_discord_notification(message):
    if not DISCORD_WEBHOOK_URL:
        print("❗ 未設定 Discord Webhook URL")
        return
    res = requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    if res.status_code == 204:
        print("✅ 通知已發送 Discord")
    else:
        print(f"❌ Discord 發送失敗，狀態碼: {res.status_code}")

def check_ticket():
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        text = soup.get_text()

        if any(k in text for k in keywords):
            send_discord_notification(f"🎟️ 釋票啦！快搶票：{url}")
        else:
            print("🔍 尚未釋票，持續監控中...")
    except Exception as e:
        print("🛑 發生錯誤:", e)

if __name__ == '__main__':
    send_discord_notification("🧪 測試通知：Webhook 正常運作！")
