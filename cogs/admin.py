import typing
import asyncio

from discord import User
from discord.ext import commands


class Admin(commands.Cog, name="Admin commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban")
    async def _ban(self, ctx):
        """Bans a user"""
        await ctx.channel.send("User banned.")

    @commands.command(name="purge", aliases=["pg"])
    async def _purge(self, ctx, msg_count: typing.Optional[int] = 10):
        """
        Purges <n> messages

        Purges <n> messages from the channel, n = 10 by default
        """

        try:
            if msg_count > 100:
                msg_count = 100

            await ctx.message.delete()
            deleted_msgs = await ctx.channel.purge(limit=msg_count)
            plural = "s" if len(deleted_msgs) != 1 else ""
            await ctx.channel.send(
                f"Deleted {len(deleted_msgs)} message{plural}!", delete_after=4
            )
        except Exception as e:
            await ctx.channel.send(f"Couldn't delete messages.\n`Exception: {e}`")

    @commands.command(name="purge_until", aliases=["puntil", "p_until"])
    async def _purge_until(
        self,
        ctx,
        message_id: int,
    ):
        """
        Purges messages in a channel until the given message_id

        Purges messages in a channel until the given message_id,
        but the message with the id is not deleted
        """
        try:
            message = await channel.fetch_message(message_id)

            await ctx.message.delete()
            deleted_msgs = await ctx.channel.purge(after=message)
            plural = "s" if len(deleted_msgs) != 1 else ""
            await ctx.channel.send(
                f"Deleted {len(deleted_msgs)} message{plural}!", delete_after=4
            )

        except Exception as e:
            await ctx.channel.send(f"Couldn't delete messages.\n`Exception: {e}`")
            return

    @commands.command(
        name="purge_user",
        aliases=["puser", "p_user"],
    )
    async def purge_user(
        self,
        ctx,
        user: User,
        msg_count: typing.Optional[int] = 10,
    ):
        """Purges <n> messagges of <user>"""

        def check(msg):
            return msg.author.id == user.id

        try:
            if msg_count > 100:
                msg_count = 100

            await ctx.message.delete()
            deleted_msgs = await ctx.channel.purge(limit=msg_count, check=check)
            plural = "s" if len(deleted_msgs) != 1 else ""
            await ctx.channel.send(
                f"Deleted {len(deleted_msgs)} message{plural}!", delete_after=4
            )
        except Exception as e:
            await ctx.channel.send(f"Couldn't delete messages.\n`Exception: {e}`")


def setup(bot):
    bot.add_cog(Admin(bot))
