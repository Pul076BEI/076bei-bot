import requests
import asyncio
import typing
import re

from discord.ext import commands

import libs.config as config

####################
# Config variables #
####################
c_prefix = config.get_config("prefix")

####################
# String variables #
####################
s_jokes = config.get_string("joke_endpoints")

####################
# Constant         #
####################
time_to_wait = 3
PATTERN = r"^<@!808012864941981726>$"


class Misc(commands.Cog, name="Misc commands"):
    def __init__(self, bot):
        self.bot = bot

    def check_status_code(self, response: str):
        if response.status_code == 200:
            return response.json()
        return False

    def fetch_joke(self, joke_type: str):
        response = requests.get(s_jokes[joke_type])
        joke_dict = self.check_status_code(response)

        if not joke_dict:
            return f"[{response.status_code}]: Could not get a joke, try again later."
        return joke_dict

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

    @commands.command(name="joke", aliases=["jk"])
    async def _joke(self, ctx, joke_type: typing.Optional[str] = "random"):
        """
        Fetches a joke
        types = [r]andom; [p]rogramming, [g]eneral
        """
        if joke_type not in s_jokes.keys() or joke_type == "list":
            await ctx.channel.send(f"Available joke types: {', '.join(s_jokes.keys())}")
            return

        joke = self.fetch_joke(joke_type)

        if isinstance(joke, str):
            await ctx.channel.send(joke)
            return
        elif isinstance(joke, list):
            joke = joke[0]

        await ctx.channel.send(joke["setup"])
        await asyncio.sleep(time_to_wait)
        await ctx.channel.send(joke["punchline"])


def setup(bot):
    bot.add_cog(Misc(bot))
