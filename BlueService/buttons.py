from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle
from BlueService.sql_helpers import AdminsHelper, ForcedJoinChannelsHelper
from BlueService.config import OWNER
from BlueService import settings_helper

admins_helper = AdminsHelper()
forced_join_channels_helper = ForcedJoinChannelsHelper()

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


def admin_markup():

    settings = settings_helper.get_settings()

    buttons = [
            [
                InlineKeyboardButton("📈 آمار ربات", callback_data="statistics"),
                InlineKeyboardButton("👤 مدیریت کاربر", callback_data="manage_users")
            ],
            [
                InlineKeyboardButton("⚙️ تنظیمات ربات", callback_data="settings"),
                InlineKeyboardButton("🧾 تنظیمات پلن ها", callback_data="main_plans_settings")
            ],
            [
                InlineKeyboardButton("🚀 پیام همگانی", callback_data="broadcast"),
                InlineKeyboardButton("📋 جوین اجباری", callback_data="forced_join")
            ],
            [
                InlineKeyboardButton("ادمین", callback_data="manage_admins")
            ],
            [
                InlineKeyboardButton("وضعیت ربات 🤖", callback_data="bot_status"),
                InlineKeyboardButton("🟢" if settings.bot_status == 1 else "🔴", callback_data="bot_status")
            ],
            [
                InlineKeyboardButton("🔄 ریستارت", callback_data="restart_bot")
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_menu")
            ]
        ]

    markup = InlineKeyboardMarkup(
        buttons
    )

    return markup

def admin_forced_join_edit_markup():
    markup = [
        [InlineKeyboardButton("➕ افزودن کانال", callback_data="add_forced_join_channel")],
    ]

    channels = forced_join_channels_helper.get_forced_join_channels()

    for channel in channels:
        markup.append([InlineKeyboardButton(f"{channel.channel_name}", callback_data=f"forced_join_channel_{channel.id}")])

    markup.append([InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")])

    return InlineKeyboardMarkup(markup)