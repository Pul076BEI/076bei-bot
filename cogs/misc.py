import requests

from discord.ext import commands

import libs.config as config

####################
# Config variables #
####################
c_prefix = config.get_config("prefix")

####################
# String variables #
####################
s_joke_api_URL = config.get_string("joke_api_URL")


class Misc(commands.Cog, name="Misc commands"):
    def __init__(self, bot):
        self.bot = bot

    def check_status_code(self, response: str):
        if response.status_code == 200:
            return response.json()
        return False

    def fetch_joke(self) -> str:
        response = requests.get(s_joke_api_URL)
        joke = self.check_status_code(response)

        if not joke:
            return f"[{response.status_code}]: Could not get a joke, try again later."
        return f"{joke['setup']}" + "\n" + f"{joke['punchline']}"


    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return

        if msg.content.startswith("<@!"+str(self.bot.user.id)+">"):
            await msg.channel.send(f"Hi! My prefix here is: `{c_prefix}`")

    @commands.command(name='ping')
    async def _ping(self, ctx):
        """Replies latency"""
        await ctx.channel.send(f"Pong! `{round(self.bot.latency * 1000)}` ms")

    @commands.command(name='joke')
    async def _joke(self, ctx):
        """Fetches a joke"""
        await ctx.channel.send(self.fetch_joke())
    
        
def setup(bot):
    bot.add_cog(Misc(bot))