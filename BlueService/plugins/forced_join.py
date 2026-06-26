from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ChatMemberUpdated
from pyrogram.errors import UserNotParticipant
from pyrogram.enums import ButtonStyle
from BlueService import app, STEP, settings_helper
from BlueService.filters import StepFilter, OwnerFilter
from BlueService.sql_helpers import UsersHelper, ForcedJoinChannelsHelper, ForcedJoinUsersHelper
from BlueService.buttons import admin_forced_join_edit_markup, start_markup
from BlueService.decorators import anti_spam

user_helper = UsersHelper()
forced_join_channels_helper = ForcedJoinChannelsHelper()
forced_join_users_helper = ForcedJoinUsersHelper()

back_button = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="forced_join")]])

@app.on_callback_query(filters.regex(r"^forced_join$") & OwnerFilter())
async def forced_join(client : Client, callback_query : CallbackQuery):
    STEP[callback_query.from_user.id] = "Home"
    await callback_query.edit_message_text("جوین اجباری", reply_markup=admin_forced_join_edit_markup())
    return

@app.on_callback_query(filters.regex(r"^add_forced_join_channel$") & OwnerFilter())
async def add_forced_join_channel(client: Client, callback_query: CallbackQuery):
    channel_count = forced_join_channels_helper.get_forced_join_channels_count()

    if channel_count >= 10:
        await callback_query.answer("حداکثر 10 کانال قابل افزودن است", show_alert=True)
        return
    await callback_query.message.reply_text("آیدی عددی کانال را وارد کنید", reply_markup=back_button)
    STEP[callback_query.from_user.id] = "AddForcedJoinChannelId"
    return

@app.on_message(filters.text & StepFilter("AddForcedJoinChannelId") & OwnerFilter() & filters.private)
async def add_forced_join_channel_id(client: Client, message: Message):
    channel_id = message.text
    channel = forced_join_channels_helper.get_forced_join_channel_by_channel_id(channel_id)
    if channel:
        await message.reply_text("این کانال قبلا افزوده شده است", reply_markup=admin_forced_join_edit_markup())
        STEP[message.from_user.id] = "Home"
        return

    await message.reply_text("نام کانال را وارد کنید", reply_markup=back_button)
    STEP[message.from_user.id] = ("AddForcedJoinChannelName", channel_id)
    return

@app.on_message(filters.text & StepFilter("AddForcedJoinChannelName") & OwnerFilter() & filters.private)
async def add_forced_join_channel_name(client: Client, message: Message):
    channel_name = message.text
    channel_id = STEP[message.from_user.id][1]
    await message.reply_text("لینک کانال را وارد کنید", reply_markup=back_button)
    STEP[message.from_user.id] = ("AddForcedJoinChannelLink", channel_id, channel_name)
    return

@app.on_message(filters.text & StepFilter("AddForcedJoinChannelLink") & OwnerFilter() & filters.private)
async def add_forced_join_channel_link(client: Client, message: Message):
    channel_link = message.text
    channel_id = STEP[message.from_user.id][1]
    channel_name = STEP[message.from_user.id][2]
    forced_join_channels_helper.insert_forced_join_channel(channel_id, channel_name, channel_link)
    await message.reply_text("کانال با موفقیت اضافه شد ربات رو حتما تو کانال مورد نظر ادمین کنید", reply_markup=admin_forced_join_edit_markup())
    STEP[message.from_user.id] = "Home"
    return

@app.on_callback_query(filters.regex(r"^forced_join_channel_(\d+)") & OwnerFilter())
async def delete_forced_join_channel(client: Client, callback_query: CallbackQuery):

    channel_id = int(callback_query.data.split("_")[3])

    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🔰 تغییر اسم کانال", callback_data=f"change_forced_join_channel_name_{channel_id}"),
                InlineKeyboardButton("🔰 تغییر لینک کانال", callback_data=f"change_forced_join_channel_link_{channel_id}")
            ],
            [
                InlineKeyboardButton("❌ حذف کانال", callback_data=f"delete_forced_join_channel_{channel_id}")

            ],
            [
                InlineKeyboardButton("🔙 بازگشت", callback_data="forced_join")
            ]
        ]
    )

    forced_join_channel = forced_join_channels_helper.get_forced_join_channel(channel_id)

    text = f"""🔒 اطلاعات کانال جوین اجباری

👤 نام کانال: {forced_join_channel.channel_name}
🔗 لینک کانال: {forced_join_channel.channel_link}
🆔 ایدی کانال: {forced_join_channel.channel_id}
    """

    await callback_query.edit_message_text(text, reply_markup=markup)
    return

@app.on_callback_query(filters.regex(r"^delete_forced_join_channel_(\d+)") & OwnerFilter())
async def delete_forced_join_channel(client: Client, callback_query: CallbackQuery):
    channel_id = int(callback_query.data.split("_")[4])
    forced_join_channels_helper.delete_forced_join_channel(channel_id)
    await callback_query.edit_message_text("کانال با موفقیت حذف شد", reply_markup=admin_forced_join_edit_markup())
    return

