import sys
import logging
from pathlib import Path
import importlib
from datetime import datetime
import jdatetime
from datetime import date, datetime

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