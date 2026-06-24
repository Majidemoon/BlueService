from apscheduler.schedulers.asyncio import AsyncIOScheduler
from BlueService import app, OWNER, anti_spam_list
from BlueService.sql_helpers import SettingsHelper
from datetime import datetime, timedelta
from BlueService.utils import jalali_time

settings_helper = SettingsHelper()

async def anti_spam():
    try:
        for user in anti_spam_list:
            if datetime.now() - anti_spam_list[user] > timedelta(seconds=0.5):
                del anti_spam_list[user]
    except RuntimeError:
        pass
    return
                
async def backup():
    settings = settings_helper.get_settings()
    caption = f'🕰{jalali_time(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")}'

    try:
        if not (settings and settings.topic_group and settings.backup_topic):
            raise ValueError()
        
        await app.send_document(settings.topic_group, "database.db", caption=caption, message_thread_id=settings.backup_topic)
    except:
        try:
            await app.send_document(OWNER, "database.db", caption=caption)
        except:
            pass



async def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(anti_spam, "interval", seconds=1)
    scheduler.add_job(backup, "interval", hours=6)
    scheduler.start()
    return scheduler