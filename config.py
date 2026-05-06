import os
import json
from pathlib import Path

CONFIG_DIR = Path(__file__).parent
CONFIG_FILE = CONFIG_DIR / 'config.json'


class Config:
    def __init__(self):
        self.bot_token = ''
        self.chat_id = ''
        self.monitoring_enabled = False
        self.auto_start = False
        self.notification_enabled = True
        self.load()

    def load(self):
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.bot_token = data.get('bot_token', '')
                    self.chat_id = data.get('chat_id', '')
                    self.monitoring_enabled = data.get('monitoring_enabled', False)
                    self.auto_start = data.get('auto_start', False)
                    self.notification_enabled = data.get('notification_enabled', True)
            except Exception as e:
                print(f"Config load error: {e}")

    def save(self):
        try:
            data = {
                'bot_token': self.bot_token,
                'chat_id': self.chat_id,
                'monitoring_enabled': self.monitoring_enabled,
                'auto_start': self.auto_start,
                'notification_enabled': self.notification_enabled
            }
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Config save error: {e}")
            return False

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self.save()


config = Config()
