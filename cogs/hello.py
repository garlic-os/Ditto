from discord.ext import commands

class HelloCommand(commands.Cog):
    """ A command for testing """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx, *, name):
        name = name or "World"
        await ctx.send(f"Hello, {name}!")



def setup(bot):
    bot.add_cog(HelloCommand(bot))
