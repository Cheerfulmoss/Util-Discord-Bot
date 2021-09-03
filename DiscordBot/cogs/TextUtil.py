import discord
from discord.ext import commands
import datetime


class TextUtil(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"---TextUtil Response---------------------------------------------------------------------")
        print(f"{datetime.datetime.now()}   ||   TextUtil cog loaded")
        print(f"-----------------------------------------------------------------------------------------\n")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx):
        await ctx.channel.purge()
        print(f"---Purge---------------------------------------------------------------------------------")
        print(f"{datetime.datetime.now()}   ||   Channel purged for {ctx.guild.id}")
        print(f"-----------------------------------------------------------------------------------------\n")


def setup(client):
    client.add_cog(TextUtil(client))


