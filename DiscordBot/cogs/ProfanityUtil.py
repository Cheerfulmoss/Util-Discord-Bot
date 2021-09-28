from discord.ext import commands
import datetime
import json
import os
import string
import re
from .GeneralFunctions.string_formatters import title_format

global bot_name


def in_depth_search(message: str, guild_id, word_list):
    swear_word = False
    slur = False

    server_settings = json.load(open(f"{os.getcwd()}\\cogs\\ServerProperties\\ServerSettings.json", "r"))
    with open(f"{os.getcwd()}\\cogs\\ServerProperties\\properties.json", "r") as properties_json:
        properties = json.load(properties_json)
        slur_count = properties[str(guild_id)]["slurcount"]
        swear_count = properties[str(guild_id)]["swearcount"]
        word_count = properties[str(guild_id)]["wordcount"]
    word_count += 1

    for word in word_list["swearwords"]:
        if word in message:
            if server_settings[f"{guild_id}"]["swearwords"].lower() == "true":
                swear_word = True
            swear_count += 1

    for word in word_list["slurs"]:
        if word in message:
            if server_settings[f"{guild_id}"]["slurs"].lower() == "true":
                slur = True
            slur_count += 1

    properties[str(guild_id)] = {"slurcount": slur_count, "swearcount": swear_count, "wordcount": word_count}
    with open(f"{os.getcwd()}\\cogs\\ServerProperties\\properties.json", "w") as propertiesJson:
        json.dump(properties, propertiesJson, indent=4)

    return swear_word, slur


def surface_search(message: str, guild_id, word_list):
    swear_word = False
    slur = False

    server_settings = json.load(open(f"{os.getcwd()}\\cogs\\ServerProperties\\ServerSettings.json", "r"))
    with open(f"{os.getcwd()}\\cogs\\ServerProperties\\properties.json", "r") as properties_json:
        properties = json.load(properties_json)
        slur_count = properties[str(guild_id)]["slurcount"]
        swear_count = properties[str(guild_id)]["swearcount"]
        word_count = properties[str(guild_id)]["wordcount"]
    word_count += 1

    words = str(message).split()

    for word in word_list["swearwords"]:
        if word in words:
            if server_settings[f"{guild_id}"]["swearwords"].lower() == "true":
                swear_word = True
            swear_count += 1

    for word in word_list["slurs"]:
        if word in words:
            if server_settings[f"{guild_id}"]["slurs"].lower() == "true":
                slur = True
            slur_count += 1

    properties[str(guild_id)] = {"slurcount": slur_count, "swearcount": swear_count, "wordcount": word_count}
    with open(f"{os.getcwd()}\\cogs\\ServerProperties\\properties.json", "w") as propertiesJson:
        json.dump(properties, propertiesJson, indent=4)

    return swear_word, slur


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
        if message.author != self.client.user:
            for symbol in string.punctuation:
                message_depth = message.content.replace(symbol, "").replace(" ", "")
                message_surface = message.content

            server_settings = json.load(open(f"{self.cwd}\\cogs\\ServerProperties\\ServerSettings.json", "r"))
            search_setting = server_settings[f"{message.guild.id}"]["indepthsearch"].lower()

            if search_setting.lower() == "true":
                search = in_depth_search(message=message_depth, guild_id=message.guild.id, word_list=self.pList)
            else:
                search = surface_search(message=message_surface, guild_id=message.guild.id, word_list=self.pList)
            if search[0] or search[1]:
                await message.delete()


def setup(client):
    client.add_cog(ProfanityUtil(client))
