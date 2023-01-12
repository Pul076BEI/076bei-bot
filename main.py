#!/bin/env python3

import logging
import os

import discord
from discord.ext import commands


from keep_alive import keep_alive
import libs.config as config


####################
# Config variables #
####################
c_prefix = config.get_config("prefix")
c_extensions = config.get_config("cogs")
c_disabled_extensions = config.get_config("disabled_cogs")

####################
# String variables #
####################
s_status = config.get_string("status")

# Prefix
bot = commands.Bot(command_prefix=c_prefix)


# Log to a file
logger = logging.getLogger("discord")
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="a")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)


# Logging the starting point of bot into the console
@bot.event
async def on_ready():
    print(f"\n### Logged in as {bot.user}\n")
    await bot.change_presence(
        status=discord.Status.online, activity=discord.Game(name=f"{s_status}")
    )


# Removes the "command not found" error from the console
@bot.event
async def on_command_error(ctx, error):
    errors_to_skip = [commands.CommandNotFound, commands.MissingRequiredArgument]

    for error_type in errors_to_skip:
        if isinstance(error, error_type):
            return

    raise error


# Load cogs
def main():
    # Logging the unlodead cogs into the console
    if len(c_disabled_extensions) != 0:
        print("\nFollowing cogs are disabled:")
        for extension in c_disabled_extensions:
            print(f"[Disabled]\t{extension} has been disabled.")

    # Logging the loaded cogs into the console
    if len(c_extensions) != 0:
        print("\nLoading the COGS:")
        for extension in c_extensions:
            try:
                bot.load_extension(extension)
                print(f"[Success]\t{extension} loaded successfully.")
            except Exception as e:
                print(
                    f"[ERROR]\tAn error occurred while loading {extension}\n-->"
                    + str(e)
                    + "\n"
                )

    @bot.command(name="reload", aliases=["rl"])
    async def _reload(ctx):
        """Reaload the enabled cogs"""
        reloaded = []
        not_reloaded = []
        for extension in c_extensions:
            try:
                bot.reload_extension(extension)
                reloaded.append(extension)
            except Exception as e:
                not_reloaded.append(extension)
                print(
                    f"[ERROR]\tAn error occurred while reloading {extension}\n-->"
                    + str(e)
                    + "\n"
                )

        if not len(not_reloaded):
            await ctx.channel.send(f"**[Success]**\tAll cogs reloaded successfully.")
        else:
            not_reloaded_cogs = "\n".join(not_reloaded)
            await ctx.channel.send(
                f"**[ERROR]**\t{len(not_reloaded)} cog(s) could not be reloaded:\n{not_reloaded_cogs}"
            )


if __name__ == "__main__":
    main()

try:
    keep_alive()
    bot.run(os.environ["BOT_TOKEN"])
except discord.errors.HTTPException as e:
    print(f"Rate limited! Try again later.\n\n{e}")
    exit(1)
