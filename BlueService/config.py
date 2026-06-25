from decouple import config

# Basics
API_ID = config('API_ID', default=None, cast=int)
API_HASH = config('API_HASH', default=None)
BOT_TOKEN = config('BOT_TOKEN', default=None)
OWNER = config('OWNER', default=None, cast=int)