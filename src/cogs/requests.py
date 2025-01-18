import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import traceback

class Reciept_Modal(discord.ui.Modal, title="Reimbursement Request"):
    category = discord.ui.TextInput(
        label = "Select request Budget",
        placeholder = 'Social'
    )
    
    requestor = discord.ui.TextInput(
        label = 'Name',
        placeholder = 'Joe Shmoe'
    )

    amount_requested = discord.ui.TextInput(
        label = "Amount (USD)",
        style = discord.TextStyle.short,
        placeholder = "12.99"
    )

    date_purchase = discord.ui.TextInput(
        label = "Purchase Date (MM-DD-YYYY)",
        style = discord.TextStyle.short,
        placeholder = "04-01-2025"
    )

    description_purchase = discord.ui.TextInput(
        label = 'Describe your purchase',
        style = discord.TextStyle.long,
        placeholder = 'Cups @ 12.99 for brolympics',
        max_length = 300
    )
    
    # TODO: Make more readable date time?
    submit_time = datetime.now()

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Request submitted at {self.submit_time}', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        traceback.print_exception(type(error), error, error.__traceback__)

class Requests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Linking Requests Cog')
    
    @app_commands.command(name="request", description = "Open a form to input receipt details")
    async def modal(self, interaction: discord.Interaction):
        await interaction.response.send_modal(Reciept_Modal())

async def setup(bot):
    await bot.add_cog(Requests(bot))