import discord
from discord.ext import commands
import datetime
import os
import asyncio
import json
from dotenv import load_dotenv

# ---Version-----------------------------------------------------
version = "1.0"
versionNote = ":p"
# ---------------------------------------------------------------


client = commands.Bot(command_prefix="U!")
cwd = os.getcwd()


@client.event
async def on_ready():
    print(f"---UtilBot Main--------------------------------------------------------------------------")
    print(f"{datetime.datetime.now()}   ||   {client.user} has connected to discord!")
    print(f"-----------------------------------------------------------------------------------------\n")


@client.event
async def on_guild_join(guild):
    print(f"---Added to Guild------------------------------------------------------------------------")
    with open(f"{cwd}\\cogs\\ServerProperties\\ServerSettings.json", "r") as settingsJson:
        settings = json.load(settingsJson)

    with open(f"{cwd}\\cogs\\ServerProperties\\properties.json", "r") as propertiesJson:
        properties = json.load(propertiesJson)

    slurs = "True"
    swear_words = "False"

    swearcount = 0
    slurcount = 0

    settings[str(guild.id)] = {"slurs": slurs, "swearwords": swear_words}
    properties[str(guild.id)] = {"slurcount": slurcount, "swearcount": swearcount}

    with open(f"{cwd}\\cogs\\ServerProperties\\ServerSettings.json", "w") as settingsJson:
        json.dump(settings, settingsJson, indent=4)

    with open(f"{cwd}\\cogs\\ServerProperties\\properties.json", "w") as propertiesJson:
        json.dump(properties, propertiesJson, indent=4)

    print(f"{datetime.datetime.now()}   ||   {client.user} added to guild: {guild.id}")
    print(f"-----------------------------------------------------------------------------------------\n")


@client.event
async def on_guild_remove(guild):
    print(f"---Removed from Guild--------------------------------------------------------------------")
    with open(f"{cwd}\\cogs\\ServerProperties\\ServerSettings.json", "r") as settingsJson:
        settings = json.load(settingsJson)

    with open(f"{cwd}\\cogs\\ServerProperties\\properties.json", "r") as propertiesJson:
        properties = json.load(propertiesJson)

    settings.pop(str(guild.id))
    properties.pop(str(guild.id))

    with open(f"{cwd}\\cogs\\ServerProperties\\ServerSettings.json", "w") as settingsJson:
        json.dump(settings, settingsJson, indent=4)

    with open(f"{cwd}\\cogs\\ServerProperties\\properties.json", "w") as propertiesJson:
        json.dump(properties, propertiesJson, indent=4)

    print(f"{datetime.datetime.now()}   ||   {client.user} removed from guild: {guild.id}")
    print(f"-----------------------------------------------------------------------------------------\n")


@client.command()
@commands.has_permissions(administrator=True)
async def profanitysettings(ctx, slurs, swearwords):
    if slurs.lower() == "true" or slurs.lower() == "false" or swearwords.lower() == "true" or slurs.lower() == "false":
        pass
    else:
        idle_embed = discord.Embed(title="Change Profanity Settings")
        idle_embed.add_field(name="Syntax:",
                             value="U!profanitysettings [True/False value for slur checks] [True/False value for swear checks]") \
            .add_field(name="Example:",
                       value="U!profanitysettings True False") \
            .add_field(name="Notes:",
                       value="The base values for this are Slurs=True and SwearWords=False.")
        await ctx.send(embed=idle_embed)
        return

    print(f"---Profanity Settings Changed------------------------------------------------------------")
    with open(f"{cwd}\\cogs\\ServerProperties\\ServerSettings.json", "r") as settingsJson:
        settings = json.load(settingsJson)

    settings[str(ctx.guild.id)] = {"Slurs": slurs, "SwearWords": swearwords}

    with open(f"{cwd}\\cogs\\ServerProperties\\ServerSettings.json", "w") as settingsJson:
        json.dump(settings, settingsJson, indent=4)
    print(f"{datetime.datetime.now()}   ||   Settings changed for {ctx.guild.id}")

    response = discord.Embed(title="Profanity Settings")
    response.add_field(name="Slurs:", value=slurs.upper()).add_field(name="Swear Words", value=swearwords.upper())

    await ctx.send(embed=response)
    print(f"-----------------------------------------------------------------------------------------\n")


print(f"---Initial Load--------------------------------------------------------------------------")
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")
        print(f"{datetime.datetime.now()}   ||   {filename} loaded successfully")
print(f"-----------------------------------------------------------------------------------------\n")


@client.command()
@commands.is_owner()
async def load(ctx, extension="all"):
    if extension == "all":
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                client.load_extension(f"cogs.{filename[:-3]}")
    else:
        client.load_extension(f"cogs.{extension}")


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")


@client.command()
@commands.is_owner()
async def reload(ctx):
    print(f"---reload--------------------------------------------------------------------------------")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.unload_extension(f"cogs.{filename[:-3]}")
            print(f"{datetime.datetime.now()}   ||   {filename} unloaded successfully")
    await asyncio.sleep(2)
    print(f"-----------------------------------------------------------------------------------------")
    await asyncio.sleep(2)
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")
            print(f"{datetime.datetime.now()}   ||   {filename} loaded successfully")
    await ctx.send("Cogs reloaded")
    print(f"{datetime.datetime.now()}   ||   Cogs reloaded")
    print(f"-----------------------------------------------------------------------------------------\n")


@client.command()
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Please pass in all required arguments")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You do not have necessary permissions")


@client.event
async def on_disconnect(ctx):
    print(f"---UtilBot Disconnect--------------------------------------------------------------------")
    print(f"{datetime.datetime.now()}   ||   {client.user} disconnected from Discord")
    print(f"-----------------------------------------------------------------------------------------")


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client.run(TOKEN)
