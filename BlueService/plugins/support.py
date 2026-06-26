from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from pyrogram.errors import PeerIdInvalid
from pyrogram.enums import ButtonStyle
from BlueService import app, STEP, settings_helper as setting_helper
from BlueService.config import OWNER
from BlueService.filters import StepFilter, OwnerFilter, SupportGroupFilter
from BlueService.decorators import forced_join, anti_spam
from BlueService.sql_helpers import UsersHelper, TicketRepliesHelper, TicketsHelper
from datetime import datetime, timedelta
from BlueService.buttons import start_markup
from BlueService.utils import time_formatter

users_helper = UsersHelper()
ticket_replies_helper = TicketRepliesHelper()
tickets_helper = TicketsHelper()

def support_markup():
    back_button = InlineKeyboardButton("بازگشت", callback_data="back_to_menu", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5352759161945867747")

    setting = setting_helper.get_settings()
    support_group_id = setting.support_group_id
    support_account_username = setting.support_username

    if not support_group_id and not support_account_username:
        return InlineKeyboardMarkup([[back_button]])
    if support_account_username and not support_group_id:
        return InlineKeyboardMarkup([[back_button]])
    
    button = [
        [
            InlineKeyboardButton("چت آنلاین", callback_data="support_online", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5348242067531251702")
        ],
        [
            back_button
        ]
    ]

    return InlineKeyboardMarkup(button)

def support_text(welcome=True):
    support_text = '![💖](tg://emoji?id=5987929875212671466) به بخش پشتیبانی خوش آمدید\n\n' if welcome else ''
    setting = setting_helper.get_settings()
    support_group_id = setting.support_group_id
    support_account_username = setting.support_username

    if not support_group_id and not support_account_username:
        return '![❌](tg://emoji?id=5990179501772903662) گروه پشتیبانی و حساب کاربری پشتیبانی وجود ندارد'
    
    if support_account_username and not support_group_id:
        return support_text + f"""جهت دریافت پشتیبانی میتوانید با آیدی زیر در ارتباط باشید

![💖](tg://emoji?id=5987929875212671466) حساب کاربری پشتیبانی: {support_account_username}"""
    
    if support_group_id and not support_account_username:
        return support_text + "![💖](tg://emoji?id=5987929875212671466) برای دریافت پشتیبانی لطفا از دکمه چت آنلاین استفاده کنید"
    
    return support_text + f"""جهت دریافت پشتیبانی میتوانید با آیدی زیر در ارتباط باشید یا از دکمه چت آنلاین استفاده کنید

![💖](tg://emoji?id=5987929875212671466) حساب کاربری پشتیبانی: {support_account_username}"""

@app.on_callback_query(filters.regex(r'^support$'))
@anti_spam
@forced_join
async def support(client: Client, callback_query: CallbackQuery):
    STEP[callback_query.from_user.id] = "Home"
    
    await callback_query.edit_message_text(support_text(), reply_markup=support_markup())
    return


@app.on_callback_query(filters.regex(r'^support_online$') & StepFilter('Home'))
@anti_spam
@forced_join
async def support_online(client: Client, callback_query: CallbackQuery):
    user_last_ticket = tickets_helper.get_user_last_ticket(callback_query.from_user.id)
    if user_last_ticket:
        time_diff = datetime.now() - user_last_ticket.datetime
        if time_diff < timedelta(minutes=5):
            time_to_wait_text = time_formatter(td=(timedelta(minutes=5) - time_diff))
            await callback_query.edit_message_text(f"![❌](tg://emoji?id=5990179501772903662) شما قبلا پیامی ارسال کرده اید\n\nبرای ارسال پیام جدید {time_to_wait_text} منتظر بمانید\n\n{support_text(welcome=False)}", reply_markup=support_markup())
            return
        
    await callback_query.edit_message_text("![🕶](tg://emoji?id=5989895286607058025) پیام خود را جهت ارتباط با پشتیبانی در قالب یک پیام کنید", reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("خروج از پشتیبانی", callback_data="support", style=ButtonStyle.DANGER, icon_custom_emoji_id="5348514879558926674")
            ]
        ]
    ))

    STEP[callback_query.from_user.id] = 'Support'

    return

