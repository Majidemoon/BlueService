from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyParameters
from pyrogram.enums import ButtonStyle
from BlueService import app, STEP, key
from BlueService.filters import StepFilter, OwnerFilter
from BlueService.sql_helpers import UsersHelper
from BlueService.utils import jalali_time
from BlueService.buttons import manage_users_markup
import traceback

users_helper = UsersHelper()

back_button = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")]])

@app.on_callback_query(filters.regex(r"^manage_users$") & OwnerFilter())
async def manage_users(client: Client, callback_query: CallbackQuery):

    await callback_query.edit_message_text("آیدی عدد یا یوزرنیم کاربر را وارد کنید", reply_markup=back_button)
    STEP[callback_query.from_user.id] = "ManageUsers"
    return

@app.on_callback_query(filters.regex(r"^information_user_(\d+)$") & OwnerFilter())
async def information_user(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.data.split("_")[2])

    try:
        user = await client.get_users(int(user_id))
    except:
        print(traceback.format_exc())
        user = None
        
    
    if not user:
        name = 'یافت نشد❌'
        username = None
    
    name = user.first_name + (" " + user.last_name if user.last_name else '')
    username = user.username
    user_id = user.id
    
    user = users_helper.get_user(user_id)
    if not user:
        await callback_query.answer("کاربر مورد نظر یافت نشد", show_alert=True)
        return
    
    STEP[callback_query.from_user.id] = "Home"
    
    text = f"""👤 اطلاعات کاربر :

🔹 نام : {name}
🔸 آیدی عددی : {user_id}
🔹 یوزرنیم :  {'@' + username if username else 'ندارد'}

⏳ تاریخ عضویت : {jalali_time(user.join_date).strftime("%Y-%m-%d")}

💰 موجودی : {user.balance}

💎 وضعیت احراز : {'✅' if user.is_verified == 1 else '❌'}"""
    
    await callback_query.edit_message_text(text, reply_markup=manage_users_markup(user_id, user.status))
    return

@app.on_message(filters.text & StepFilter("ManageUsers") & OwnerFilter() & filters.private)
async def manage_users(client: Client, message: Message):
    user_id = message.text
    if user_id.isdigit():
        user_id = int(user_id)

    try:
        user = await client.get_users(user_id)
    except:
        print(traceback.format_exc())
        user = None
    
    if not user:
        name = 'یافت نشد❌'
        username = None
    
    STEP[message.from_user.id] = ("Home")
    
    name = user.first_name + (" " + user.last_name if user.last_name else '')
    username = user.username
    user_id = user.id
    
    user = users_helper.get_user(user_id)
    if not user:
        await message.reply_text("کاربر مورد نظر یافت نشد", reply_markup=back_button)
        return
    
    text = f"""👤 اطلاعات کاربر :

🔹 نام : {name}
🔸 آیدی عددی : {user_id}
🔹 یوزرنیم :  {'@' + username if username else 'ندارد'}

⏳ تاریخ عضویت : {jalali_time(user.join_date).strftime("%Y-%m-%d")}

💰 موجودی : {user.balance}

💎 وضعیت احراز : {'✅' if user.is_verified == 1 else '❌'}
"""
    
    await message.reply_text(text, reply_markup=manage_users_markup(user_id, user.status))

    return

@app.on_callback_query(filters.regex(r"^user_add_balance_(\d+)$") & OwnerFilter())
async def user_add_balance(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.data.split("_")[3])

    await callback_query.message.reply_text("مقداری موجودی که میخواهید اضافه کنید را وارد کنید", reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("لغو", callback_data=f"information_user_{user_id}")]
        ]
    ))
    
    STEP[callback_query.from_user.id] = ("AddBalanceToUser", user_id)
    return

@app.on_message(StepFilter("AddBalanceToUser") & OwnerFilter() & filters.private & filters.text)
async def add_balance_to_user(client: Client, message: Message):
    user_id = STEP[message.from_user.id][1]
    
    amount = message.text

    if not amount.isdigit():
        await message.reply_text("لطفا مقداری موجودی که میخواهید اضافه کنید را وارد کنید")
        return

    user = users_helper.get_user(user_id)
    if not user:
        await message.reply_text("کاربر مورد نظر یافت نشد")
        return

    amount = int(amount)
    users_helper.update_balance(user_id, user.balance + amount)

    await message.reply_text(f"موجودی کاربر {amount} تومان اضافه شد ✅", reply_markup=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔙 بازگشت", callback_data=f"information_user_{user_id}")]
        ]
    ))

    try:
        await client.send_message(user_id, f"![💰](tg://emoji?id=5348418461838098123) مقدار {amount} تومان به موجودی شما توسط مدیریت افزوده شد")
    except:
        pass

    STEP[message.from_user.id] = "Home"
    return

