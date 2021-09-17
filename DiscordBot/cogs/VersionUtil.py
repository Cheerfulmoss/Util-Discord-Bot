import discord
from discord.ext import commands
import datetime
import os
import json
import string
import re
import math
from .GeneralFunctions.string_formatters import title_format

global bot_name


class VersionUtil(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cwd = os.getcwd()
        self.version = json.load(open(f"{self.cwd}\\cogs\\version_info.json", "r"))["version"]
        self.version_note = json.load(open(f"{self.cwd}\\cogs\\version_info.json", "r"))["version_note"]

    @commands.Cog.listener()
    async def on_ready(self):
        global bot_name
        bot_name = re.search('^[^#]*', str(self.client.user)).group(0)
        debug_title_ready = title_format(f"{bot_name}: VersionUtil Response")
        print(debug_title_ready[0])
        print(f"{datetime.datetime.now()}   ||   VersionUtil cog loaded")
        print(debug_title_ready[1])

    @commands.command()
    async def check(self, ctx, *, option):

        global bot_name
        for symbol in string.punctuation:
            option = option.replace(symbol, "").replace(" ", "").lower()

        if "vers" in option:

            version_embed = discord.Embed(title=f"{bot_name} Version", color=discord.Colour.gold())
            version_embed.add_field(name=self.version, value=self.version_note)
            await ctx.send(embed=version_embed)

        elif "set" in option:
            server_settings = json.load(open(f"{self.cwd}\\cogs\\ServerProperties\\ServerSettings.json", "r"))

            settings_embed = discord.Embed(title=f"{bot_name} Settings", colour=discord.Colour.from_rgb(255, 255, 0))
            swear_setting = server_settings[f"{ctx.guild.id}"]["SwearWords"].lower()
            slur_settings = server_settings[f"{ctx.guild.id}"]["Slurs"].lower()
            settings_embed.add_field(name="Profanity Filter", value=f"Swear Words: {swear_setting.upper()}\n"
                                                                    f"Slurs: {slur_settings.upper()}")
            await ctx.send(embed=settings_embed)

        elif "stat" in option:
            server_properties = json.load(open(f"{self.cwd}\\cogs\\ServerProperties\\properties.json", "r"))

            properties_embed = discord.Embed(title="Server Properties", colour=discord.Colour.blurple())
            swear_count = server_properties[str(ctx.guild.id)]["swearcount"]
            slur_count = server_properties[str(ctx.guild.id)]["slurcount"]
            word_count = server_properties[str(ctx.guild.id)]["wordcount"]
            properties_embed.add_field(name="Amount of swear words said:", value=swear_count)
            properties_embed.add_field(name="Amount of slurs said:", value=slur_count)
            percent = ((slur_count + swear_count) / word_count) * 100
            bar_custom = '-' * (math.floor((percent - 1) / 4)) + 'X' + '-' * (math.floor((100 - percent) / 4))
            properties_embed.add_field(name="Percentage of words that are swears or slurs:",
                                       value=f"{round(percent, 2)}"
                                       )
            await ctx.send(embed=properties_embed,
                           content=f"Percentage of words that are swears or slurs\n"
                                   f"0% | {bar_custom} | 100%"
                           )


def setup(client):
    client.add_cog(VersionUtil(client))
