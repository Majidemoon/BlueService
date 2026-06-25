import logging
import sys

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