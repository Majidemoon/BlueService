from pyrogram import filters, Client
from pyrogram.types import Message, CallbackQuery, ReplyParameters
from BlueService import app, STEP
from BlueService.filters import OwnerFilter
from BlueService.buttons import admin_markup

@app.on_message(filters.command("panel") & OwnerFilter())
async def panel(client: Client, message: Message):
    STEP[message.from_user.id] = "Home"
    await message.reply_text("Admin Panel", reply_markup=admin_markup(), reply_parameters=ReplyParameters(quote=True))
    return

@app.on_callback_query(filters.regex(r"^admin_panel$") & OwnerFilter())
async def admin_panel(client: Client, callback_query: CallbackQuery):
    STEP[callback_query.from_user.id] = "Home"
    await callback_query.edit_message_text("Admin Panel", reply_markup=admin_markup())
    return