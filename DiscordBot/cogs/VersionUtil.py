import discord
from discord.ext import commands
import datetime
from DiscordBot.UtilBot import version, versionNote
import os
import json
import string
import re


class VersionUtil(commands.Cog):

    def __init__(self, client):
        self.cwd = os.getcwd()
        self.bot_name = re.search('^[^#]*', str(client.user)).group(0)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"---VersionUtil Response------------------------------------------------------------------")
        print(f"{datetime.datetime.now()}   ||   VersionUtil cog loaded")
        print(f"-----------------------------------------------------------------------------------------\n")

    @commands.command()
    async def check(self, ctx, *, option):

        for symbol in string.punctuation:
            option = option.replace(symbol, "").replace(" ", "").lower()

        if "vers" in option:

            version_embed = discord.Embed(title=f"{self.bot_name} Version")
            version_embed.add_field(name=version, value=versionNote)
            await ctx.send(embed=version_embed)

        elif "set" in option:
            server_settings = json.load(open(f"{self.cwd}\\cogs\\ServerProperties\\ServerSettings.json", "r"))

            settings_embed = discord.Embed(title=f"{self.bot_name} Settings")
            swear_setting = server_settings[f"{ctx.guild.id}"]["swearwords"].lower()
            slur_settings = server_settings[f"{ctx.guild.id}"]["slurs"].lower()
            settings_embed.add_field(name="Profanity Filter", value=f"Swear Words: {swear_setting.upper()}\n"
                                                                    f"Slurs: {slur_settings.upper()}")
            await ctx.send(embed=settings_embed)

        elif "stat" in option:
            server_properties = json.load(open(f"{self.cwd}\\cogs\\ServerProperties\\properties.json", "r"))

            properties_embed = discord.Embed(title="Server Properties")
            swear_count = server_properties[str(ctx.guild.id)]["swearcount"]
            slur_count = server_properties[str(ctx.guild.id)]["slurcount"]
            properties_embed.add_field(name="Amount of swear words said:", value=swear_count)
            properties_embed.add_field(name="Amount of slurs said:", value=slur_count)

            await ctx.send(embed=properties_embed)


def setup(client):
    client.add_cog(VersionUtil(client))
