from datetime import datetime
from utils import logger

log = logger.Logger.afkbot_logger


async def time_duration(start_str, end_str):
    """
    Calculate the duration between two time strings and return the duration in days, hours, minutes, and seconds.

    Parameters:
    start_str (str): The start time string in the format '%d %B, %Y'
    end_str (str): The end time string in the format '%d %B, %Y'

    Returns:
    str: The duration in days, hours, minutes, and seconds
    """

    start = datetime.strptime(start_str, '%m-%d-%Y, %X')
    log.debug(f'Start: {start}')
    end = datetime.strptime(end_str, '%m-%d-%Y, %X')
    log.debug(f'End: {end}')
    delta = end - start
    log.debug(f'Delta: {delta}')

    seconds = delta.total_seconds()
    log.debug(f'Seconds: {seconds}')
    days, seconds = divmod(seconds, 24 * 3600)
    log.debug(f'Days: {days}, Seconds: {seconds}')
    hours, seconds = divmod(seconds, 3600)
    log.debug(f'Hours: {hours}, Seconds: {seconds}')
    minutes, seconds = divmod(seconds, 60)
    log.debug(f'Minutes: {minutes}, Seconds: {seconds}')

    duration_parts = []
    log.debug(f'Duration parts: {duration_parts}')
    if days:
        duration_parts.append(f"{int(days)} days")
        log.debug(f'Duration parts: {duration_parts}')
    if hours:
        duration_parts.append(f"{int(hours)} hours")
        log.debug(f'Duration parts: {duration_parts}')
    if minutes:
        duration_parts.append(f"{int(minutes)} minutes")
        log.debug(f'Duration parts: {duration_parts}')
    if seconds:
        duration_parts.append(f"{int(seconds)} seconds")
        log.debug(f'Duration parts: {duration_parts}')

    log.debug(f'Duration parts: {duration_parts}')
    if len(duration_parts) == 1:
        return duration_parts[0]
    else:
        return ', '.join(duration_parts[:-1]) + ', and ' + duration_parts[-1]
