from BlueService import STEP, settings_helper
from BlueService.config import OWNER
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from BlueService.sql_helpers import UsersHelper, AdminsHelper
import re

user_helper = UsersHelper()
admins_helper = AdminsHelper()

class OwnerFilter(filters.Filter):
    async def __call__(self, client : Client, message_or_callback: Message | CallbackQuery):
        if not message_or_callback.from_user:
            return False
        from_user = message_or_callback.from_user.id
        
        if from_user == OWNER or admins_helper.get_admin_by_user_id(from_user):
            return True
        
        return False
    
class ReportGroupsFilter(filters.Filter):

    def __init__(self, topic : str | tuple):
        self._topic = topic
        self._dictionary = {
            'gift_buy_topic' : '0',
            'premium_buy_topic' : '1',
            'star_buy_topic' : '2'
        }

    async def __call__(self, client : Client, update : Message):
        if not update.chat.id:
            return False
        
        if not update.reply_to_message:
            return False
        
        settings = settings_helper.get_settings()
        if not settings.topic_group:
            return False
        
        if not update.chat.id == settings.topic_group:
            return False
        
        text = update.reply_to_message.text
        pattern = r"#️⃣ کد پیگیری : (\d+)"
        buy_id = re.findall(pattern, text)
        buy_code = buy_id[0][0]

        if not buy_id:
            return
        
        if not self._dictionary.get(self._topic):
            return
        
        return self._dictionary.get(self._topic) == buy_code
    
class StepFilter(filters.Filter):

    def __init__(self, step : str | tuple):
        self.step = step

    async def __call__(self, client : Client, message_or_callback: Message | CallbackQuery):
        if not message_or_callback.from_user:
            return False
        from_user = message_or_callback.from_user.id
        if STEP.get(from_user) is None:
            STEP[from_user] = "Home"
        if isinstance(STEP[from_user], tuple):
            return self.step == STEP[from_user][0]
        
        return self.step == STEP[from_user]
    
class SupportGroupFilter(filters.Filter):

    async def __call__(self, client : Client, message_or_callback: Message | CallbackQuery):
        setting = settings_helper.get_settings()
        if not setting.support_group_id:
            return False
        return message_or_callback.chat.id == int(setting.support_group_id)