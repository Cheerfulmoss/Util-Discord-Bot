from discord.ext import commands
import datetime
import json
import os
import re
from .GeneralFunctions.string_formatters import title_format

global bot_name


class TextUtil(commands.Cog):

    def __init__(self, client):
        self.prohibited = json.load(open(f"{os.getcwd()}/\\cogs\\ServerProperties\\prohibit.json", "r"))["servers"]
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        global bot_name
        bot_name = re.search('^[^#]*', str(self.client.user)).group(0)
        debug_title_ready = title_format(f"{bot_name}: TextUtil Response")
        print(debug_title_ready[0])
        print(f"{datetime.datetime.now()}   ||   TextUtil cog loaded")
        print(debug_title_ready[1])

    @commands.command()
    @commands.has_permissions(administrator=True, manage_messages=True)
    async def clear(self, ctx, amount=5):
        if str(ctx.guild.id) not in self.prohibited:
            await ctx.channel.purge(limit=amount + 1)
        else:
            await ctx.send("Prohibited command")
            debug_title_clear_prohibited = title_format(f"{bot_name}: Prohibited Command - Clear")
            print(debug_title_clear_prohibited[0])
            print(f"{datetime.datetime.now()}   ||   Channel clear attempt for {ctx.guild.id}: FAILED")
            print(debug_title_clear_prohibited[1])

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":no_entry: Missing Permissions", delete_after=3)
            await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(administrator=True, manage_messages=True)
    async def purge(self, ctx):
        if str(ctx.guild.id) not in self.prohibited:
            await ctx.channel.purge()
            debug_title_purge = title_format(f"{bot_name}: Purge")
            print(debug_title_purge[0])
            print(f"{datetime.datetime.now()}   ||   Channel purged for {ctx.guild.id}")
            print(debug_title_purge[1])
        else:
            await ctx.send("Prohibited command")
            debug_title_purge_prohibited = title_format(f"{bot_name}: Prohibited Command - PURGE")
            print(debug_title_purge_prohibited[0])
            print(f"{datetime.datetime.now()}   ||   Channel purged attempt for {ctx.guild.id}: FAILED")
            print(debug_title_purge_prohibited[1])

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":no_entry: Missing Permissions", delete_after=3)
            await ctx.message.delete()

def setup(client):
    client.add_cog(TextUtil(client))
