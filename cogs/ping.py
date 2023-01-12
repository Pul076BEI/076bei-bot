import re

from discord.ext import commands

import libs.config as config

####################
# Config variables #
####################
c_prefix = config.get_config("prefix")

####################
# Constant         #
####################
PATTERN = r"^<@!808012864941981726>$"


class Ping(commands.Cog, name="Ping commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return

        if re.match(PATTERN, msg.content):
            await msg.channel.send(f"Hi! My prefix here is: `{c_prefix}`")

    @commands.command(name="ping")
    async def _ping(self, ctx):
        """Replies latency"""
        await ctx.channel.send(f"Pong! `{round(self.bot.latency * 1000)}` ms")


def setup(bot):
    bot.add_cog(Ping(bot))