@app.on_message(filters.private & StepFilter('Support'))
@anti_spam
async def support_message(client: Client, message: Message):
    setting = setting_helper.get_settings()
    support_group_id = setting.support_group_id
    if not support_group_id:
        await message.reply_text("![❌](tg://emoji?id=5990179501772903662) چت با پشتیبانی در دسترس نیست\n\n" + support_text(welcome=False), reply_markup=support_markup())
        STEP[message.from_user.id] = 'Home'
        return
    
    user_last_ticket = tickets_helper.get_user_last_ticket(message.from_user.id)
    if user_last_ticket:
        time_diff = datetime.now() - user_last_ticket.datetime
        if time_diff < timedelta(minutes=5):
            time_to_wait_text = time_formatter(td=(timedelta(minutes=5) - time_diff))
            await message.reply_text(f"![❌](tg://emoji?id=5990179501772903662) شما قبلا پیامی ارسال کرده اید\n\nبرای ارسال پیام جدید {time_to_wait_text} منتظر بمانید\n\n" + support_text(welcome=False), reply_markup=support_markup())
            STEP[message.from_user.id] = 'Home'
            return
    
    await message.reply_text("![✅](tg://emoji?id=5990177534677881598) پیام شما به پشتیبانی ارسال شد\n\n" + support_text(welcome=False), reply_markup=support_markup())
    STEP[message.from_user.id] = 'Home'
    ticket_text = message.text if message.text else message.caption if message.caption else 'رسانه بدون کپشن' if message.media else 'بدون متن'
    user_ticket = tickets_helper.insert_ticket(message.from_user.id, ticket_text)
    try:
        msg = await message.forward(int(support_group_id))
    except PeerIdInvalid:
        await message.reply_text("![❌](tg://emoji?id=5990179501772903662) چت با پشتیبانی در دسترس نیست", reply_markup=start_markup(message.from_user.id))
        STEP[message.from_user.id] = 'Home'
        await client.send_message(OWNER, "⚠️ گروه پشتیبانی شناخته نمیشود یه پیام دلخواه به گروه پشتیبانی ارسال کنید")
        return
    await msg.reply_text(f"""پیام جدید

نام: [{message.from_user.first_name} {message.from_user.last_name if message.from_user.last_name else ''}](tg://user?id={message.from_user.id})
ایدی عددی: {message.from_user.id}
نام کاربری: {'@' + message.from_user.username if message.from_user.username else 'ندارد'}
""",
reply_markup=InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("پاسخ", callback_data=f"answer_{user_ticket.id}", style=ButtonStyle.SUCCESS, icon_custom_emoji_id="5348429250795945732")
        ]
    ]
))
    return

@app.on_callback_query(filters.regex(r'^answer_(\d+)$') & OwnerFilter())
async def answer(client: Client, callback_query: CallbackQuery):
    ticket_id = int(callback_query.data.split("_")[1])
    await callback_query.message.reply_text("پیام خود را ارسال کنید", reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("لغو پاسخ", callback_data=f"cancel_answer", style=ButtonStyle.DANGER, icon_custom_emoji_id="5348514879558926674")
            ]
        ]
    ))
    STEP[callback_query.from_user.id] = ('SupportAnswer', ticket_id)
    return

@app.on_callback_query(filters.regex(r'^cancel_answer$') & StepFilter('SupportAnswer') & OwnerFilter())
async def cancel_answer(client: Client, callback_query: CallbackQuery):
    STEP[callback_query.from_user.id] = 'Home'
    await callback_query.edit_message_text("پاسخ لغو شد", reply_markup=None)
    return

@app.on_message(filters.group & OwnerFilter() & SupportGroupFilter() & StepFilter('SupportAnswer'))
async def answer_message(client: Client, message: Message):
    ticket_id = STEP[message.from_user.id][1]
    user_ticket = tickets_helper.get_ticket(ticket_id)
    target_user_id = user_ticket.user_id
    msg = await message.forward(target_user_id, hide_sender_name=True)
    await msg.reply_text("پیام جدید از پشتیبانی![⬆️](tg://emoji?id=5974053716347589290)", reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("پاسخ", callback_data=f"support_online", style=ButtonStyle.SUCCESS, icon_custom_emoji_id="5348429250795945732")
            ]
    ]))
    await message.reply_text("پیام شما به کاربر ارسال شد")
    ticket_replies_helper.insert_ticket_reply(ticket_id, message.text if message.text else message.caption if message.caption else 'رسانه بدون کپشن' if message.media else 'بدون متن', message.from_user.id)
    STEP[message.from_user.id] = 'Home'
    return