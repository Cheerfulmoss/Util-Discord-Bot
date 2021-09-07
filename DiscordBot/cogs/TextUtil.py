from discord.ext import commands
import datetime
import json
import os


class TextUtil(commands.Cog):

    def __init__(self, client):
        self.prohibited = json.load(open(f"{os.getcwd()}/\\cogs\\ServerProperties\\prohibit.json", "r"))["servers"]
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"---TextUtil Response---------------------------------------------------------------------")
        print(f"{datetime.datetime.now()}   ||   TextUtil cog loaded")
        print(f"-----------------------------------------------------------------------------------------\n")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=5):
        if str(ctx.guild.id) not in self.prohibited:
            await ctx.channel.purge(limit=amount + 1)
        else:
            await ctx.send("Prohibited command")
            print(f"---Clear---------------------------------------------------------------------------------")
            print(f"{datetime.datetime.now()}   ||   Channel clear attempt for {ctx.guild.id}: FAILED")
            print(f"-----------------------------------------------------------------------------------------\n")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx):
        print(self.prohibited)
        if str(ctx.guild.id) not in self.prohibited:
            await ctx.channel.purge()
            print(f"---Purge---------------------------------------------------------------------------------")
            print(f"{datetime.datetime.now()}   ||   Channel purged for {ctx.guild.id}")
            print(f"-----------------------------------------------------------------------------------------\n")
        else:
            await ctx.send("Prohibited command")
            print(f"---Purge---------------------------------------------------------------------------------")
            print(f"{datetime.datetime.now()}   ||   Channel purged attempt for {ctx.guild.id}: FAILED")
            print(f"-----------------------------------------------------------------------------------------\n")



def setup(client):
    client.add_cog(TextUtil(client))


