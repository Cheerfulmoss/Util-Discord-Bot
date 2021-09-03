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

            versionEmbed = discord.Embed(title="UtilBot Version")
            versionEmbed.add_field(name=version, value=versionNote)
            await ctx.send(embed=versionEmbed)

        elif "settings" in option or "setting" in option:
            ServerSettings = json.load(open(f"{self.cwd}\\cogs\\ServerProperties\\ServerSettings.json", "r"))


            settingsEmbed = discord.Embed(title="UtilBot Settings")
            swearSetting = ServerSettings[f"{ctx.guild.id}"]["SwearWords"].lower()
            slurSettings = ServerSettings[f"{ctx.guild.id}"]["Slurs"].lower()
            settingsEmbed.add_field(name="Profanity Filter", value=f"Swear Words: {swearSetting}\n"
                                                                   f"Slurs: {slurSettings}")
            await ctx.send(embed=settingsEmbed)

        elif "stat" in option:
            ServerProperties = json.load(open(f"{self.cwd}\\cogs\\ServerProperties\\properties.json", "r"))

            propertiesEmbed = discord.Embed(title="Server Properties")
            swearcount = ServerProperties[str(ctx.guild.id)]["swearcount"]
            slurcount = ServerProperties[str(ctx.guild.id)]["slurcount"]
            propertiesEmbed.add_field(name="Amount of swear words said:", value=swearcount)
            propertiesEmbed.add_field(name="Amount of slurs said:", value=slurcount)

            await ctx.send(embed=propertiesEmbed)
            



def setup(client):
    client.add_cog(VersionUtil(client))
