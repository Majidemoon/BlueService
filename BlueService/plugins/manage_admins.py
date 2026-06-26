from BlueService import app, STEP
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from BlueService.filters import StepFilter, OwnerFilter
from BlueService.sql_helpers import UsersHelper, AdminsHelper

users_helper = UsersHelper()
admins_helper = AdminsHelper()

def manage_admins_markup():
    admins_list = admins_helper.get_admins()

    admin_markup = [
        [InlineKeyboardButton("افزودن ادمین", callback_data="add_admin")]
    ]
    for admin in admins_list:
        admin_markup.append([InlineKeyboardButton(admin.user_id, callback_data=f"admin_{admin.id}")])

    admin_markup.append([InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")])

    return InlineKeyboardMarkup(admin_markup)
    

@app.on_callback_query(filters.regex("^manage_admins$") & OwnerFilter())
async def admins_panel(client: Client, callback_query: CallbackQuery):

    admin_markup = manage_admins_markup()
    await callback_query.edit_message_text("لیست ادمین ها", reply_markup=admin_markup)

    return

@app.on_callback_query(filters.regex("^add_admin$") & OwnerFilter())
async def add_admin(client: Client, callback_query: CallbackQuery):
    await callback_query.message.reply_text("ایدی کاربر را وارد کنید")
    STEP[callback_query.from_user.id] = "AddAdmin"
    return

@app.on_message(StepFilter("AddAdmin") & OwnerFilter() & filters.private & filters.text)
async def add_admin(client: Client, message: Message):
    user_id = message.text
    admins_helper.insert_admin(user_id)
    await message.reply_text("ادمین با موفقیت اضافه شد", reply_markup=manage_admins_markup())
    STEP[message.from_user.id] = "Home"
    return

@app.on_callback_query(filters.regex(r"^admin_(\d+)$") & OwnerFilter())
async def remove_admin(client: Client, callback_query: CallbackQuery):
    admin_id = int(callback_query.data.split("_")[1])
    admin = admins_helper.get_admin(admin_id)

    txt = f"""
ایدی کاربر : {admin.user_id}
ایدی ادمین : {admin.id}"""
    
    markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("حذف ادمین", callback_data=f"remove_admin_{admin.id}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="manage_admins")]
        ]
    )
    
    await callback_query.edit_message_text(txt, reply_markup=markup)

    return

@app.on_callback_query(filters.regex(r"^remove_admin_(\d+)$") & OwnerFilter())
async def remove_admin(client: Client, callback_query: CallbackQuery):
    admin_id = int(callback_query.data.split("_")[2])
    admins_helper.delete_admin(admin_id)
    await callback_query.edit_message_text("ادمین با موفقیت حذف شد", reply_markup=manage_admins_markup())
    return