@app.on_callback_query(filters.regex(r"^change_forced_join_channel_name_(\d+)") & OwnerFilter())
async def change_forced_join_channel_name(client: Client, callback_query: CallbackQuery):
    channel_id = int(callback_query.data.split("_")[5])
    forced_join_channel = forced_join_channels_helper.get_forced_join_channel(channel_id)
    await callback_query.edit_message_text(f"نام کانال را وارد کنید\n\n{forced_join_channel.channel_name}", reply_markup=back_button)
    STEP[callback_query.from_user.id] = ("ChangeForcedJoinChannelName", channel_id)
    return

@app.on_message(filters.text & StepFilter("ChangeForcedJoinChannelName") & OwnerFilter() & filters.private)
async def change_forced_join_channel_name(client: Client, message: Message):
    channel_id = STEP[message.from_user.id][1]
    forced_join_channels_helper.update_forced_join_channel(channel_id, channel_name=message.text)
    await message.reply_text("نام کانال با موفقیت تغییر کرد", reply_markup=admin_forced_join_edit_markup())
    STEP[message.from_user.id] = "Home"
    return

@app.on_callback_query(filters.regex(r"^change_forced_join_channel_link_(\d+)") & OwnerFilter())
async def change_forced_join_channel_link(client: Client, callback_query: CallbackQuery):
    channel_id = int(callback_query.data.split("_")[5])
    forced_join_channel = forced_join_channels_helper.get_forced_join_channel(channel_id)
    await callback_query.edit_message_text(f"لینک کانال را وارد کنید\n\n{forced_join_channel.channel_link}", reply_markup=back_button)
    STEP[callback_query.from_user.id] = ("ChangeForcedJoinChannelLink", channel_id)
    return

@app.on_message(filters.text & StepFilter("ChangeForcedJoinChannelLink") & OwnerFilter() & filters.private)
async def change_forced_join_channel_link(client: Client, message: Message):
    channel_id = STEP[message.from_user.id][1]
    forced_join_channels_helper.update_forced_join_channel(channel_id, channel_link=message.text)
    await message.reply_text("لینک کانال با موفقیت تغییر کرد", reply_markup=admin_forced_join_edit_markup())
    STEP[message.from_user.id] = "Home"
    return

@app.on_chat_member_updated()
async def forced_join(client: Client, chat_member: ChatMemberUpdated):

    if not chat_member.old_chat_member:
        return

    forced_join_channels = forced_join_channels_helper.get_forced_join_channels()

    channels = [channel.channel_id for channel in forced_join_channels]

    if chat_member.chat.id not in channels:
        return
    
    user = chat_member.from_user.id
    forced_join_user = forced_join_users_helper.get_forced_join_user(user, chat_member.chat.id)

    if forced_join_user:
        forced_join_users_helper.delete_forced_join_user(user, chat_member.chat.id)
    return

@app.on_callback_query(filters.regex(r"^user_click_join"))
@anti_spam
async def user_click_join(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    forced_join_channels = forced_join_channels_helper.get_forced_join_channels()
    markup = []

    for channel in forced_join_channels:
        forced_users = forced_join_users_helper.get_forced_join_user(user_id, channel.channel_id)
        if forced_users:
            continue
        try:
            member = await app.get_chat_member(channel.channel_id, user_id)
            forced_join_users_helper.insert_forced_join_user(user_id, channel.channel_id)
        except UserNotParticipant:
            markup.append(
                [
                    InlineKeyboardButton(
                        text = f"{channel.channel_name}",
                        url = f"{channel.channel_link}",
                        style=ButtonStyle.PRIMARY,
                        icon_custom_emoji_id="5350831267090809192"
                    )
                ]
            )

    if markup:
        markup.append([InlineKeyboardButton("عضو شدم", callback_data="user_click_join")])
        await callback_query.answer("📣 هنوز در برخی از کانال ها عضو نشده اید", show_alert=True)
        try:
            await callback_query.edit_message_text("![✈️](tg://emoji?id=5332423642850536254) لطفا ابتدا در کانال ها عضو شوید:", reply_markup=InlineKeyboardMarkup(markup))
        except:
            pass
        return
    
    await callback_query.message.delete()

    user_id = callback_query.from_user.id

    setting = settings_helper.get_settings()
    is_welcome_message_exists = setting.wellcome_message or None
    
    if not is_welcome_message_exists:
        await callback_query.message.reply("![✨](tg://emoji?id=5222108309795908493) سلام دوست عزیز به ربات ما خوش آمدی", reply_markup=start_markup(callback_query.from_user.id))
        return

    await callback_query.message.reply(setting.wellcome_message, reply_markup=start_markup(callback_query.from_user.id))

    await callback_query.answer("✅ می توانید از ربات استفاده کنید")      
    return
    