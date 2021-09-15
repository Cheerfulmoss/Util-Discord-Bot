import discord
from discord.ext import commands
import datetime
import os
import asyncio
import json
from dotenv import load_dotenv
import re

# ---Version-----------------------------------------------------
version = "1.7"
versionNote = "\> _ <"
# ---------------------------------------------------------------


client = commands.Bot(command_prefix="U!")
client.remove_command('help')
cwd = os.getcwd()


@client.event
async def on_ready():
    print(f"---{re.search('^[^#]*', str(client.user)).group(0)} Main--------------------------------------------------------------------------")
    print(f"{datetime.datetime.now()}   ||   {client.user} has connected to discord!")
    print(f"-----------------------------------------------------------------------------------------\n")


print(f"---Initial Load--------------------------------------------------------------------------")
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")
        print(f"{datetime.datetime.now()}   ||   {filename} loaded successfully")
print(f"-----------------------------------------------------------------------------------------\n")


@client.command()
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Please pass in all required arguments")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You do not have necessary permissions")


@client.event
async def on_disconnect():
    print(f"---{re.search('^[^#]*', str(client.user)).group(0)} Disconnect--------------------------------------------------------------------")
    print(f"{datetime.datetime.now()}   ||   {client.user} disconnected from Discord")
    print(f"-----------------------------------------------------------------------------------------")


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


@client.command(aliases=["profanitysettings"])
@commands.has_permissions(administrator=True)
async def profanity_settings(ctx, slurs, swearwords):
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


@client.command()
@commands.is_owner()
async def load(ctx, extension="all"):
    if extension == "all":
        for file_name in os.listdir("./cogs"):
            if file_name.endswith(".py"):
                client.load_extension(f"cogs.{file_name[:-3]}")
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
    for file_name in os.listdir("./cogs"):
        if file_name.endswith(".py"):
            client.unload_extension(f"cogs.{file_name[:-3]}")
            print(f"{datetime.datetime.now()}   ||   {file_name} unloaded successfully")
    await asyncio.sleep(2)
    print(f"-----------------------------------------------------------------------------------------")
    await asyncio.sleep(2)
    for file_name in os.listdir("./cogs"):
        if file_name.endswith(".py"):
            client.load_extension(f"cogs.{file_name[:-3]}")
            print(f"{datetime.datetime.now()}   ||   {file_name} loaded successfully")
    await ctx.send("Cogs reloaded")
    print(f"{datetime.datetime.now()}   ||   Cogs reloaded")
    print(f"-----------------------------------------------------------------------------------------\n")


@client.command(aliases=["help", "Help", "HELP"])
async def discord_help(ctx):
    short = ctx.author.guild_permissions
    if_admin = short.administrator
    if_manage_messages = short.manage_messages
    if_ban_members = short.ban_members
    if_kick_members = short.kick_members

    bot_name = re.search("^[^#]*", str(client.user)).group(0)
    help_embed = discord.Embed(title=f"{bot_name} help",
                               description=f"Just some info on how to use {re.search('^[^#]*', str(client.user)).group(0)}",
                               colour=discord.Colour.from_rgb(26, 255, 0)
                               )
    if if_admin:
        help_embed.add_field(name=f"Profanity Settings",
                             value=f"This command controls the settings of the profanity filter on your server.\n"
                                   f"To use:\n"
                                   f"```U!profanitysettings [True/False value for slur checks] [True/False value for swear checks]```"
                             )
    if if_admin or if_manage_messages:
        help_embed.add_field(name=f"Clear and Purge",
                             value=f"Clear and purge are both commands that delete messages. Clear allows you to "
                                   f"specify the amount of messages to delete, while purge deletes all messages in"
                                   f"that channel.\n"
                                   f"To use:\n"
                                   f"```U!clear [number of messages]```\n"
                                   f"```U!purge```"
                             )
    if if_admin or if_kick_members:
        help_embed.add_field(name=f"Kick",
                             value=f"Kick members, duh\n"
                                   f"To use:\n"
                                   f"```U!kick [members name]```"
                             )
    if if_admin or if_ban_members:
        help_embed.add_field(name=f"Ban and unban",
                             value=f"Ban and unban members, duh.\n"
                                   f"To use:\n"
                                   f"```U!ban [members name]```\n"
                                   f"```U!unban [members name + #xxxx]```"
                             )
        help_embed.add_field(name=f"Ban list",
                             value=f"Ban list, gives you a list of all banned users (including bots).\n"
                                   f"To use:\n"
                                   f"```U!banlist```"
                             )
    help_embed.add_field(name=f"Ping me in",
                         value=f"Ping me in, pings you in a specified amount of time.\n"
                               f"To use:\n"
                               f"```U!pingmein [units of time] [type: seconds, minutes, hours]```"
                         )
    help_embed.add_field(name=f"Check",
                         value=f"Check lets you check the settings or stats of the server you're in and the version of the bot.\n"
                               f"To use:\n"
                               f"```U!check settings```\n"
                               f"```U!check stats```\n"
                               f"```U!check version```"
                         )

    await ctx.send(embed=help_embed)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client.run(TOKEN)
