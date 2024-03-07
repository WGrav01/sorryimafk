import discord
import aiosqlite
import logger
import os
from dotenv import load_dotenv

load_dotenv()
log = logger.Logger()


class Bot(discord.AutoShardedBot):
    async def on_ready(self, owner_id=os.getenv('OWNER_ID')):
        log.info(f'Logged in successfully as {self.user} with ID {self.user.id}')
        log.debug(f'Owner ID: {owner_id}')
        db_init_query = ("CREATE TABLE IF NOT EXISTS Afk"
                         " (usr INTEGER PRIMARY KEY, status VARCHAR(1024), time_back VARCHAR(1024))")
        db = aiosqlite.connect('sqlite+aiosqlite:///users.sqlite')
        await db.execute(db_init_query)
        await db.commit()
        await db.close()
