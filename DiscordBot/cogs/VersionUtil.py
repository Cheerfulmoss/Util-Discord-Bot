import discord
from discord.ext import commands
import datetime
from DiscordBot.UtilBot import version, versionNote
import os
import json
import string


class VersionUtil(commands.Cog):

    def __init__(self, client):
        self.cwd = os.getcwd()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"---VersionUtil Response------------------------------------------------------------------")
        print(f"{datetime.datetime.now()}   ||   VersionUtil cog loaded")
        print(f"-----------------------------------------------------------------------------------------\n")

    @commands.command()
    async def check(self, ctx, *, option):

        for symbol in string.punctuation:
            option = option.replace(symbol, "").replace(" ", "").lower()

        if "version" in option:

            version_embed = discord.Embed(title="UtilBot Version")
            version_embed.add_field(name=version, value=versionNote)
            await ctx.send(embed=version_embed)

        elif "settings" in option or "setting" in option:
            server_settings = json.load(open(f"{self.cwd}\\cogs\\ServerProperties\\ServerSettings.json", "r"))

            settings_embed = discord.Embed(title="UtilBot Settings")
            swear_setting = server_settings[f"{ctx.guild.id}"]["SwearWords"].lower()
            slur_settings = server_settings[f"{ctx.guild.id}"]["Slurs"].lower()
            settings_embed.add_field(name="Profanity Filter", value=f"Swear Words: {swear_setting}\n"
                                                                    f"Slurs: {slur_settings}")
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