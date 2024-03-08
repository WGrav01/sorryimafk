from datetime import datetime
import pytz

"""
get the full, formatted, datetime string
"""


def now():  # get the full datetime string
    raw_now = datetime.now(pytz.utc)  # get current datetime in utc
    return raw_now.strftime('%d %B, %Y')  # convert to string and return
