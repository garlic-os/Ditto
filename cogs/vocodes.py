from discord.ext import commands
from typing import Optional
import random
import discord
import requests  # TODO: replace with aiohttp
import atexit
import json

session = requests.Session()
with open("./speakers.json") as f:
    speakers = json.load(f)


def get_speaker(name: str) -> Optional[dict]:
    """
    Get a speaker's data entry from any of many names.
    You can use their formal name, their slug, or one of any provided aliases.
    All the names associated with a speaker can be found in speaker.json.
    """
    name = name.lower()
    for speaker in speakers:
        aliases = speaker.get("aliases", [])
        for i, alias in enumerate(aliases):
            aliases[i] = alias.lower()
        names = [speaker["name"].lower(), speaker["slug"]] + aliases
        if name in names:
            return speaker
    return None


class VocodesCommand(commands.Cog):
    """ Make pop culture icons say whatever you want! Powered by vo.codes. """

    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["ditto"], usage=f"speaker name; message to speak")
    async def vocodes(self, ctx, *, args):
        """ Make pop culture icons say whatever you want! """
        
        # If there are any errors in user input syntax, use this embed
        syntax_error_embed = discord.Embed(
            title = "Syntax error",
            description = "You didn't do that correctly! Try this:\n`.vocodes speaker name; your text`",
            color = 0xf57f17  # Orange
        )

        length_error_embed = discord.Embed(
            title = "Text too long",
            description = "Text must be at least 1 character and at most 280 characters long.",
            color = 0xf57f17  # Orange
        )

        player_in_guild = None
        for player in self.bot.voice_clients:
            if player.guild == ctx.guild:
                player_in_guild = player
                break

        if not ctx.author.voice or player_in_guild is None:
            await ctx.send(embed=discord.Embed(
                title = "Error",
                description = "You and I must both be in a voice channel to use this command.",
                color = 0xf57f17  # Orange
            ))
            return

        """
        Command parsing code copied from crimsoBOT.
        Copyright (c) 2019 crimso, williammck; MIT License.
        """
        user_input = args.split(";", 1)
        speaker_name = user_input.pop(0).strip().lower()

        # Parse command input into a speaker name and body of text,
        #   separated by a semicolon.
        try:
            text = user_input[0].strip()
        except IndexError:
            await ctx.send(embed=syntax_error_embed)
            return

        # Verify proper length. Must be at least 1 character and at most 280.
        if not (1 <= len(text) <= 280):
            await ctx.send(embed=length_error_embed)
            return


        speaker = get_speaker(speaker_name)

        if speaker is None:
            await ctx.send(embed=discord.Embed(
                title = "Invalid speaker name",
                color = 0xf57f17  # Orange
            ))
            return

        payload = {
            "speaker": speaker["slug"],
            "text": text
        }

        loading_embed = discord.Embed.from_dict({
            "title": "Generating sentence...",
            "description": "_" + speaker["description"] + "_",
            "color": 11225020,  # Purple
            "author": {
                "name": speaker["name"],
                "icon_url": "https://i.gifer.com/ZZ5H.gif"  # Loading spinner
            },
            "footer": {
                "text": f"Voice model quality: {speaker['voiceQuality'] * 10}%"
            },
            "thumbnail": {
                "url": f"https://vo.codes/avatars/{speaker['avatarUrl']}"  # Speaker avatar
            }
        })

        # Send a loading message
        loading_message = await ctx.send(embed=loading_embed)

        # Send a request to vo.codes for a clip of the given character saying the
        #   given text. The server will respond back with a .wav file.
        response = session.post("https://mumble.stream/speak", json=payload)

        # Once complete, edit the message to say "success" instead of "loading".
        loading_embed.title = "Generated a sentence!"
        loading_embed.set_author(name = "✅ " + speaker["name"])
        await loading_message.edit(embed=loading_embed)

        if response.status_code == 200:
            # Transform the data into a file stream.
            # Unfortunately, a BytesIO won't cut it here, because FFmpeg
            #   requires that the stream implements the fileno() method,
            #   and BytesIO does (can) not.
            # So we have to use a hacky file workaround instead.
            with open(f"/tmp/{random.randint(0, 9999999999)}", "w+b") as f:
                # Write the audio data to a temporary file.
                f.write(response.content)

                # Seek to the beginning to read it again.
                f.seek(0)

                # Stream the audio over voice chat.
                player_in_guild.play(discord.FFmpegPCMAudio(f, pipe=True, options=["-ar 48000"]))
        else:
            await ctx.send(embed=discord.Embed(
                title = "🤷‍♂️ Error",
                description = f"Something went wrong while generating the speech:\n{response.status_code} {response.reason}",
                color = 0xf44336,  # Red
                footer = "Give it a moment and try again."
            ))



def setup(bot):
    bot.add_cog(VocodesCommand(bot))

# Make sure to try to close the HTTP session when stopping the program
def on_exit():
    session.close()

atexit.register(on_exit)
