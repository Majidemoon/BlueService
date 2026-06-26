from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyParameters
from BlueService import app, STEP, settings_helper as setting_helper
from BlueService.config import OWNER
from BlueService.filters import StepFilter, OwnerFilter
from BlueService.sql_helpers import SettingsHelper
from BlueService.buttons import setting_markup, admin_markup
import asyncio

back_button = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="back_settings")]])

@app.on_callback_query(filters.regex(r"^back_settings$"))
async def back_settings(client: Client, callback_query: CallbackQuery):
    await callback_query.edit_message_text("تنظیمات ربات", reply_markup=setting_markup())
    STEP[callback_query.from_user.id] = "Home"
    return

@app.on_callback_query(filters.regex(r"^settings$") & OwnerFilter())
async def settings(client: Client, callback_query: CallbackQuery):
    await callback_query.edit_message_text("تنظیمات ربات", reply_markup=setting_markup())
    return

@app.on_callback_query(filters.regex("bot_status") & OwnerFilter())
async def bot_status(client: Client, callback_query: CallbackQuery):

    setting = setting_helper.get_settings()
    bot = setting.bot_status

    if bot == 1:
        setting_helper.update_settings(bot_status=0)
    else:
        setting_helper.update_settings(bot_status=1)

    try:
        await callback_query.edit_message_reply_markup(admin_markup())
    except Exception as e:
        print(e)
    return   

@app.on_callback_query(filters.regex(r"^start_text$") & OwnerFilter())
async def change_start_text(client: Client, callback_query: CallbackQuery):
    setting = setting_helper.get_settings()
    txt = f"""متن استارت فعلی : 
{setting.wellcome_message if setting.wellcome_message else "متن استارت ثبت نشده است"}"""
    
    await callback_query.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("تغییر متن استارت", callback_data="change_start_text")
            ],
            [
                InlineKeyboardButton("🗑 حذف متن استارت" if setting.wellcome_message else "☹️", callback_data="delete_start_text" if setting.wellcome_message else "Nones")
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="settings")
            ]
        ]
    ))

    return

@app.on_callback_query(filters.regex(r"^delete_start_text$") & OwnerFilter())
async def delete_start_text(client: Client, callback_query: CallbackQuery):
    setting_helper.update_settings(wellcome_message=None)
    await callback_query.edit_message_text("متن استارت با موفقیت حذف شد", reply_markup=setting_markup())
    return

@app.on_callback_query(filters.regex(r"^change_start_text$"))
async def change_start_text(client: Client, callback_query: CallbackQuery):
    await callback_query.edit_message_text("متن استارت را وارد کنید", reply_markup=back_button)
    STEP[callback_query.from_user.id] = "ChangeStartText"
    return

@app.on_message(filters.text & filters.private & StepFilter("ChangeStartText") & OwnerFilter())
async def change_start_text(client: Client, message: Message):
    setting_helper.update_settings(wellcome_message=message.text)
    await message.reply_text("متن استارت با موفقیت تغییر کرد", reply_parameters=ReplyParameters(quote=True), reply_markup=setting_markup())
    STEP[message.from_user.id] = "Home"
    return

@app.on_callback_query(filters.regex(r"^help_text$") & OwnerFilter())
async def change_help_text(client: Client, callback_query: CallbackQuery):
    setting = setting_helper.get_settings()
    txt = f"""متن راهنمایی فعلی : 
{setting.help_text if setting.help_text else "متن راهنمایی ثبت نشده است"}"""
    
    await callback_query.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("تغییر متن راهنمایی", callback_data="change_help_text")
            ],
            [
                InlineKeyboardButton("🗑 حذف متن راهنمایی" if setting.help_text else "☹️", callback_data="delete_help_text" if setting.help_text else "None")
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="settings")
            ]
        ]
    ))

    return

