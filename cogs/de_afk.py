import os

import aiosqlite
import discord
from discord.commands import Option
from discord.ext import commands

from utils import logger
from utils import time
from utils import duration
from utils import bot

log = logger.Logger.afkbot_logger
bot = bot.Bot


class DeAfk(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="de-afk", description="Remove your AFK status")
    async def deafk(
        self,
        ctx,
        quiet: Option(
            str,
            description="Do you the bot to not announce your coming back?",
            required=True,
            choices=["Off", "On"],
        ),
    ):

        log.debug(
            f"Received de-afk command from user {ctx.user.name}, in channel {ctx.channel.id},"
            f" quiet: {quiet}"
        )

        db = await aiosqlite.connect(
            os.path.join(os.path.dirname(__file__), "..", "users.sqlite")
        )
        log.debug(f"Connected to database {db}")
        query = "SELECT * FROM Afk WHERE :usr = usr"
        log.debug(f"Query: {query}")
        values = {"usr": ctx.user.id}
        log.debug(f"Values: {values}")
        log.debug(f"Checking if user {ctx.user.id} is in the database")
        try:
            result = await db.execute_fetchall(query, values)
            log.debug(f"User id result: {result[0][0]}")
            log.debug(f"Channel id result: {result[0][5]}")
        except IndexError:
            log.debug(f"User {ctx.user.id} not found in database")
            not_afk = discord.Embed(
                title="Error: you are not AFK", color=discord.Color.red()
            )
            await db.close()
            log.debug(f"Closed database connection")
            await ctx.respond(embed=not_afk, ephemeral=True)
            log.debug(f"Sent error message to user {ctx.user.id}")
            return

        if quiet == "On":
            log.debug("Setting quiet to 1 and deferring")
            await ctx.defer(ephemeral=True)
            quiet = 1
        elif quiet == "Off":
            log.debug("Setting quiet to 0 and deferring")
            await ctx.defer(ephemeral=False)
            quiet = 0

        log.debug(f"User {ctx.user.id} is in the database")
        query = "DELETE FROM Afk WHERE :usr = usr"
        log.debug(f"Query: {query}")
        values = {"usr": ctx.user.id}
        log.debug(f"Values: {values}")
        await db.execute(query, values)
        log.debug(f"Executed query with values {values}")
        await db.commit()
        log.debug(f"Committed query")
        await db.close()
        log.debug(f"Closed database connection")

        afk = discord.Embed(
            title=f"Welcome back {ctx.user.nick}!", color=discord.Color.green()
        )
        log.debug(f"Created afk embed")
        afk_duration_coroutine = duration.time_duration(
            start_str=result[0][4], end_str=time.now()
        )
        afk_duration = await afk_duration_coroutine
        log.debug(
            f"start_str: {result[0][4]}, end_str: {time.now()}, duration: {afk_duration}"
        )
        afk.add_field(name="You have been away for", value=afk_duration, inline=False)
        log.debug(f"Added field with value {afk_duration} to deafk embed")

        user = ctx.user
        log.debug(f"Fetched user: {user}, id: {user.id}")
        pfp = user.avatar.url
        log.debug(f"Fetched avatar URL for {user}, URL: {pfp}")
        afk.set_thumbnail(url=pfp)
        log.debug(f"Set thumbnail to {pfp}")

        afk.set_footer(text=f"Current UTC time: {time.now()}")
        log.debug(f"Set footer to current UTC time: {time.now()}")

        await ctx.respond(embed=afk, ephemeral=quiet)
        log.debug(f"Responding, ephemeral = {quiet}")
        log.info(f"User {user} is now marked as not afk")


def setup(bot):  # this is called by Pycord to set up the cog
    log.debug("Running de-afk cog setup function")
    bot.add_cog(DeAfk(bot))  # add the cog to the bot
