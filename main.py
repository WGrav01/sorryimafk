from utils import logger
from dotenv import load_dotenv
import os
from utils import bot

"""
Main module for starting up the bot and loading cogs. (consider it the launcher)

This module initializes the bot, loads the necessary cogs, and runs the bot with the token from the .env file.

Attributes:
    None

Methods:
    None
"""

load_dotenv()
bot = bot.Bot()
log = logger.Logger()

log.info('Starting up...')
for filename in os.listdir('./cogs'):  # load all the cogs and print that they've been loaded
    log.debug(f'Found file {filename}')
    if filename.endswith('.py') and filename.startswith('#') is False:  # check if it is a python file and not disabled
        bot.load_extension(f"cogs.{filename[:-3]}")
        log.debug(f"Loaded cogs.{filename[:-3]}")
log.debug('Done loading cogs')

log.debug(f'Running bot with token {os.getenv("DISCORD_TOKEN")}')
bot.run(os.getenv('DISCORD_TOKEN'))
