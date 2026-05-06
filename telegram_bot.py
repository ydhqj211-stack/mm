import requests
from datetime import datetime


class TelegramBot:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
        self._last_check = None

    def send_message(self, text, parse_mode='Markdown'):
        try:
            url = f"{self.api_url}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': parse_mode
            }
            response = requests.post(url, json=payload, timeout=10)
            result = response.json()
            return result.get('ok', False)
        except Exception as e:
            print(f"Telegram send error: {e}")
            return False

    def send_photo(self, photo_path, caption=None):
        try:
            url = f"{self.api_url}/sendPhoto"
            payload = {
                'chat_id': self.chat_id,
                'caption': caption or ''
            }
            with open(photo_path, 'rb') as photo:
                files = {'photo': photo}
                response = requests.post(url, data=payload, files=files, timeout=10)
            result = response.json()
            return result.get('ok', False)
        except Exception as e:
            print(f"Telegram send photo error: {e}")
            return False

    def get_updates(self, offset=None, timeout=0):
        try:
            url = f"{self.api_url}/getUpdates"
            payload = {'timeout': timeout}
            if offset:
                payload['offset'] = offset
            response = requests.get(url, params=payload, timeout=30)
            result = response.json()
            if result.get('ok'):
                return result.get('result', [])
            return []
        except Exception as e:
            print(f"Telegram get updates error: {e}")
            return []

    def get_chat_id(self):
        updates = self.get_updates()
        if updates:
            return updates[0].get('message', {}).get('chat', {}).get('id')
        return None

    def set_webhook(self, webhook_url):
        try:
            url = f"{self.api_url}/setWebhook"
            payload = {'url': webhook_url}
            response = requests.post(url, json=payload, timeout=10)
            result = response.json()
            return result.get('ok', False)
        except Exception as e:
            print(f"Telegram set webhook error: {e}")
            return False

    def delete_webhook(self):
        try:
            url = f"{self.api_url}/deleteWebhook"
            response = requests.get(url, timeout=10)
            result = response.json()
            return result.get('ok', False)
        except Exception as e:
            print(f"Telegram delete webhook error: {e}")
            return False

    def send_sms_notification(self, sender, message, time_str=None):
        if not time_str:
            time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        text = f"📱 *新短信*\n\n📤 *发件人:* `{sender}`\n⏰ *时间:* {time_str}\n💬 *内容:*\n{message}"
        return self.send_message(text)

    def test_connection(self):
        return self.send_message("✅ SMS Watcher 连接测试成功！\n\n如果收到这条消息，说明配置正确。")
