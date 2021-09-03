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
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member.mention} for {reason}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.mention} for {reason}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        bannedMembers = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in bannedMembers:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user=user)
                await ctx.send(f"Unbanned {user.name}#{user.discriminator}")
                return

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def banlist(self, ctx):
        bannedMemberList = []
        bannedBotList = []

        banEmbed = discord.Embed(title="Banned Users", color=discord.Color.red())

        bannedMembers = await ctx.guild.bans()
        for user in bannedMembers:
            if user[1].bot == False:
                bannedMemberList.append(user[1].name + "#" + user[1].discriminator)
            else:
                bannedBotList.append(user[1].name + "#" + user[1].discriminator)

        if len(bannedBotList) <= 0:
            bannedBotList = None
        if len(bannedMemberList) <= 0:
            bannedMemberList = None

        banEmbed.add_field(name="Hoomans", value=str(bannedMemberList).replace("[", "").replace("]", "").replace("'", ""))
        banEmbed.add_field(name="Bots", value=str(bannedBotList).replace("[", "").replace("]", "").replace("'", ""))
        await ctx.send(embed=banEmbed)

    @commands.command()
    async def pingmein(self, ctx, tick: int, minhoursec):
        waitDone = False
        type = ""

        if "sec" in minhoursec:
            await asyncio.sleep(tick)
            waitDone = True
            type = "seconds"
        elif "min" in minhoursec:
            await asyncio.sleep(tick*60)
            waitDone = True
            type = "minutes"
        elif "hour" in minhoursec:
            await asyncio.sleep(tick*360)
            waitDone = True
            type = "hours"

        if waitDone == True:
            await ctx.send(f"{ctx.message.author.mention} Your time is up: It has been {tick} {type}")

        return

def setup(client):
    client.add_cog(UserUtil(client))
