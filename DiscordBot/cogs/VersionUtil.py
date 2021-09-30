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
    async def check(self, ctx, option, narrow="none"):
        narrow_list = ["true", "none"]
        if narrow.lower() not in narrow_list:
            help_embed = discord.Embed(title="Check help", colour=discord.Colour.from_rgb(26, 255, 0)) \
                .add_field(name="Explanation", value="There are 2 parameters:\n"
                                                     "The option and sub option, the option can be version, settings or"
                                                     "stats. While narrow only applies to stats and shows a percentage"
                                                     "graph of how many messages have swears or slurs in them compared"
                                                     "to total messages in the server.") \
                .add_field(name="Use", value="U!check [version / settings / stats] [true or leave blank]")
            await ctx.send(embed=help_embed)

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
            swear_setting = server_settings[f"{ctx.guild.id}"]["swearwords"].lower()
            slur_settings = server_settings[f"{ctx.guild.id}"]["slurs"].lower()
            in_depth_search = server_settings[f"{ctx.guild.id}"]["indepthsearch"].lower()
            settings_embed.add_field(name="Profanity Filter", value=f"Swear Words: {swear_setting.upper()}\n"
                                                                    f"Slurs: {slur_settings.upper()}\n"
                                                                    f"In Depth Search: {in_depth_search}")
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
                                       value=f"{round(percent, 2)}%"
                                       )

            if narrow.lower() == "true":
                bar_embed = discord.Embed(title="Percentage Graph", colour=discord.Colour.blurple()) \
                    .add_field(name=f"0% | {bar_custom} | 100%", value=f"X at {round(percent, 2)}%")
                await ctx.send(embed=bar_embed)
                return
            await ctx.send(f"0% | {bar_custom} | 100%")
            await ctx.send(embed=properties_embed)

    @check.error
    async def check_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(":scream: Missing Required Parameters\n"
                           "Format: \n"
                           f"```U!check settings```\n"
                           f"```U!check stats [True/False whether it should only be the graph]```\n"
                           f"```U!check version```"
                           , delete_after=3)
            await ctx.message.delete()


def setup(client):
    client.add_cog(VersionUtil(client))