@app.on_callback_query(filters.regex(r"^delete_help_text$") & OwnerFilter())
async def delete_help_text(client: Client, callback_query: CallbackQuery):
    setting_helper.update_settings(help_text=None)
    await callback_query.edit_message_text("متن راهنمایی با موفقیت حذف شد", reply_markup=setting_markup())
    return

@app.on_callback_query(filters.regex(r"^change_help_text$") & OwnerFilter())
async def change_help_text(client: Client, callback_query: CallbackQuery):
    await callback_query.edit_message_text("متن راهنمایی را وارد کنید", reply_markup=back_button)
    STEP[callback_query.from_user.id] = "ChangeHelpText"
    return

@app.on_message(filters.text & filters.private & StepFilter("ChangeHelpText") & OwnerFilter())
async def change_help_text(client: Client, message: Message):
    setting_helper.update_settings(help_text=message.text)
    await message.reply_text("متن راهنمایی با موفقیت تغییر کرد", reply_parameters=ReplyParameters(quote=True), reply_markup=setting_markup())
    STEP[message.from_user.id] = "Home"
    return

@app.on_callback_query(filters.regex(r"^support_id$") & OwnerFilter())
async def change_support_id(client: Client, callback_query: CallbackQuery):
    setting = setting_helper.get_settings()
    txt = f"""آیدی پشتیبانی فعلی : 
{setting.support_username if setting.support_username else "آیدی پشتیبانی ثبت نشده است"}"""
    
    await callback_query.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("تغییر آیدی پشتیبانی", callback_data="change_support_id")
            ],
            [
                InlineKeyboardButton("🗑 حذف آیدی پشتیبانی" if setting.support_username else "☹️", callback_data="delete_support_id" if setting.support_username else "None")
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="settings")
            ]
        ]
    ))

    return

@app.on_callback_query(filters.regex(r"^delete_support_id$") & OwnerFilter())
async def delete_support_id(client: Client, callback_query: CallbackQuery):
    setting_helper.update_settings(support_username=None)
    await callback_query.edit_message_text("آیدی پشتیبانی با موفقیت حذف شد", reply_markup=setting_markup())
    return

@app.on_callback_query(filters.regex(r"^change_support_id$") & OwnerFilter())
async def change_support_id(client: Client, callback_query: CallbackQuery):
    await callback_query.edit_message_text("آیدی پشتیبانی را وارد کنید", reply_markup=back_button)
    STEP[callback_query.from_user.id] = "ChangeSupportId"
    return

@app.on_message(filters.text & filters.private & StepFilter("ChangeSupportId") & OwnerFilter())
async def change_support_id(client: Client, message: Message):
    setting_helper.update_settings(support_username=message.text)
    await message.reply_text("آیدی پشتیبانی با موفقیت تغییر کرد",reply_parameters=ReplyParameters(quote=True), reply_markup=setting_markup())
    STEP[message.from_user.id] = "Home"
    return

@app.on_callback_query(filters.regex(r"^min_increase$") & OwnerFilter())
async def change_min_increase(client: Client, callback_query: CallbackQuery):
    setting = setting_helper.get_settings()
    txt = f"""حداقل افزایش موجودی فعلی : 
{setting.min_increase if setting.min_increase else "حداقل افزایش موجودی ثبت نشده است"}"""
    
    await callback_query.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("تغییر حداقل افزایش موجودی", callback_data="change_min_increase")
            ],
            [
                InlineKeyboardButton("🗑 حذف حداقل افزایش موجودی" if setting.min_increase else "☹️", callback_data="delete_min_increase" if setting.min_increase else "None")
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="settings")
            ]
        ]
    ))

    return

