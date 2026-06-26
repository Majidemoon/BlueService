from functools import wraps
from BlueService.sql_helpers import ForcedJoinUsersHelper, ForcedJoinChannelsHelper, UsersHelper, AdminsHelper
from BlueService import anti_spam_list, STEP, settings_helper
from BlueService.logger import logger
from BlueService.config import OWNER
from pyrogram import Client
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyParameters
from pyrogram.errors import UserNotParticipant
from pyrogram.enums import ButtonStyle
from datetime import datetime

forced_join_users_helper = ForcedJoinUsersHelper()
forced_join_channels_helper = ForcedJoinChannelsHelper()
users_helper = UsersHelper()
admins_helper = AdminsHelper()

def forced_join(func):
    @wraps(func)
    async def wrapper(app : Client, message: Message | CallbackQuery):
        user_id = message.from_user.id

        setting = settings_helper.get_settings()

        bot_status = setting.bot_status

        # bot on/off
        if bot_status == 0:
            admins = admins_helper.get_admins()
            admins_list = [admin.user_id for admin in admins] + [OWNER]
            if user_id not in admins_list:
                await app.send_message(user_id, "ربات خاموش است ![📴](tg://emoji?id=5987632324173370690)")
                return

        # forced join part
        forced_join_channels = forced_join_channels_helper.get_forced_join_channels()
        markup = []

        for channel in forced_join_channels:
            forced_users = forced_join_users_helper.get_forced_join_user(user_id, channel.channel_id)
            if forced_users:
                continue
            try:
                member = await app.get_chat_member(channel.channel_id, user_id)
                forced_join_users_helper.insert_forced_join_user(user_id, channel.channel_id)
            except UserNotParticipant:
                markup.append(
                    [
                        InlineKeyboardButton(
                            text = f"{channel.channel_name}",
                            url = f"{channel.channel_link}",
                            style=ButtonStyle.PRIMARY,
                            icon_custom_emoji_id="5350831267090809192"
                        )
                    ]
                )
            except Exception as e:
                await app.send_message(OWNER, f"⚠️ مشکلی در جوین اجباری چنل {channel.channel_name} رخ داد")
                await app.send_message(message.from_user.id, "⚠️ مشکلی رخ داده است دقایقی بعد دوباره تلاش کنید")
                logger.error(f"Error getting chat member: {e}")
                return

        if markup:
            markup.append([InlineKeyboardButton("عضو شدم", callback_data="user_click_join", style=ButtonStyle.SUCCESS, icon_custom_emoji_id="5988053965407786316")])
            await app.send_message(message.from_user.id, "📣 هنوز در برخی از کانال ها عضو نشده اید", reply_markup=InlineKeyboardMarkup(markup))
        else:
            await func(app, message)       
        return
    return wrapper

def anti_spam(func):
    @wraps(func)
    async def wrapper(app : Client, message: Message | CallbackQuery):
        '''
        Anti Spam
        Get user language
        '''
        user_id = message.from_user.id
        if user_id in anti_spam_list:
            return
        
        anti_spam_list[user_id] = datetime.now()

        user = users_helper.get_user(user_id)

        if user and user.status == -1:
            if isinstance(message, Message):
                await message.reply_text('متاسفانه شما بلاک شدید', reply_parameters=ReplyParameters(quote=True))
                return
            if isinstance(message, CallbackQuery):
                await message.answer('متاسفانه شما بلاک شدید', show_alert=True)
                return

        await func(app, message)
        return
    return wrapper