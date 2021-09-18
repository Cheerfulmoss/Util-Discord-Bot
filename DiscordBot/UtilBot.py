import discord
from discord.ext import commands
from discord.ext.tasks import loop
import datetime
import os
import asyncio
import json
from dotenv import load_dotenv
import re
from cogs.GeneralFunctions.string_formatters import title_format

# Debug ------------
full_debug = True
# ------------------


client = commands.Bot(command_prefix="U!")
client.remove_command('help')
cwd = os.getcwd()
global bot_name


def NOR(a, b):
    if (a == 0) and (b == 0):
        return 1
    elif (a == 0) and (b == 1):
        return 0
    elif (a == 1) and (b == 0):
        return 0
    elif (a == 1) and (b == 1):
        return 0


def load_cogs(load_type):
    try:
        load_cog_title = title_format(f"{bot_name}: {load_type} Load")
    except:
        load_cog_title = title_format(f"UtilBot: {load_type} Load")
    print(load_cog_title[0])
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")
            print(f"{datetime.datetime.now()}   ||   {filename[:-3]} Loaded")
    print(load_cog_title[1])


def unload_cogs(load_type):
    try:
        unload_cog_title = title_format(f"{bot_name}: {load_type} Unload")
    except:
        unload_cog_title = title_format(f"UtilBot: {load_type} Unload")
    print(unload_cog_title[0])
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.unload_extension(f"cogs.{filename[:-3]}")
            print(f"{datetime.datetime.now()}   ||   {filename[:-3]} Unloaded")
    print(unload_cog_title[1])


def reload_cogs(load_type):
    try:
        reload_cog_title = title_format(f"{bot_name}: {load_type} Reload")
    except:
        reload_cog_title = title_format(f"UtilBot: {load_type} Reload")
    print(reload_cog_title[0])
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.unload_extension(f"cogs.{filename[:-3]}")
            print(f"{datetime.datetime.now()}   ||   {filename[:-3]} Unloaded")
            client.load_extension(f"cogs.{filename[:-3]}")
            print(f"{datetime.datetime.now()}   ||   {filename[:-3]} loaded")
    print(reload_cog_title[1])


@client.event
async def on_ready():
    global bot_name
    bot_name = re.search('^[^#]*', str(client.user)).group(0)
    debug_title_ready = title_format(f"{bot_name}: Main")
    print(debug_title_ready[0])
    print(f"{datetime.datetime.now()}   ||   {client.user} is ready!")
    print(debug_title_ready[1])
    if full_debug == False:
        load_cogs("Initial")


if full_debug == True:
    load_cogs("Initial")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Please pass in all required arguments")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You do not have necessary permissions")


@client.event
async def on_disconnect():
    debug_title_disconnect = title_format(f"{bot_name}: Disconnected")
    print(debug_title_disconnect[0])
    print(f"{datetime.datetime.now()}   ||   {client.user} disconnected from Discord")
    print(debug_title_disconnect[1])


@client.event
async def on_connect():
    await asyncio.sleep(5)
    debug_title_connect = title_format(f"{bot_name}: Connected")
    print(debug_title_connect[0])
    print(f"{datetime.datetime.now()}   ||   {client.user} connected to Discord")
    print(debug_title_connect[1])


@client.event
async def on_guild_join(guild):
    debug_title_join = title_format(f"{bot_name}: Added to Guild")
    print(debug_title_join[0])
    with open(f"{cwd}\\cogs\\ServerProperties\\ServerSettings.json", "r") as settingsJson:
        settings = json.load(settingsJson)

    with open(f"{cwd}\\cogs\\ServerProperties\\properties.json", "r") as propertiesJson:
        properties = json.load(propertiesJson)

    slurs = "True"
    swear_words = "False"

    swear_count = 0
    slur_count = 0
    word_count = 0

    settings[str(guild.id)] = {"slurs": slurs, "swearwords": swear_words}
    properties[str(guild.id)] = {"slurcount": slur_count, "swearcount": swear_count, "wordcount": word_count}

    with open(f"{cwd}\\cogs\\ServerProperties\\ServerSettings.json", "w") as settingsJson:
        json.dump(settings, settingsJson, indent=4)

    with open(f"{cwd}\\cogs\\ServerProperties\\properties.json", "w") as propertiesJson:
        json.dump(properties, propertiesJson, indent=4)

    print(f"{datetime.datetime.now()}   ||   {client.user} added to guild: {guild.id}")
    print(debug_title_join[1])


@client.event
async def on_guild_remove(guild):
    debug_title_remove = title_format(f"{bot_name}: Removed from Guild")
    print(debug_title_remove[0])
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
    print(debug_title_remove[1])


@loop(hours=5)
async def auto_reload():
    reload_cogs("Auto")


