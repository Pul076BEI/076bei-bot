from discord.ext import commands
from discord import File

import libs.config as config
from libs.my_feed import MyFeed

####################
# Config variables #
####################
c_prefix = config.get_config("prefix")
c_listen_channels = config.get_config("listen_channels")

####################
# String variables #
####################
s_feed_info = config.get_string("feed_info")


class Feed(commands.Cog, name="Feed commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return

        ## check if channel id is in db
        if ctx.channel.id in c_listen_channels:
            MyFeed().add_feed(ctx, ctx.attachments)

    @commands.command(name="feed")
    async def _feed(self, ctx, purpose=None, *, channel: int = None):
        """Updates via feeds"""
        if purpose is None or purpose == "url" and channel is None:
            await ctx.channel.send(
                content=f"**Feed URL:** {s_feed_info['feed_url']}\n----------\n",
                file=File("assets/rss_feed_url.png"),
            )

        elif purpose == "list" and channel is None:
            channel_names = [
                "#"
                + self.bot.get_channel(int(listen_channel)).name
                + " - "
                + str(listen_channel)
                for listen_channel in c_listen_channels
            ]
            await ctx.channel.send(
                "I'm listening for messages on:\n" + "\n".join(channel_names)
            )

        # elif purpose == "add" and channel is not None:
        #     channels = "-".join((self.listen_channels, channel))


def setup(bot):
    bot.add_cog(Feed(bot))
