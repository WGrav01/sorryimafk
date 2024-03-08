import discord  # pycord, not discord.py
import aiosqlite
from utils import logger
import os
from dotenv import load_dotenv

load_dotenv()  # load the .env file

log = logger.Logger.afkbot_logger  # initialize the logger

"""
runs when the bot logs in (initializes database)

Parameters:
    owner_id (int): the owner's ID

Returns:
    None
"""


class Bot(discord.AutoShardedBot):  # autosharded bot ensures improved performance when in many servers
    async def on_ready(self, owner_id=os.getenv('OWNER_ID')):  # runs when the bot logs in (initializes database)
        log.info(f'Logged in successfully as {self.user} with ID {self.user.id}')
        log.debug(f'Owner ID: {owner_id}')  # print the owner ID for debugging
        db_init_query = ("CREATE TABLE IF NOT EXISTS Afk"  # initalizes the database
                         " (usr INTEGER PRIMARY KEY, status VARCHAR(1024), time_back VARCHAR(1024),"
                         " quiet INTEGER(1, 0), time VARCHAR(23), channel INTEGER)")
        db = await aiosqlite.connect(os.path.join(os.path.dirname(__file__), '..', 'users.sqlite'))
        await db.execute(db_init_query)  # execute the query
        await db.commit()  # commit the changes
        await db.close()  # close the database
