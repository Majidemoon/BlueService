from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle
from BlueService.sql_helpers import AdminsHelper
from BlueService.config import OWNER

admins_helper = AdminsHelper()

def start_markup(user_id : int) -> InlineKeyboardMarkup:
    markup = [
        [InlineKeyboardButton('استارز - پرمیوم', style=ButtonStyle.SUCCESS, callback_data="stars_and_premium")],
        [
            InlineKeyboardButton('بوست', style=ButtonStyle.SUCCESS, callback_data="boost"),
            InlineKeyboardButton('گیفت', style=ButtonStyle.SUCCESS, callback_data="gift")
        ],
        [
            InlineKeyboardButton('ممبر تلگرام', style=ButtonStyle.SUCCESS, callback_data="member"),
            InlineKeyboardButton('ویو، ری‌اکشن', style=ButtonStyle.SUCCESS, callback_data="view_reaction")
        ],
        [
            InlineKeyboardButton('کیف پول', style=ButtonStyle.PRIMARY, callback_data="user_wallet"),
            InlineKeyboardButton('اطلاعات حساب', style=ButtonStyle.PRIMARY, callback_data="user_panel")
        ],
        [
            InlineKeyboardButton('پشتیبانی', style=ButtonStyle.PRIMARY, callback_data="support"),
            InlineKeyboardButton('سفارشات من', style=ButtonStyle.PRIMARY, callback_data="my_orders")
        ]
    ]

    if user_id == OWNER or admins_helper.get_admin_by_user_id(user_id):
        markup.append(
            [
                InlineKeyboardButton('پنل ادمین', style=ButtonStyle.DEFAULT, callback_data="admin_panel"),
            ]
        )
    

    return InlineKeyboardMarkup(markup)