@app.on_callback_query(filters.regex(r"^delete_min_increase$") & OwnerFilter())
async def delete_min_increase(client: Client, callback_query: CallbackQuery):
    settings = setting_helper.get_settings()
    if not settings.min_increase:
        await callback_query.answer("حداقل افزایش موجودی ثبت نشده.")
        return
    
    setting_helper.update_settings(min_increase=None)
    await callback_query.answer("حداقل افزایش موجودی با موفقیت حذف شد")
    settings = setting_helper.get_settings()
    txt = f"""حداقل افزایش موجودی فعلی : 
{settings.min_increase if settings.min_increase else "حداقل افزایش موجودی ثبت نشده است"}"""
    await callback_query.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("تغییر حداقل افزایش موجودی", callback_data="change_min_increase")
            ],
            [
                InlineKeyboardButton("🗑 حذف حداقل افزایش موجودی" if settings.min_increase else "☹️", callback_data="delete_min_increase" if settings.min_increase else "None")
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="settings")
            ]
        ]
    ))

@app.on_callback_query(filters.regex(r"^change_min_increase$") & OwnerFilter())
async def change_min_increase(client: Client, callback_query: CallbackQuery):
    await callback_query.edit_message_text("حداقل افزایش موجودی را وارد کنید", reply_markup=back_button)
    STEP[callback_query.from_user.id] = "ChangeMinIncrease"
    return

@app.on_message(filters.text & filters.private & StepFilter("ChangeMinIncrease") & OwnerFilter())
async def change_min_increase(client: Client, message: Message):
    text = message.text
    if not text.isdigit():
        await message.reply_text("لطفا عدد وارد کنید")
        return
    setting = setting_helper.get_settings()
    text = int(text)
    if setting.max_increase:
        if text > setting.max_increase:
            await message.reply_text("حداقل افزایش نباید بزرگتر از حداکثر باشد")
            return
    setting_helper.update_settings(min_increase=message.text)
    await message.reply_text("حداقل افزایش موجودی با موفقیت تغییر کرد",reply_parameters=ReplyParameters(quote=True), reply_markup=setting_markup())
    STEP[message.from_user.id] = "Home"
    return

@app.on_callback_query(filters.regex(r"^max_increase$") & OwnerFilter())
async def change_max_increase(client: Client, callback_query: CallbackQuery):
    setting = setting_helper.get_settings()
    txt = f"""حداکثر افزایش موجودی فعلی : 
{setting.max_increase if setting.max_increase else "حداکثر افزایش موجودی ثبت نشده است"}"""
    
    await callback_query.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("تغییر حداکثر افزایش موجودی", callback_data="change_max_increase")
            ],
            [
                InlineKeyboardButton("🗑 حذف حداکثر افزایش موجودی" if setting.max_increase else "☹️", callback_data="delete_max_increase" if setting.max_increase else "None")
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="settings")
            ]
        ]
    ))

    return

@app.on_callback_query(filters.regex(r"^delete_max_increase$") & OwnerFilter())
async def delete_max_increase(client : Client, callback_query : CallbackQuery):
    
    settings = setting_helper.get_settings()
    if not settings.max_increase:
        await callback_query.answer("حداکثر افزایش موجودی ثبت نشده.")
        return
    
    setting_helper.update_settings(max_increase=None)
    await callback_query.answer("حداکثر افزایش موجودی با موفقیت حذف شد")
    settings = setting_helper.get_settings()
    txt = f"""حداکثر افزایش موجودی فعلی : 
{settings.max_increase if settings.max_increase else "حداکثر افزایش موجودی ثبت نشده است"}"""
    await callback_query.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("تغییر حداکثر افزایش موجودی", callback_data="change_max_increase")
            ],
            [
                InlineKeyboardButton("🗑 حذف حداکثر افزایش موجودی" if settings.max_increase else "☹️", callback_data="delete_max_increase" if settings.max_increase else "None")
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="settings")
            ]
        ]
    ))


@app.on_callback_query(filters.regex(r"^change_max_increase$") & OwnerFilter())
async def change_max_increase(client: Client, callback_query: CallbackQuery):
    await callback_query.edit_message_text("حداکثر افزایش موجودی را وارد کنید", reply_markup=back_button)
    STEP[callback_query.from_user.id] = "ChangeMaxIncrease"
    return

