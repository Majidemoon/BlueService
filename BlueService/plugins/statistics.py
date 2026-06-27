from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from BlueService import app
from BlueService.sql_helpers import UsersHelper, ChargeWalletHelper
from BlueService.filters import OwnerFilter
from BlueService.utils import jalali_time
from datetime import datetime
import os

users_helper = UsersHelper()
charge_wallet_helper = ChargeWalletHelper()

@app.on_callback_query(filters.regex(r"^statistics$") & OwnerFilter())
async def statistics(client: Client, callback_query: CallbackQuery):

    users_count = users_helper.user_count()
    users_total_balance = users_helper.users_total_balance()
    users_total_charge = charge_wallet_helper.get_users_total_charge_amount(type='All')
    users_total_charge_payment_gate = charge_wallet_helper.get_users_total_charge_amount(type='payment_gate')
    users_total_charge_card = charge_wallet_helper.get_users_total_charge_amount(type='card')

    text = f"""👤 تعداد کاربران ربات : {users_count}
💰 موجودی کل کاربران : {users_total_balance:,}
───────────────────────
مجموع پرداخت ها : {users_total_charge}

💳 کارت به کارت : {users_total_charge_card}
💳 درگاه پرداخت : {users_total_charge_payment_gate}
───────────────────────


📅 تاریخ : {jalali_time(datetime.now()).strftime("%Y-%m-%d - %H:%M:%S")}"""
    
    markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("👥 لیست کاربران", callback_data="users_total_list")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")]
        ]
    )

    await callback_query.edit_message_text(text=text, reply_markup=markup)

    return

@app.on_callback_query(filters.regex(r"^users_total_list$") & OwnerFilter())
async def users_total_list(client : Client, callback_query : CallbackQuery):
    await callback_query.edit_message_text("در حال آماده سازی فایل کاربران ...",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🔙 بازگشت", callback_data="statistics")]
            ]
        ))
    offset = 0
    limit = 100

    if os.path.exists("users.txt"):
        os.remove("users.txt")

    with open("users.txt", "a") as f:
        f.write("ID => Balance\n")
        
    while True:
        users = users_helper.get_all_users(offset=offset, limit=limit)
        if not users:
            break


        for user in users:
            txt = f"{user.user_id} => {user.balance}\n"
            with open("users.txt", "a") as f:
                f.write(txt)

        offset += limit

    await callback_query.message.reply_document("users.txt", caption="👥 لیست کل کاربران")
    os.remove("users.txt")
    return