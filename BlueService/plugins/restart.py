from BlueService import app
from BlueService.filters import OwnerFilter
from pyrogram import filters, Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
import sys
import os

@app.on_callback_query(filters.regex(r"^restart_bot$") & OwnerFilter())
async def restart(client : Client, callback_query : CallbackQuery):

    await callback_query.edit_message_text("ربات ریستارت شود؟", reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅", callback_data="confirm_restart"),
                InlineKeyboardButton('❌', callback_data="admin_panel")
            ]
        ]
    ))

    return

@app.on_message(filters.command("restart") & filters.text & filters.private & OwnerFilter())
async def restart_command(client : Client, message : Message):
    await message.reply_text("ربات ریستارت شود؟", reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅", callback_data="confirm_restart"),
                InlineKeyboardButton('❌', callback_data="admin_panel")
            ]
        ]
    ))

    return

@app.on_callback_query(filters.regex(r"^confirm_restart$") & OwnerFilter())
async def confirm_restart(client : Client, callback_query : CallbackQuery):

    await callback_query.answer("Restarting ...")
    python = sys.executable
    os.execl(python, python, "-m", "BlueService")