@app.on_message(filters.text & filters.private & StepFilter("ChangeMaxIncrease") & OwnerFilter())
async def change_max_increase(client: Client, message: Message):
    text = message.text
    if not text.isdigit():
        await message.reply_text("لطفا عدد وارد کنید")
        return
    setting = setting_helper.get_settings()
    text = int(text)
    if setting.min_increase:
        if text < setting.min_increase:
            await message.reply_text("حداکثر افزایش نباید کوچکتر از حداقل باشد")
            return
    setting_helper.update_settings(max_increase=message.text)
    await message.reply_text("حداکثر افزایش موجودی با موفقیت تغییر کرد",reply_parameters=ReplyParameters(quote=True), reply_markup=setting_markup())
    STEP[message.from_user.id] = "Home"
    return

@app.on_callback_query(filters.regex(r'^support_group$') & OwnerFilter())
async def st_support_group_id(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    text = callback_query.message.text

    setting = setting_helper.get_settings()
    group_id = setting.support_group_id
    help_text = """برای تغییر گروه پشتیبانی با استفاده از دکمه زیر ربات رو تو گروه اضافه کرده و ادمین کنید سپس با دستور 
/set_support_group
گروه جدید تنظیم میشود"""

    await callback_query.edit_message_text(help_text, reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("افزودن ربات به گروه", url=f"t.me/{client.me.username}?startgroup=botstart")
            ],
            [
                InlineKeyboardButton("🗑 حذف گروه پشتیبانی" if group_id else "☹️", callback_data="delete_support_group" if group_id else "None")
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="settings")
            ]
        ]
    ))

    return

@app.on_callback_query(filters.regex(r'^delete_support_group$') & OwnerFilter())
async def delete_support_group(client: Client, callback_query: CallbackQuery):
    setting_helper.update_settings(support_group_id=None)
    await callback_query.edit_message_text("گروه پشتیبانی با موفقیت حذف شد")
    return

@app.on_message(filters.command("set_support_group") & filters.group & OwnerFilter())
async def set_support_group(client: Client, message: Message):
    setting_helper.update_settings(support_group_id=message.chat.id)
    await message.reply_text("گروه پشتیبانی با موفقیت تنظیم شد")
    return

@app.on_callback_query(filters.regex(r'^buy_report_channel$') & OwnerFilter())
async def st_buy_report_channel(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    text = callback_query.message.text

    setting = setting_helper.get_settings()
    channel_id = setting.buy_report_channel
    help_text = """برای تغییر کانال گزارش خرید با استفاده از دکمه زیر ربات رو تو کانال اضافه کرده و ادمین کنید سپس با دستور 
/set_buy_report_channel
کانال جدید تنظیم میشود"""

    await callback_query.edit_message_text(help_text, reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("افزودن ربات به کانال", url=f"t.me/{client.me.username}?startchannel=botstart")
            ],
            [
                InlineKeyboardButton("🗑 حذف کانال گزارش خرید" if channel_id else "☹️", callback_data="delete_buy_report_channel" if channel_id else "None")
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="settings")
            ]
        ]
    ))

    return

@app.on_message(filters.command("set_buy_report_channel") & filters.channel)
async def set_buy_report_channel(client: Client, message: Message):
    setting_helper.update_settings(buy_report_channel=message.chat.id)
    msg = await message.forward(OWNER)
    await msg.reply_text(f"""درخواست ثبت کانال گزارش خرید""", reply_parameters=ReplyParameters(quote=True), reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ تایید", callback_data=f"accept_buy_report_channel_{message.chat.id}"),
                InlineKeyboardButton("❌ رد", callback_data="reject_buy_report_channel")
            ]
        ]
    ))
    return

@app.on_callback_query(filters.regex(r'^reject_buy_report_channel$') & OwnerFilter())
async def reject_buy_report_channel(client: Client, callback_query: CallbackQuery):
    await callback_query.edit_message_text("❌ درخواست ثبت کانال گزارش خرید رد شد")
    return

