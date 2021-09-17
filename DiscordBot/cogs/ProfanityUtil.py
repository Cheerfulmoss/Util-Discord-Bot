from discord.ext import commands
import datetime
import json
import os
import string
import re
from .GeneralFunctions.string_formatters import title_format

global bot_name


class ProfanityUtil(commands.Cog):

    def __init__(self, client):
        self.cwd = cwd = os.getcwd()
        self.client = client

        self.pList = json.load(open(f"{cwd}\\cogs\\ProfanityFiles\\BadWords.json", "r"))

    @commands.Cog.listener()
    async def on_ready(self):
        global bot_name
        bot_name = re.search('^[^#]*', str(self.client.user)).group(0)
        debug_title_ready = title_format(f"{bot_name}: ProfanityUtil Response")
        print(debug_title_ready[0])
        print(f"{datetime.datetime.now()}   ||   ProfanityUtil cog loaded")
        print(debug_title_ready[1])

    @commands.Cog.listener()
    async def on_message(self, message):
        global message_fix
        if message.author != self.client.user:
            for symbol in string.punctuation:
                message_fix = message.content.replace(symbol, "").replace(" ", "")

            server_settings = json.load(open(f"{self.cwd}\\cogs\\ServerProperties\\ServerSettings.json", "r"))

            with open(f"{self.cwd}\\cogs\\ServerProperties\\properties.json", "r") as propertiesJson:
                properties = json.load(propertiesJson)

            slur_count = properties[str(message.guild.id)]["slurcount"]
            swear_count = properties[str(message.guild.id)]["swearcount"]

            for word in self.pList["swearwords"]:
                if word in message_fix:
                    if server_settings[f"{message.guild.id}"]["SwearWords"].lower() == "true":
                        await message.delete()
                    swear_count += 1

            for word in self.pList["slurs"]:
                if word in message_fix:
                    if server_settings[f"{message.guild.id}"]["Slurs"].lower() == "true":
                        await message.delete()
                    slur_count += 1

            properties[str(message.guild.id)] = {"slurcount": slur_count, "swearcount": swear_count}
            with open(f"{self.cwd}\\cogs\\ServerProperties\\properties.json", "w") as propertiesJson:
                json.dump(properties, propertiesJson, indent=4)


def setup(client):
    client.add_cog(ProfanityUtil(client))
