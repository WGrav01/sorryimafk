import os

import aiosqlite
import discord
from discord.ext import commands

from utils import bot
from utils import duration
from utils import logger
from utils import time

log = logger.Logger.afkbot_logger
bot = bot.Bot


class CheckUSR(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="checkusr", description="Check if user is afk")
    async def checkusr(self, ctx,
                       member: discord.Option(discord.Member,
                                              description='Check if this member is afk (leave blank to check yourself)',
                                              required=False)):
        if member is None:
            member = ctx.user
            log.debug(f'Member left blank, defaulting to {ctx.user.id}')

        log.debug(f'User {ctx.user.id} fetched {member}')

        db = await aiosqlite.connect(os.path.join(os.path.dirname(__file__), '..', 'users.sqlite'))
        log.debug(f'Connected to database {db}')
        query = 'SELECT * FROM Afk WHERE :usr = usr'
        log.debug(f'Query: {query}')
        values = {'usr': member.id}
        log.debug(f'Values: {values}')
        log.debug(f'Checking if user {member.id} is in the database')
        try:
            result = await db.execute_fetchall(query, values)
            log.debug(f'User id result: {result[0][0]}')
            log.debug(f'Channel id result: {result[0][5]}')
        except IndexError:
            log.debug(f'User {member.id} not found in database')
            not_afk = discord.Embed(title=f'Error: {member} is not AFK', color=discord.Color.red())
            await db.close()
            log.debug(f'Closed database connection')
            await ctx.respond(embed=not_afk, ephemeral=True)
            log.info(f'Sent error message to user {ctx.user.id}')
            return
        else:
            log.debug(f'User {member.id} is in the database')
            afk = discord.Embed(title=f'User {member} is AFK', color=discord.Color.orange())
            if result[0][1] is not None:
                log.debug(f'{member} has status {result[0][1]}')
                afk.add_field(name='With status', value=result[0][1])
            else:
                log.debug(f'{member} has no status')
            if result[0][2] is not None:
                log.debug(f'{member} has has ETA until back {result[0][2]}')
                afk.add_field(name='ETA until back', value=result[0][2])
            else:
                log.debug(f'{member} has no ETA until back')
            afk.set_thumbnail(url=member.display_avatar.url)
            afk.set_footer(text=f'{member} has been away for'
                                f' {await duration.time_duration(start_str=result[0][4], end_str=time.now())}')
            await db.close()
            log.debug(f'Closed database connection')
            await ctx.respond(embed=afk, ephemeral=True)
            log.info(f"Sent {member}'s afk status message to user {ctx.user.id}")


def setup(bot):  # this is called by Pycord to set up the cog
    log.debug('Running checkusr cog setup function')
    bot.add_cog(CheckUSR(bot))  # add the cog to the bot
