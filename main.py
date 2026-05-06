import sys
import os
import threading
from datetime import datetime

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.recycleview import RecycleView
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty
from kivy.storage.jsonstore import JsonStore

from sms_monitor import SMSMonitor
from telegram_bot import TelegramBot


class SMSItemLayout(BoxLayout):
    sender = StringProperty()
    message = StringProperty()
    time = StringProperty()


class StatusCard(BoxLayout):
    status_text = StringProperty()
    is_active = BooleanProperty(False)


class SMSWatcherApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sms_monitor = None
        self.telegram_bot = None
        self.is_monitoring = False
        self.store = JsonStore('config.json')
        self.recent_sms = []

    def on_start(self):
        self.load_config()
        self.init_services()

    def load_config(self):
        if self.store.exists('telegram'):
            config = self.store.get('telegram')
            self.ids.bot_token.text = config.get('bot_token', '')
            self.ids.chat_id.text = config.get('chat_id', '')
        if self.store.exists('monitoring'):
            self.is_monitoring = self.store.get('monitoring').get('active', False)
            self.ids.monitor_switch.active = self.is_monitoring

    def save_config(self):
        self.store.put('telegram', bot_token=self.ids.bot_token.text, chat_id=self.ids.chat_id.text)
        self.store.put('monitoring', active=self.is_monitoring)

    def init_services(self):
        bot_token = self.ids.bot_token.text
        chat_id = self.ids.chat_id.text
        if bot_token and chat_id:
            self.telegram_bot = TelegramBot(bot_token, chat_id)
            self.sms_monitor = SMSMonitor(on_sms_received=self.on_sms_received)
            if self.is_monitoring:
                self.start_monitoring()

    def on_sms_received(self, sms_data):
        message = f"📱 新短信\n\n📤 发件人: {sms_data['sender']}\n⏰ 时间: {sms_data['time']}\n💬 内容:\n{sms_data['message']}"
        if self.telegram_bot:
            threading.Thread(target=self.telegram_bot.send_message, args=(message,)).start()
        Clock.schedule_once(lambda dt: self.add_sms_to_list(sms_data))

    def add_sms_to_list(self, sms_data):
        self.recent_sms.insert(0, sms_data)
        if len(self.recent_sms) > 20:
            self.recent_sms.pop()
        self.update_sms_list()

    def update_sms_list(self):
        rv = self.ids.sms_list
        rv.data = [{'sender': sms['sender'], 'message': sms['message'][:50] + '...' if len(sms['message']) > 50 else sms['message'], 'time': sms['time']} for sms in self.recent_sms]

    def start_monitoring(self):
        if not self.sms_monitor:
            if not self.ids.bot_token.text or not self.ids.chat_id.text:
                self.show_popup('错误', '请先配置 Telegram Bot Token 和 Chat ID')
                return
            self.telegram_bot = TelegramBot(self.ids.bot_token.text, self.ids.chat_id.text)
            self.sms_monitor = SMSMonitor(on_sms_received=self.on_sms_received)
        try:
            self.sms_monitor.start()
            self.is_monitoring = True
            self.ids.status_label.text = '状态: 监控中'
            self.ids.status_label.color = (0, 1, 0, 1)
            self.save_config()
            self.show_popup('成功', '短信监控已启动')
        except Exception as e:
            self.show_popup('错误', f'启动监控失败: {str(e)}')

    def stop_monitoring(self):
        if self.sms_monitor:
            self.sms_monitor.stop()
            self.is_monitoring = False
            self.ids.status_label.text = '状态: 已停止'
            self.ids.status_label.color = (1, 0, 0, 1)
            self.save_config()

    def on_monitor_switch(self, instance, value):
        if value:
            self.start_monitoring()
        else:
            self.stop_monitoring()

    def test_telegram(self):
        bot_token = self.ids.bot_token.text
        chat_id = self.ids.chat_id.text
        if not bot_token or not chat_id:
            self.show_popup('错误', '请输入 Bot Token 和 Chat ID')
            return
        threading.Thread(target=self._test_telegram_thread, args=(bot_token, chat_id)).start()

    def _test_telegram_thread(self, bot_token, chat_id):
        try:
            bot = TelegramBot(bot_token, chat_id)
            success = bot.send_message("🧪 SMS Watcher 连接测试成功！\n\n如果收到这条消息，说明配置正确。")
            if success:
                Clock.schedule_once(lambda dt: self.show_popup('成功', 'Telegram Bot 连接测试成功！'))
            else:
                Clock.schedule_once(lambda dt: self.show_popup('失败', '发送消息失败，请检查Chat ID是否正确'))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_popup('错误', f'连接失败: {str(e)}'))

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.3))
        popup.open()

    def load_history(self):
        if not self.sms_monitor:
            self.sms_monitor = SMSMonitor(on_sms_received=self.on_sms_received)
        try:
            history = self.sms_monitor.get_all_sms(limit=50)
            for sms in reversed(history):
                self.add_sms_to_list(sms)
            self.show_popup('成功', f'已加载 {len(history)} 条历史短信')
        except Exception as e:
            self.show_popup('错误', f'读取历史短信失败: {str(e)}\n\n注意: 未Root的手机需要手动备份短信。')

    def build(self):
        return Builder.load_file('sms_watcher.kv')


from kivy.lang import Builder
Builder.load_file('sms_watcher.kv')