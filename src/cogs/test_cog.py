import discord
from discord import app_commands
from discord.ext import commands

class Test_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Linking Test Cog')
    
    # Example basic commands
    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Hello, {ctx.author.mention}')

    # Example tree commands
    @app_commands.command(name="parrot", description= "Silly command that repeats given input")
    @app_commands.describe(thing_to_say = "What should I say?")
    async def say(self, interaction: discord.Interaction, thing_to_say : str):
        await interaction.response.send_message(f"{interaction.user.name} (You) said: '{thing_to_say}'")

async def setup(bot):
    await bot.add_cog(Test_cog(bot))