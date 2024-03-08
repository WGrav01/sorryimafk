from datetime import datetime
import pytz
from utils import logger

log = logger.Logger.afkbot_logger

"""
get the full, formatted, datetime string
"""


def now():  # get the full datetime string
    log.debug(f'Now: {datetime.now()}')
    raw_now = datetime.now(pytz.utc)  # get current datetime in utc
    log.debug(f'Raw now: {raw_now}')
    log.debug(f'Formatted now: {raw_now.strftime("%m-%d-%Y, %X")}')
    return raw_now.strftime('%m-%d-%Y, %X')  # convert to string and return
