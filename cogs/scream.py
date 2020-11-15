from discord.ext import commands
import random
import cogs.ASCII as ASCII


def chance(percent: float) -> bool:
    """ Random outcome with a <percent>% chance of being True. """
    return random.random() < percent / 100


def generate_scream() -> str:
    # Vanilla scream half the time
    if chance(50):
        return "A" * random.randint(1, 100)
    
    # One of these choices repeated 1-100 times
    body = random.choice(["A", "O"]) * random.randint(1, 100)

    # Chance to wrap the message in one of these Markdown strings
    formatter = "" if chance(50) else random.choice(["*", "**", "***"])

    # Chance to put one of these at the end of the message
    suffix = "" if chance(50) else random.choice(["H", "RGH"])

    # Example: "**AAAAAAAAAAAARGH**"
    text = formatter + body + suffix + formatter

    if chance(12.5):
        text = text.lower()

    return text


def generate_screech() -> str:
    # Vanilla screech half the time
    if chance(50):
        return "E" * random.randint(1, 100)
    
    # One of these choices repeated 1-100 times
    body = "E" * random.randint(1, 100)

    # Chance to wrap the message in one of these Markdown strings
    formatter = "" if chance(50) else random.choice(["*", "**", "***"])

    # Chance to put an "R" at the beginning of the message
    prefix = "" if chance(50) else "R"

    # Example: "**REEEEEEEEEEEEEEEEEEE**"
    text = formatter + prefix + body + formatter

    if chance(12.5):
        text = text.lower()

    return text



class ScreamCommands(commands.Cog):
    """ COMMANDS FOR SCREAMING!!! """

    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["aaa"])
    async def scream(self, ctx: commands.Context):
        """ AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA """
        await ctx.send(generate_scream())

    
    @commands.command(aliases=["eee", "ree"])
    async def screech(self, ctx: commands.Context):
        """ EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE """
        await ctx.send(generate_screech())

    @commands.command(aliases=["o"])
    async def obama(self, ctx):
            eh = ASCII.OBAMA
            payload = ""
            for x in eh:
                payload += x + "\n"
            await ctx.send(payload)

    @commands.command()
    async def boom(self, ctx):
            eh = ASCII.BOOM
            payload = ""
            for x in eh:
                payload += x + "\n"
            payload = "```" + payload + "```"
            await ctx.send(payload)

    @commands.command()
    async def color(self, ctx, *, args):
            rnd_num = random.randint(0, 5)
            if rnd_num == 1:
                usr_str_cool = '```ARM\n' + args + '\n' + '```' # ARM for orange
            elif rnd_num == 2:
                usr_str_cool = '```CSS\n' + args + '\n' + '```' # CSS for lime
            elif rnd_num == 3:
                usr_str_cool = '```HTTP\n' + args + '\n' + '```' # HTTP for yellow-ish
            elif rnd_num == 4:
                usr_str_cool = '```yaml\n' + args + '\n' + '```' # yaml for cyan
            else:
                usr_str_cool = '```fix\n' + args + '\n' + '```' # fix for yellow
            await ctx.send(usr_str_cool)


def setup(bot):
    bot.add_cog(ScreamCommands(bot))
