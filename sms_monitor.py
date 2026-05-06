import sys
import threading
from datetime import datetime
from android.broadcast import BroadcastReceiver
from android import mActivity


class SMSMonitor:
    def __init__(self, on_sms_received=None):
        self.on_sms_received = on_sms_received
        self.is_running = False
        self._receiver = None
        self._last_sms_id = None

    def start(self):
        if self.is_running:
            return
        self.is_running = True
        self._receiver = BroadcastReceiver(self._on_sms, actions=['android.provider.Telephony.SMS_RECEIVED'])
        self._receiver.start()
        self._get_last_sms_id()

    def stop(self):
        if not self.is_running:
            return
        self.is_running = False
        if self._receiver:
            self._receiver.stop()

    def _get_last_sms_id(self):
        try:
            cursor = mActivity.getContentResolver().query(
                mActivityCALL("android.net.Uri", "parse", "content://sms/inbox"),
                ["_id"],
                None,
                None,
                "date DESC"
            )
            if cursor and cursor.moveToFirst():
                self._last_sms_id = cursor.getString(0)
                cursor.close()
        except:
            pass

    def _on_sms(self, context, intent):
        if not self.on_sms_received:
            return
        try:
            from android.provider import Telephony
            messages = Telephony.Sms.Intents.getMessagesFromIntent(intent)
            for message in messages:
                sms_data = {
                    'sender': message.getOriginatingAddress(),
                    'message': message.getMessageBody(),
                    'time': datetime.fromtimestamp(message.getTimestampMillis() / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                    'timestamp': message.getTimestampMillis()
                }
                if self._last_sms_id != str(message.getIndex()):
                    self._last_sms_id = str(message.getIndex())
                    self.on_sms_received(sms_data)
        except Exception as e:
            print(f"SMS parse error: {e}")

    def get_all_sms(self, limit=50):
        sms_list = []
        try:
            uri = mActivity.call("android.net.Uri", "parse", "content://sms/inbox")
            cursor = mActivity.getContentResolver().query(
                uri,
                ["_id", "address", "body", "date"],
                None,
                None,
                "date DESC"
            )
            if cursor:
                count = 0
                while cursor.moveToNext() and count < limit:
                    sms_list.append({
                        'sender': cursor.getString(1),
                        'message': cursor.getString(2),
                        'time': datetime.fromtimestamp(int(cursor.getString(3)) / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    })
                    count += 1
                cursor.close()
        except Exception as e:
            print(f"Get SMS error: {e}")
        return sms_list


def mActivityCALL(class_name, method, *args):
    if method == "parse":
        return mActivity.getContentResolver().query(args[0], ["_id", "address", "body", "date"], None, None, "date DESC")
    return None