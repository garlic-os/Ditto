from discord.ext import commands
from utils import Pagination
import discord
import math
import json


def to_lower(text: str) -> str:
    return text.lower()


# Load the speakers database
with open("./speakers.json") as f:
    speaker_names = []
    for speaker in json.load(f):
        speaker_names.append(speaker["name"])
    speaker_names.sort(key=to_lower)


class ListVoicesCommand(commands.Cog):
    """ A command for listing all the voices """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["lv", "speakers"])
    async def listvoices(self, ctx):
        speaker_count = len(speaker_names)
        embeds = []
        page_count = math.ceil(speaker_count / 24)

        for i in range(page_count):
            embed = discord.Embed(
                title = f"Speakers (Page {i + 1}/{page_count})",
                footer = {
                    "text": "Powered by vo.codes",
                    "url": "https://vo.codes/"
                },
                author = {
                    "name": ctx.author.display_name,
                    "icon_url": ctx.author.avatar_url
                },
                color = 0xab47bc,
            )

            next_endpoint = min(speaker_count, (i + 1) * 24)
            for name in speaker_names[i * 24 : next_endpoint]:
                embed.add_field(name="​", value=name)

            embeds.append(embed)

        paginator = Pagination.CustomEmbedPaginator(ctx)
        paginator.add_reaction("⏪", "back")
        paginator.add_reaction("⏩", "next")
        await paginator.run(embeds)

        


def setup(bot):
    bot.add_cog(ListVoicesCommand(bot))
