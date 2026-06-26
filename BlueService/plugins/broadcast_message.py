from BlueService import app, STEP, logger
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from pyrogram.errors import FloodWait, PeerIdInvalid
from BlueService.sql_helpers import UsersHelper
from BlueService.filters import StepFilter, OwnerFilter
from BlueService.utils import progress_bar
import asyncio
import random
import traceback

users_helper = UsersHelper()
sending_message = False

@app.on_callback_query(filters.regex(r'^broadcast$') & OwnerFilter())
async def broadcast_message(client: Client, callback_query: CallbackQuery):
    if sending_message:
        await callback_query.answer("در حال ارسال پیام همگانی", show_alert=True)
        return

    await callback_query.edit_message_text(
        "نوع ارسال همگانی را انتخاب کنید",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ارسال همگانی", callback_data="sendall_message"),
                    InlineKeyboardButton("فروارد همگانی", callback_data="forwardall_message"),
                ],
                [
                    InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")
                ]
            ]
        )
    )
    return


@app.on_callback_query(OwnerFilter() & filters.regex(r'^sendall_message$'))
async def broadcast_message2(client: Client, callback_query: CallbackQuery):
    from_user = callback_query.from_user.id
    STEP[from_user] = 'SendAllMessage'


    await callback_query.edit_message_text(
        "لطفا پیام را وارد کنید",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")
                ]
            ]
        )
    )

    return

@app.on_callback_query(filters.regex(r'^forwardall_message$'))
async def broadcast_message3(client: Client, callback_query: CallbackQuery):
    from_user = callback_query.from_user.id
    STEP[from_user] = 'ForwardAllMessage' 


    await callback_query.edit_message_text(
        "لطفا پیام را وارد کنید",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")
                ]
            ]
        )
    )

async def generate_text(users_count, success_count, unsuccess_count):
    return f"""در حال ارسال پیام همگانی
تعداد کل کاربران: {users_count}
ارسال موفق: {success_count}
ارسال ناموفق: {unsuccess_count}
{progress_bar(success_count + unsuccess_count, users_count)}"""

@app.on_message((StepFilter('SendAllMessage') | StepFilter('ForwardAllMessage')) & OwnerFilter() & filters.private)
async def broadcast_message4(client: Client, message: Message):

    asyncio.create_task(send_broadcast_message(client, message))


async def send_broadcast_message(client: Client, message: Message):
    from_user = message.from_user.id
    global sending_message

    offset = 0
    limit = 100
    if STEP[from_user] == 'SendAllMessage':
        hide_sender_name = True
    else:
        hide_sender_name = False

    STEP[from_user] = 'AdminPanel'

    users_count = users_helper.user_count()
    success_count = 0
    unsuccess_count = 0

    await message.reply_text("در حال ارسال پیام همگانی")
    msg = await message.reply_text(await generate_text(users_count, success_count, unsuccess_count))

    sending_message = True

    while True:
        all_users = users_helper.get_all_users(offset, limit)
        if not all_users:
            break

        for user in all_users:
            try:
                await message.forward(user.user_id, hide_sender_name=hide_sender_name)
                success_count += 1
                await msg.edit_text(await generate_text(users_count, success_count, unsuccess_count))
                await asyncio.sleep(0.2)
            except FloodWait as e:
                await asyncio.sleep(300)
                unsuccess_count += 1
                continue
            except PeerIdInvalid:
                unsuccess_count += 1
                try:
                    await msg.edit_text(await generate_text(users_count, success_count, unsuccess_count))
                except:
                    logger.error(traceback.format_exc())
                await asyncio.sleep(0.2)
                continue
            except Exception as e:
                logger.exception(f"❌ Error while sending message to user {user.user_id}: {e}")
                unsuccess_count += 1
                try:
                    await msg.edit_text(await generate_text(users_count, success_count, unsuccess_count))
                except:
                    logger.error(traceback.format_exc())
                await asyncio.sleep(0.2)
                continue
        offset += limit
    text = await generate_text(users_count, success_count, unsuccess_count)
    await msg.edit_text(text.replace("در حال ارسال پیام همگانی", "پیام همگانی با موفقیت ارسال شد"))
    await msg.reply_text(random.choice(["😊", "👍", "💯", "😎", "👏"]))
    sending_message = False
    return
