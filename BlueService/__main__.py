import glob
from pathlib import Path
from BlueService.utils import load_plugins
import logging
from BlueService import app
from BlueService.scheduler import start_scheduler
import asyncio

path = "BlueService/plugins/*.py"
files = glob.glob(path)
for name in sorted(files):
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))

print("Successfully deployed!")
print("Enjoy!")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_scheduler())
    app.run()