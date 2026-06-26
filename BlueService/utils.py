import sys
import logging
from pathlib import Path
import importlib
from datetime import datetime
import jdatetime
from datetime import date, datetime, timedelta

def load_plugins(plugin_name):
    path = Path(f"BlueService/plugins/{plugin_name}.py")
    name = "BlueService.plugins.{}".format(plugin_name)
    spec = importlib.util.spec_from_file_location(name, path)
    load = importlib.util.module_from_spec(spec)
    load.logger = logging.getLogger(plugin_name)
    sys.modules["BlueService.plugins." + plugin_name] = load
    spec.loader.exec_module(load)
    print("BlueService has Imported " + plugin_name)

def jalali_time(date_time : datetime):
    if isinstance(date_time, datetime):
        return jdatetime.datetime.fromgregorian(datetime=date_time)
    elif isinstance(date_time, date):
        return jdatetime.date.fromgregorian(date=date_time)
    

def progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=20, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '▒' * (length - filled_length)
    msg = f'\r{prefix} |{bar}| {percent}% {suffix}'
    return msg

def time_formatter(td : timedelta = None, miliseconds : int = None):
    if td is not None:
        total_seconds = td.total_seconds()
        milliseconds = total_seconds * 1000
    else:
        milliseconds = miliseconds
    minutes, seconds = divmod(int(milliseconds / 1000), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    tmp = (
        ((str(weeks) + " هفته:") if weeks else "")
        + ((str(days) + " روز:") if days else "")
        + ((str(hours) + " ساعت:") if hours else "")
        + ((str(minutes) + " دقیقه:") if minutes else "")
        + ((str(seconds) + " ثانیه") if seconds else "")
    )
    if not tmp:
        return "0 ثانیه"

    if tmp.endswith(":"):
        return tmp[:-1]
    return tmp