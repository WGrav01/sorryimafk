import os

import aiosqlite
import discord
from discord.commands import Option
from discord.ext import commands

from utils import logger
from utils import time

log = logger.Logger.afkbot_logger


class GoAfk(commands.Cog):
    """
    A function to handle the user going AFK via the /afk command
    - Parameters:
        - ctx: The context of the command.
        - status (str): Enter the reason for being afk (optional), max length 1024.
        - time_back (str): When do you plan on being back? (optional), max length 1024.
        - quiet (str): Do you want the bot to not announce your being AFK? Choices: ['On', 'Off']
    - Returns: None
    """

    @discord.slash_command(name="afk", description="Go afk")
    async def goafk(self, ctx,
                    quiet: Option(str, description='Do you the bot to not announce your being AFK?', required=True,
                                  choices=['Off', 'On']),
                    status: Option(str, description='Enter the reason for being afk (optional)', max_length=1024,
                                   required=False),
                    time_back: Option(str, description='Describe when you plan on being back (optional)',
                                      max_length=1024, required=False)):

        log.debug(f'Received afk command from user {ctx.user.name}, in channel {ctx.channel.name},'
                  f' status: {status}, time_back: {time_back}, quiet: {quiet}')

        if len(status) > 1024:  # discord's per field character limit is 1024
            status_character_limit = discord.Embed(title='Error',
                                                   description=f'Your status is {len(status)}'
                                                               f' characters long, but the maximum is 1024.',
                                                   color=discord.Color.red())
            await ctx.respond(embed=status_character_limit, ephemeral=True)
            log.debug(f'Status for {ctx.user} is too long, responding with error embed')
            return
        elif len(time_back) > 1024:
            time_back_character_limit = discord.Embed(title='Error',
                                                      description=f'Your ETA until back is {len(status)}'
                                                                  f' characters long, but the maximum is 1024.',
                                                      color=discord.Color.red())
            await ctx.respond(embed=time_back_character_limit, ephemeral=True)
            log.debug(f'Time back for {ctx.user} is too long, responding with error embed')
            return
        elif len(status) > 1024 and len(time_back) > 1024:
            character_limit = discord.Embed(title='Error',
                                            description=f'Both your status ({len(status)} characters long) and your '
                                                        f'ETA until back ({len(time_back)} characters long) are '
                                                        f'over the character limit of 1024.', color=discord.Color.red())
            await ctx.respond(embed=character_limit, ephemeral=True)
            log.debug(f'Status and time back for {ctx.user} are too long, responding with error embed')
            return

        if quiet == 'On':
            log.debug('Setting quiet to 1 and deferring')
            await ctx.defer(ephemeral=True)
            quiet = 1
        elif quiet == 'Off':
            log.debug('Setting quiet to 0 and deferring')
            await ctx.defer(ephemeral=False)
            quiet = 0

        query = ('INSERT OR REPLACE INTO Afk (usr, status, time_back, quiet, time, channel)'
                 ' VALUES (:usr, :status, :time_back, :quiet, :time, :channel)')
        log.debug(f'Query: {query}')
        values = {'usr': ctx.user.id, 'status': status, 'time_back': time_back, 'quiet': quiet,
                  'time': time.now(), 'channel': ctx.channel.id}
        log.debug(f'Values: {values}')
        db = await aiosqlite.connect(os.path.join(os.path.dirname(__file__), '..', 'users.sqlite'))
        log.debug(f'Connected to database')
        await db.execute(query, values)
        log.debug(f'Executed query')
        await db.commit()
        log.debug(f'Committed query')
        await db.close()
        log.debug(f'Closed database connection')

        afk = discord.embeds.Embed(title=f'✅ {ctx.user.name} is now afk', color=discord.Color.green())
        log.debug(f'Created afk embed')
        user = ctx.user
        log.debug(f'Fetched user: {user}, id: {user.id}')
        pfp = user.avatar.url
        log.debug(f'Fetched avatar URL for {user}, URL: {pfp}')
        if status is not None:
            afk.add_field(name='Status', value=str(status))
            log.debug(f'Added status {status} to embed')
        else:
            log.debug(f'Status is none, not adding to embed')
        if time_back is not None:
            afk.add_field(name='Estimated time back', value=str(time_back), inline=True)
            log.debug(f'Adding ETA {time_back} to embed')
        else:
            log.debug('ETA is none, not adding to embed')
        afk.set_thumbnail(url=pfp)
        log.debug(f'Set thumbnail to {pfp}')
        afk.set_footer(text=f'Current UTC time: {time.now()}')
        log.debug(f'Set footer to current UTC time: {time.now()}')

        await ctx.respond(embed=afk, ephemeral=quiet == 1)
        log.debug(f'Responding, ephemeral = {quiet == 1}')
        log.info(f'User {user} is now marked as afk')

    def __init__(self, bot):
        self.bot = bot


# this is called by Pycord to set up the cog
def setup(bot):  # this is called by Pycord to set up the cog
    log.debug('Running afk cog setup function')
    bot.add_cog(GoAfk(bot))  # add the cog to the bot
