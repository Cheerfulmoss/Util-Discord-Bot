import discord
from discord.ext import commands
import datetime
import asyncio
import re
from .GeneralFunctions.string_formatters import title_format

global bot_name


class UserUtil(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        global bot_name
        bot_name = re.search('^[^#]*', str(self.client.user)).group(0)
        debug_title_ready = title_format(f"{bot_name}: UserUtil Response")
        print(debug_title_ready[0])
        print(f"{datetime.datetime.now()}   ||   UserUtil cog loaded")
        print(debug_title_ready[1])

    @commands.command()
    @commands.has_permissions(administrator=True, kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member.mention} for {reason}")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":no_entry: Missing Permissions", delete_after=3)
            await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(":scream: Missing Required Parameters", delete_after=3)
            await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(administrator=True, ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.mention} for {reason}")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":no_entry: Missing Permissions", delete_after=3)
            await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(":scream: Missing Required Parameters", delete_after=3)
            await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(administrator=True, ban_members=True)
    async def unban(self, ctx, *, member):
        banned_members = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_members:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user=user)
                await ctx.send(f"Unbanned {user.name}#{user.discriminator}")
                return

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":no_entry: Missing Permissions", delete_after=3)
            await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(":scream: Missing Required Parameters", delete_after=3)
            await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(administrator=True, ban_members=True)
    async def banlist(self, ctx):
        banned_member_list = []
        banned_bot_list = []

        banned_members = await ctx.guild.bans()
        for user in banned_members:
            if not user[1].bot:
                banned_member_list.append(user[1].name + "#" + user[1].discriminator)
            else:
                banned_bot_list.append(user[1].name + "#" + user[1].discriminator)

        if len(banned_bot_list) <= 0:
            banned_bot_list = None
        if len(banned_member_list) <= 0:
            banned_member_list = None

        ban_embed = discord.Embed(title="Banned Users", color=discord.Color.red())
        ban_embed.add_field(name="Humans",
                            value=str(banned_member_list).replace("[", "").replace("]", "").replace("'", ""), )
        ban_embed.add_field(name="Bots", value=str(banned_bot_list).replace("[", "").replace("]", "").replace("'", ""))
        await ctx.send(embed=ban_embed)

    @banlist.error
    async def banlist_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":no_entry: Missing Permissions", delete_after=3)
            await ctx.message.delete()

    @commands.command()
    async def pingmein(self, ctx, tick: int, time_unit):
        wait_done = False
        time_unit_type = ""

        if "sec" in time_unit:
            await asyncio.sleep(tick)
            wait_done = True
            time_unit_type = "seconds"
        elif "min" in time_unit:
            await asyncio.sleep(tick * 60)
            wait_done = True
            time_unit_type = "minutes"
        elif "hour" in time_unit:
            await asyncio.sleep(tick * 360)
            wait_done = True
            time_unit_type = "hours"

        if wait_done:
            await ctx.send(f"{ctx.message.author.mention} Your time is up: It has been {tick} {time_unit_type}")

        return

    @pingmein.error
    async def pingmein_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(":scream: Missing Required Parameters", delete_after=3)
            await ctx.message.delete()


def setup(client):
    client.add_cog(UserUtil(client))
