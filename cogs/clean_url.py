import re
from urllib.parse import unquote

from unalix import clear_url, unshort_url
from discord.ext import commands

import libs.config as config

URL_PATTERN = re.compile(r'(https?://\S+|https?://www\.\S+|www\.\S+)')
puncts = ',.?\'"-:!'


class Clean_URL(commands.Cog, name="Clean URLs"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:# or msg.channel.id != 758645353368125461:
            return

        message = msg.content.lower()
        found_links = list(set(URL_PATTERN.findall(msg.content)))

        if not found_links:
            return

        found_links = [unquote(url) for url in found_links]     # decode the urls
        links = []

        for link in found_links:
            if link[-1] in puncts:
                    links.append(link[:-2])
            else:
                links.append(link)

        clean_links = []

        for link in links:
            try:
                tmp = unshort_url(clear_url(link))      # tries to unshort url if services like tinyurl, bitly are used
            except:
                tmp = clear_url(link)       # no url shortening services used

            if tmp == link:
                continue
            else:
                clean_links.append(tmp)

        if not len(clean_links):        # if no unclean url, do nothing
            return
    
        plural = 's' if len(clean_links) != 1 else ''
        to_send = '\n'.join(clean_links)
        await msg.channel.send(f":warning: **Foul URL{plural} detected. Cleaned URL{plural}:**\n{to_send}")


def setup(bot):
    bot.add_cog(Clean_URL(bot))