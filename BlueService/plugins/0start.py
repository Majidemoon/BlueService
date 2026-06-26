from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, ReplyParameters, ReplyKeyboardMarkup, KeyboardButton
from pyrogram.enums import ButtonStyle
from BlueService.decorators import anti_spam
from BlueService.sql_helpers import UsersHelper
from BlueService.buttons import start_markup
from BlueService.filters import StepFilter
from BlueService import settings_helper, STEP, app

users_helper = UsersHelper()

@app.on_message(filters.command("start") & filters.private)
@anti_spam
async def start(client: Client, message: Message):
    from_user = message.chat.id
    setting = settings_helper.get_settings()

    if not setting:
        settings_helper.create_settings()
        is_welcome_mssage_exists = False
    else:
        is_welcome_mssage_exists = bool(setting.wellcome_message)

    STEP[from_user] = "Home"

    user = users_helper.get_user(from_user)
    if not user:
        users_helper.insert_user(from_user)

    user = users_helper.get_user(from_user)
    
    if not is_welcome_mssage_exists:
        await message.reply_text("![✨](tg://emoji?id=5222108309795908493) سلام دوست عزیز به ربات ما خوش آمدی", reply_markup=start_markup(from_user), reply_parameters=ReplyParameters(quote=True))
    else:
        await message.reply_text(setting.wellcome_message, reply_markup=start_markup(from_user), reply_parameters=ReplyParameters(quote=True))

    await message.reply_text("✅ منوی پایین فعال شد.", reply_markup=ReplyKeyboardMarkup(
        [
            [KeyboardButton("منو", icon_custom_emoji_id=5222108309795908493)]
        ],
        resize_keyboard=True,
    ))

    return



@app.on_message(filters.regex("^🔙") & filters.private & StepFilter("Home"))
@anti_spam
async def back_to_menu(client: Client, message: Message):
    STEP[message.from_user.id] = "Home"
    await message.reply_text("![✨](tg://emoji?id=5222108309795908493) منو اصلی", reply_markup=start_markup(message.from_user.id), reply_parameters=ReplyParameters(quote=True))
    return

@app.on_message(filters.regex("^منو$") & filters.text & filters.private)
async def menu(client : Client, message : Message):
    STEP[message.from_user.id] = "Home"
    await message.reply_text("![✨](tg://emoji?id=5222108309795908493) منو اصلی", reply_markup=start_markup(message.from_user.id), reply_parameters=ReplyParameters(quote=True))
    return

@app.on_callback_query(filters.regex("^back_to_menu$"))
async def back_to_menu(client : Client, callback_query : CallbackQuery):
    STEP[callback_query.from_user.id] = "Home"
    try:
        await callback_query.edit_message_text("![✨](tg://emoji?id=5222108309795908493) منو اصلی", reply_markup=start_markup(callback_query.from_user.id))
    except:
        pass
    return