@app.on_callback_query(filters.regex(r'^accept_buy_report_channel_-(\d+)$') & OwnerFilter()) # I add - before id because channel ids in Telegram are negative
async def accept_buy_report_channel(client: Client, callback_query: CallbackQuery):
    channel_id = int(callback_query.data.split("_")[4])
    setting_helper.update_settings(buy_report_channel=channel_id)
    await callback_query.edit_message_text("✅ درخواست ثبت کانال گزارش خرید تایید شد")
    await client.send_message(channel_id, "✅ کانال گزارش خرید تنظیم شد")
    return

@app.on_callback_query(filters.regex(r'^delete_buy_report_channel$') & OwnerFilter())
async def delete_buy_report_channel(client: Client, callback_query: CallbackQuery):
    setting_helper.update_settings(buy_report_channel=None)
    await callback_query.edit_message_text("کانال گزارش خرید با موفقیت حذف شد")
    return

@app.on_callback_query(filters.regex(r'^topic_group$') & OwnerFilter())
async def st_topic_group(client: Client, callback_query: CallbackQuery):
    setting = setting_helper.get_settings()
    group_id = setting.topic_group
    help_text = """برای تغییر گروه گزارشات با استفاده از دکمه زیر ربات رو تو کانال اضافه کرده و ادمین کنید سپس با دستور 
/set_topic_group
گروه جدید تنظیم میشود
**توجه : به ربات باید دسترسی ایجاد تاپیک داده شود**"""

    await callback_query.edit_message_text(help_text, reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("افزودن ربات به گروه", url=f"t.me/{client.me.username}?startgroup=botstart")
            ],
            [
                InlineKeyboardButton("🗑 حذف گروه گزارشات" if group_id else "☹️", callback_data="delete_topic_group" if group_id else "None")
            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="settings")
            ]
        ]
    ))

    return

@app.on_message(filters.command("set_topic_group") & filters.group & OwnerFilter())
async def set_topic_group(client: Client, message: Message):
    msg = await message.forward(OWNER)
    await msg.reply_text(f"""درخواست ثبت گروه گزارشات""", reply_parameters=ReplyParameters(quote=True), reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ تایید", callback_data=f"accept_topic_group_{message.chat.id}"),
                InlineKeyboardButton("❌ رد", callback_data="reject_topic_group")
            ]
        ]
    ))
    return

@app.on_callback_query(filters.regex(r'^reject_topic_group$') & OwnerFilter())
async def reject_topic_group(client: Client, callback_query: CallbackQuery):
    await callback_query.edit_message_text("❌ درخواست ثبت گروه گزارشات رد شد")
    return

@app.on_callback_query(filters.regex(r'^accept_topic_group_-(\d+)$') & OwnerFilter()) # I add - before id because channel ids in Telegram are negative
async def accept_topic_group(client: Client, callback_query: CallbackQuery):
    group_id = int(callback_query.data.split("_")[3])

    try:

        charge_report_topic = await client.create_forum_topic(group_id, "💰 شارژ حساب")
        await asyncio.sleep(0.5)
        backup_topic = await client.create_forum_topic(group_id, "📥 BackUp")
        
        setting_helper.update_settings(
            topic_group = group_id,
            charge_report_topic = charge_report_topic.id,
            backup_topic = backup_topic.id
        )
        await callback_query.edit_message_text("✅ درخواست ثبت گروه گزارشات تایید شد")
    except Exception as e:
        print(e)
        await callback_query.answer("ناموفق")
    return

@app.on_callback_query(filters.regex(r'^delete_topic_group$') & OwnerFilter())
async def delete_topic_group(client: Client, callback_query: CallbackQuery):
    setting_helper.update_settings(
        topic_group=None,
        transfer_report_topic = None,
        charge_report_topic = None,
        refferal_report_topic = None,
        backup_topic = None,
        star_buy_topic = None,
        premium_buy_topic = None,
        gift_buy_topic = None
    )
    await callback_query.edit_message_text("گروه گزارشات با موفقیت حذف شد")
    return
