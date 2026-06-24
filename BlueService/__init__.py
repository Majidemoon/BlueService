from BlueService.database import engine, SessionLocal
from BlueService.sql_helpers import SettingsHelper
import BlueService.models
from sqlalchemy import text
from pyrogram import Client
from decouple import config
import logging
import sys
from datetime import datetime

# Create logger 
logger = logging.getLogger('BlueService')
logger.setLevel(logging.INFO)


# Console Handler: Logs INFO to console 
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter(f'[%(levelname)s - %(asctime)s] %(name)s: %(message)s')
console_handler.setFormatter(console_formatter)


# File Handler: Logs ERROR and CRITICAL to a file
file_handler = logging.FileHandler('error_logs.log', mode='a', encoding='utf-8')
file_handler.setLevel(logging.ERROR)
file_formatter = logging.Formatter("[%(levelname)s - %(asctime)s] %(name)s: %(message)s")
file_handler.setFormatter(file_formatter)


# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


logger.info('"Logger is configured successfully.')


# Basics
API_ID = config('API_ID', default=None, cast=int)
API_HASH = config('API_HASH', default=None)
BOT_TOKEN = config('BOT_TOKEN', default=None)
OWNER = config('OWNER', default=None, cast=int)
# Users Step
STEP = dict()
key = 7655485471 # This is a random naumber for encrypt and decrypt !dont change it if this change database will not work properly

anti_spam_list : dict[int, datetime] = {} # user_id: created_at

# Initial database settings
# Activate foreign keys
with engine.connect() as conn:
    conn.execute(text("PRAGMA foreign_keys = ON;"))


app = Client('mainbot', API_ID, API_HASH, bot_token=BOT_TOKEN)

settings = SettingsHelper()