@client.command(aliases=["profanitysettings"])
@commands.has_permissions(administrator=True)
async def profanity_settings(ctx, slurs, swearwords):
    if NOR(slurs.lower() == "true" or slurs.lower() == "false",
           swearwords.lower() == "true" or swearwords.lower() == "false"):
        idle_embed = discord.Embed(title="Change Profanity Settings", colour=discord.Colour.from_rgb(255, 0, 0))
        idle_embed.add_field(name="Syntax:",
                             value="U!profanitysettings [True/False value for slur checks] [True/False value for swear checks]") \
            .add_field(name="Example:",
                       value="U!profanitysettings True False") \
            .add_field(name="Notes:",
                       value="The base values for this are Slurs=True and SwearWords=False.")
        await ctx.send(embed=idle_embed)
        return

    debug_title_settings = title_format(f"{bot_name}: Profanity Settings Changed")
    print(debug_title_settings[0])
    with open(f"{cwd}\\cogs\\ServerProperties\\ServerSettings.json", "r") as settingsJson:
        settings = json.load(settingsJson)

    settings[str(ctx.guild.id)] = {"Slurs": slurs, "SwearWords": swearwords}

    with open(f"{cwd}\\cogs\\ServerProperties\\ServerSettings.json", "w") as settingsJson:
        json.dump(settings, settingsJson, indent=4)
    print(f"{datetime.datetime.now()}   ||   Settings changed for {ctx.guild.id}")

    response = discord.Embed(title="Profanity Settings", color=discord.Color.from_rgb(255, 255, 0))
    response.add_field(name="Slurs:", value=slurs.upper()).add_field(name="Swear Words", value=swearwords.upper())

    await ctx.send(embed=response)
    print(debug_title_settings[1])


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
    debug_title_reload = title_format(f"{bot_name}: Reload")
    print(debug_title_reload[0])
    for file_name in os.listdir("./cogs"):
        if file_name.endswith(".py"):
            client.unload_extension(f"cogs.{file_name[:-3]}")
            print(f"{datetime.datetime.now()}   ||   {file_name} unloaded successfully")
    await asyncio.sleep(2)
    print(debug_title_reload[1])
    await asyncio.sleep(2)
    for file_name in os.listdir("./cogs"):
        if file_name.endswith(".py"):
            client.load_extension(f"cogs.{file_name[:-3]}")
            print(f"{datetime.datetime.now()}   ||   {file_name} loaded successfully")
    await ctx.send("Cogs reloaded")
    print(f"{datetime.datetime.now()}   ||   Cogs reloaded")
    print(debug_title_reload[1])


@client.command(aliases=["invite", "Invite"])
async def create_invite(ctx):
    debug_title_invite = title_format(f"{bot_name}: Invite Link")
    print(debug_title_invite[0])
    data = await client.application_info()
    link = discord.utils.oauth_url(client_id=data.id, permissions=discord.Permissions(8))

    invite_embed = discord.Embed(title=f"{bot_name} Invite", color=discord.Color.from_rgb(247, 55, 24))
    invite_embed.add_field(name="Link", value=link).add_field(name="Permissions", value="- Administrator")
    await ctx.send(embed=invite_embed)

    print(f"{datetime.datetime.now()}   ||   Invite link created in {ctx.guild.id}")
    print(debug_title_invite[1])


@client.command(aliases=["help", "Help", "HELP"])
async def discord_help(ctx):
    short = ctx.author.guild_permissions
    if_admin, if_manage_messages, if_ban_members, if_kick_members = short.administrator, short.manage_messages, short.ban_members, short.kick_members

    help_embed = discord.Embed(title=f"{bot_name} help",
                               description=f"Just some info on how to use {bot_name}",
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
                             ) \
            .add_field(name=f"Ban list",
                       value=f"Ban list, gives you a list of all banned users (including bots).\n"
                             f"To use:\n"
                             f"```U!banlist```"
                       )
    help_embed.add_field(name=f"Ping me in",
                         value=f"Ping me in, pings you in a specified amount of time.\n"
                               f"To use:\n"
                               f"```U!pingmein [units of time] [type: seconds, minutes, hours]```"
                         ) \
        .add_field(name=f"Check",
                   value=f"Check lets you check the settings or stats of the server you're in and the version of the bot.\n"
                         f"To use:\n"
                         f"```U!check settings```\n"
                         f"```U!check stats```\n"
                         f"```U!check version```"
                   )\
        .add_field(name=f"Invite",
                   value=f"Creates an invite to invite the bot to a server.\n"
                         f"To use:\n"
                         f"```U!invite```"
                   )

    await ctx.send(embed=help_embed)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

auto_reload.start()
client.run(TOKEN)
