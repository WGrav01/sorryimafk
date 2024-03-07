import discord  # pycord, not discord.py
import aiosqlite
import logger
import os
from dotenv import load_dotenv

load_dotenv()  # load the .env file

log = logger.Logger()  # initialize the logger


class Bot(discord.AutoShardedBot):  # autosharded bot ensures improved performance when in many servers
    async def on_ready(self, owner_id=os.getenv('OWNER_ID')):  # runs when the bot logs in (initializes database)
        log.info(f'Logged in successfully as {self.user} with ID {self.user.id}')
        log.debug(f'Owner ID: {owner_id}')  # print the owner ID for debugging
        db_init_query = ("CREATE TABLE IF NOT EXISTS Afk"  # initalizes the database
                         " (usr INTEGER PRIMARY KEY, status VARCHAR(1024), time_back VARCHAR(1024))")
        db = aiosqlite.connect('sqlite+aiosqlite:///users.sqlite')  # connect to the database (and create it if missing)
        await db.execute(db_init_query)  # execute the query
        await db.commit()  # commit the changes
        await db.close()  # close the database