@app.on_callback_query(filters.regex(r"^user_reduce_balance_(\d+)$") & OwnerFilter())
async def user_reduce_balance(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.data.split("_")[3])

    await callback_query.message.reply_text("مقداری موجودی که میخواهید کاهش دهید را وارد کنید", reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("لغو", callback_data=f"information_user_{user_id}")]
        ]
    ))
    
    STEP[callback_query.from_user.id] = ("ReduceBalanceToUser", user_id)
    return

@app.on_message(StepFilter("ReduceBalanceToUser") & OwnerFilter() & filters.private & filters.text)
async def reduce_balance_to_user(client: Client, message: Message):
    user_id = STEP[message.from_user.id][1]
    
    amount = message.text
    if not amount.isdigit():
        await message.reply_text("لطفا مقداری موجودی که میخواهید اضافه کنید را وارد کنید")
        return

    user = users_helper.get_user(user_id)
    if not user:
        await message.reply_text("کاربر مورد نظر یافت نشد")
        return

    amount = int(amount)
    users_helper.update_balance(user_id, user.balance - amount)

    await message.reply_text(f"موجودی کاربر {amount} تومان کاهش یافت ✅", reply_markup=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔙 بازگشت", callback_data=f"information_user_{user_id}")]
        ]
    ))

    try:
        await client.send_message(user_id, f"![💰](tg://emoji?id=5348418461838098123) مقدار {amount} تومان از موجودی شما توسط مدیریت کسر شد")
    except:
        pass

    STEP[message.from_user.id] = "Home"
    return

@app.on_callback_query(filters.regex(r"^user_send_message_(\d+)$") & OwnerFilter())
async def user_send_message(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.data.split("_")[3])

    await callback_query.message.reply_text("پیام خود را وارد کنید", reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("لغو", callback_data=f"information_user_{user_id}")]
        ]
    ))
    
    STEP[callback_query.from_user.id] = ("SendMessageToUser", user_id)
    return

@app.on_message(StepFilter("SendMessageToUser") & OwnerFilter() & filters.private & filters.text)
async def send_message_to_user(client: Client, message: Message):
    user_id = STEP[message.from_user.id][1]

    m = await message.forward(user_id, hide_sender_name=True)
    await m.reply_text("![🗣](tg://emoji?id=5988053067759625249) پیام جدید از طرف پشتیبانی", reply_parameters=ReplyParameters(quote=True), reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("پاسخ", callback_data=f"support_online", style=ButtonStyle.PRIMARY, icon_custom_emoji_id="5348242067531251702")]
        ]
    ))

    await message.reply_text("پیام شما ارسال شد ✅")
    STEP[message.from_user.id] = "Home"
    return
    
@app.on_callback_query(filters.regex(r'^block_user_(\d+)$') & OwnerFilter())
async def block_unblock_user(client : Client, callback_query : CallbackQuery):

    user_id = int(callback_query.data.split("_")[2])

    user = users_helper.get_user(user_id)

    user_status = user.status if user.status is not None else 0

    user_new_status = -1 if user_status == 0 else 0

    if user_new_status == 0:
        await callback_query.answer("کاربر مورد نظر آزاد شد")
        try:
            await callback_query.edit_message_reply_markup(manage_users_markup(user_id, user_new_status))
        except:
            pass
        try:
            await client.send_message(user_id, '![🌿](tg://emoji?id=5350464257840399147) شما آزاد شدید')
        except:
            pass
        
    if user_new_status == -1:
        await callback_query.answer("کاربر مورد نظر بلاک شد")
        try:
            await callback_query.edit_message_reply_markup(manage_users_markup(user_id, user_new_status))
        except:
            pass
        try:
            await client.send_message(user_id, '![‼️](tg://emoji?id=5350626912546865231) شما مسدود شدید')
        except:
            pass

    users_helper.update_user_status(user_id, user_new_status)