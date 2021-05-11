import re
from urllib.parse import unquote

from unalix import clear_url, unshort_url
from discord.ext import commands

URL_PATTERN = re.compile(r"(https?://\S+|https?://www\.\S+|www\.\S+)")
# puncts = ',.?\'"-:!'
puncts = "!\"$%'()*+,-.:;<>?@[\\]^_`{|}~"


class Clean_URL(commands.Cog, name="Clean URLs"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return

        found_links = list(set(URL_PATTERN.findall(msg.content.replace("`", ""))))

        if not found_links:
            return

        found_links = [unquote(url) for url in found_links]  # decode the urls
        links = []

        for link in found_links:
            if link[-1] in puncts:
                links.append(link[:-2])
            else:
                links.append(link)

        clean_links = {}

        for link in links:
            try:
                tmp = unshort_url(
                    clear_url(link)
                )  # tries to unshort url if services like tinyurl, bitly are used
            except:
                tmp = clear_url(link)  # no url shortening services used

            if tmp == link:
                continue
            else:
                clean_links[link] = tmp

        if not len(clean_links.values()):  # if no unclean url, do nothing
            return

        plural = "s" if len(clean_links.values()) != 1 else ""
        to_send = "\n".join(
            [
                clean_link + " -> [Foul URL: <" + old_link + "> ]"
                for old_link, clean_link in clean_links.items()
            ]
        )
        await msg.channel.send(
            f":warning: **Foul URL{plural} detected. Cleaned URL{plural}:**\n{to_send}"
        )


def setup(bot):
    bot.add_cog(Clean_URL(bot))
