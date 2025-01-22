import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import traceback

import os

class Receipt:
    category : str
    requestor : str
    amount : str
    date_purchase : str
    description : str
    submit_time : str
    
    # TODO: Input validation
    def __init__(self, category : str, requestor : str, amount : str, date_purchase : str, description : str, submit_time : str):
        self.category = category 
        self.requestor = requestor
        self.amount = amount
        self.date_purchase = date_purchase
        self.description = description 
        self.submit_time = submit_time

    def toString(self):
        return f'{self.submit_time}: {self.requestor} requested ${self.amount} from {self.category} for {self.description}'

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
    submit_time = datetime.now().strftime("%B %d, %Y %I:%M %p")
    submit_receipt = None

    async def on_submit(self, interaction: discord.Interaction):
        request = Receipt(self.category, self.requestor, self.amount_requested, self.date_purchase, self.description_purchase, self.submit_time)
        self.submit_receipt = request
        await interaction.response.send_message(f'Processing... {request.toString()}', ephemeral = True)

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
        modal = Reciept_Modal()
        await interaction.response.send_modal(modal)

        await modal.wait()

        if not modal.submit_receipt:
            await interaction.response.send_message("No receipt data was submitted.", ephemeral=True)
            return

        try:
            await self.insert_receipt(modal.submit_receipt)
            await interaction.response.send_message("Receipt successfully submitted for approval!")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

    async def insert_receipt(self, request : Receipt):
        table = os.getenv("queue_table")

        async with self.bot.pg_pool.acquire() as connection:
        # Insert the receipt into the database
            try:
                res = await connection.execute(f'''
                    INSERT INTO {table} (category, requestor, amount, date_purchase, description, submit_time)
                    VALUES ($1, $2, $3, $4, $5, $6)
                ''', (request.category, request.requestor, request.amount, request.date_purchase, request.description, request.submit_time))
                
                print("Query result:", res)  # Check if this is reached
            
            except Exception as e:
                print("Error executing query:" + e)  # Log any errors

async def setup(bot):
    await bot.add_cog(Requests(bot))