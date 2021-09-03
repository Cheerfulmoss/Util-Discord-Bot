import discord
from discord.ext import commands
import datetime
import asyncio


class UserUtil(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"---UserUtil Response---------------------------------------------------------------------")
        print(f"{datetime.datetime.now()}   ||   UserUtil cog loaded")
        print(f"-----------------------------------------------------------------------------------------\n")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member.mention} for {reason}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.mention} for {reason}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        banned_members = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_members:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user=user)
                await ctx.send(f"Unbanned {user.name}#{user.discriminator}")
                return

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def banlist(self, ctx):
        banned_member_list = []
        banned_bot_list = []

        ban_embed = discord.Embed(title="Banned Users", color=discord.Color.red())

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

        ban_embed.add_field(name="Humans",
                            value=str(banned_member_list).replace("[", "").replace("]", "").replace("'", ""))
        ban_embed.add_field(name="Bots", value=str(banned_bot_list).replace("[", "").replace("]", "").replace("'", ""))
        await ctx.send(embed=ban_embed)

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


def setup(client):
    client.add_cog(UserUtil(client))
