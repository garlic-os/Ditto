# Python library for communicating with Discord
import discord

# Extension for writing commands
from discord.ext import commands

# Other imports
import os
import json
import asyncio
import atexit

# Load settings from the .env file
from dotenv import load_dotenv
load_dotenv()


# Create an instance of the Bot class.
# Here, we tell it the character to put before chat commands,
#   the users who own the bot (us), and a couple other things.
print("Initializing...")
bot = commands.Bot(
    command_prefix = os.environ["COMMAND_PREFIX"],
    owner_ids = json.loads(os.environ["BOT_OWNERS"]),
    case_insensitive = True
)

# This will run as soon as the bot logs in. When this runs,
#   the bot is ready to take commands!
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}#{bot.user.discriminator}")
    await bot.change_presence(activity=discord.Game('Living....(O _ O)'))


@bot.event
async def on_command_error(ctx, exception):
    print(exception)

    embed = discord.Embed(
        title = "An error has occurred",
        description = str(exception),
        color = 0xf44336,  # Red
    )
    await ctx.send(embed=embed)


# Obligatory ping command
@bot.command()
async def ping(ctx):
    """ Respond with the bot's reponse time. """
    await ctx.send(f"Pong! Took **{round(bot.latency * 1000, 2)}** ms.")


# Load cogs
cogs = ["hello", "vocodes", "scream", "voice-chat", "list-voices"]
bot.load_extension("jishaku")
for cog in cogs:
    try:
        print(f"Loading cog {cog}...")
        bot.load_extension(f"cogs.{cog}")
    except Exception as e:
        print(f"Failed to load cog {cog}:", e)
print("Cogs successfully loaded")


# Once the bot is loaded, this line makes the bot connect to Discord.
# If all goes well, it will appear in the users list of whatever
#   server(s) we have put it in.
print("Logging in...")
bot.run(os.environ["DISCORD_BOT_TOKEN"])


# async def leave_voice_channels():
#     promises = []
#     for voice_client in bot.voice_clients:
#         promises.append(voice_client.disconnect())
#     await asyncio.wait(promises)

def on_exit():
    print("Exiting...")
    asyncio.run_until_complete(bot.logout())

atexit.register(on_exit)
