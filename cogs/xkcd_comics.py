import aiohttp
from soup2dict import convert
from bs4 import BeautifulSoup

from discord.ext import commands

import libs.config as config

####################
# String variables #
####################
s_xkcd_comics_url = config.get_string("xkcd_comics_url")


class XkcdComics(commands.Cog, name="Xkcd Comics"):
    def __init__(self, bot):
        self.bot = bot

    def parse_html(self, html_block):
        comic = convert(html_block)["div"][0]["img"][0]
        comic_alt = comic["@alt"]
        comic_title = comic["@title"]
        comic_url = comic["@src"][2:]
        return (comic_alt, "https://" + comic_url, comic_title)

    async def get_comic(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(s_xkcd_comics_url) as response:
                r = await response.text()
                soup = BeautifulSoup(r, "html.parser")
        comic_alt, comic_url, comic_title = self.parse_html(soup.findAll(id="comic"))
        return {"alt": comic_alt, "title": comic_title, "url": comic_url}

    @commands.command(name="xkcd", aliases=["x"])
    async def _xkcd(self, ctx):
        """
        Fetches a random xkcd comic
        """
        comic = await self.get_comic()
        await ctx.channel.send(
            "**" + comic["alt"] + "**\n*" + comic["title"] + "*\n" + comic["url"]
        )


def setup(bot):
    bot.add_cog(XkcdComics(bot))
