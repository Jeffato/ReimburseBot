''' 
- Database for budget limits?
- Access approval queue
- embed UI element for approve, rejecting, or modifing request
- Submit to ledger database
- Export ledger database to gsheets
'''

import discord
from discord import app_commands
from discord.ext import commands

import os

class Treasurer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def is_treasurer(interaction: discord.Interaction):
        teasurer_id = int(os.getenv("BOT_ADMIN"))
        return interaction.user.id== teasurer_id

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Linking Treasurer Cog')
    
    @app_commands.command(name="check_admin", description="Checks if user id matches the bot's known admin id")
    async def check_admin(self, interaction: discord.Interaction):
        is_admin = await Treasurer.is_treasurer(interaction)
        await interaction.response.send_message(f'Admin match: {is_admin}', ephemeral = True)

    # Example restricted command
    @app_commands.command(name="ping", description="A simple ping command")
    @app_commands.check(is_treasurer)
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")

    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        else:
            # Log or handle other errors
            await interaction.response.send_message("An error occurred while processing your command.", ephemeral=True)
            print(f"An error occurred: {error}")

async def setup(bot):
    await bot.add_cog(Treasurer(bot))