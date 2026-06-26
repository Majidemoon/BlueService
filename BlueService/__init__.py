from BlueService.database import engine, SessionLocal
from BlueService.sql_helpers import SettingsHelper
from sqlalchemy import text
from pyrogram import Client
from datetime import datetime
from BlueService.logger import logger
from BlueService.config import API_ID, API_HASH, BOT_TOKEN

# Users Step
STEP = dict()
key = 7655485471 # This is a random naumber for encrypt and decrypt !dont change it if this change database will not work properly

anti_spam_list : dict[int, datetime] = {} # user_id: created_at

# Initial database settings
# Activate foreign keys
with engine.connect() as conn:
    conn.execute(text("PRAGMA foreign_keys = ON;"))


app = Client('mainbot', API_ID, API_HASH, bot_token=BOT_TOKEN)

settings_helper = SettingsHelper()