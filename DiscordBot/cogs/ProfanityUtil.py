import discord
from discord.ext import commands, tasks
import datetime
import json
import os
import string


class ProfanityUtil(commands.Cog):

    def __init__(self, client):
        self.cwd = cwd = os.getcwd()
        self.client = client

        profanityList = open(f"{cwd}\\cogs\\ProfanityFiles\\BadWords.json", "r")
        self.pList = json.load(profanityList)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"---ProfanityUtil Response----------------------------------------------------------------")
        print(f"{datetime.datetime.now()}   ||   ProfanityUtil cog loaded")
        print(f"-----------------------------------------------------------------------------------------\n")


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.client.user:
            for symbol in string.punctuation:
                messageFix = message.content.replace(symbol, "").replace(" ", "")

            ServerSettings = json.load(open(f"{self.cwd}\\cogs\\ServerProperties\\ServerSettings.json", "r"))

            with open(f"{self.cwd}\\cogs\\ServerProperties\\properties.json", "r") as propertiesJson:
                properties = json.load(propertiesJson)

            slurcount = properties[str(message.guild.id)]["slurcount"]
            swearcount = properties[str(message.guild.id)]["swearcount"]


            for word in self.pList["swearwords"]:
                if word in messageFix:
                    if ServerSettings[f"{message.guild.id}"]["swearwords"].lower() == "true":
                        await message.delete()
                    swearcount += 1



            for word in self.pList["slurs"]:
                if word in messageFix:
                    if ServerSettings[f"{message.guild.id}"]["slurs"].lower() == "true":
                        await message.delete()
                    slurcount += 1

            properties[str(message.guild.id)] = {"slurcount": slurcount, "swearcount": swearcount}
            with open(f"{self.cwd}\\cogs\\ServerProperties\\properties.json", "w") as propertiesJson:
                json.dump(properties, propertiesJson, indent=4)

def setup(client):
    client.add_cog(ProfanityUtil(client))

