import discord
from discord.ext import commands

class VoiceChatCommands(commands.Cog):
    """ Commands for managing the bot for voice channels. """

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            await voice_channel.connect()
        else:
            await ctx.send(embed=discord.Embed(
            title = "Error",
            description = "You must be in a voice channel to use this command.",
            color = 0xf57f17  # Orange
        ))


    @commands.command()
    async def leave(self, ctx):
        player_in_guild = None
        for player in self.bot.voice_clients:
            if player.guild == ctx.guild:
                player_in_guild = player
                break

        if player_in_guild is None:
            await ctx.send(embed=discord.Embed(
                title = "Error",
                description = "Not in a voice channel right now!",
                color = 0xf57f17  # Orange
            ))
        else:
            await player_in_guild.disconnect()


def setup(bot):
    bot.add_cog(VoiceChatCommands(bot))
