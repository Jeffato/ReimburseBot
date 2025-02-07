import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import traceback

import os

from receipt import Receipt

class Receipt_Modal(discord.ui.Modal, title="Reimbursement Request"):
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
        label = "Purchase Date (YYYY-MM-DD)",
        style = discord.TextStyle.short,
        placeholder = "2025-04-01"
    )
    description_purchase = discord.ui.TextInput(
        label = 'Describe your purchase',
        style = discord.TextStyle.long,
        placeholder = 'Cups @ 12.99 for brolympics',
        max_length = 300
    )
    submit_time = datetime.now()
    submit_receipt = None

    async def on_submit(self, interaction: discord.Interaction):
        request = Receipt(self.category.value, 
                          self.requestor.value, 
                          self.amount_requested.value, 
                          self.date_purchase.value, 
                          self.description_purchase.value, 
                          self.submit_time)
        
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
        modal = Receipt_Modal()
        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.submit_receipt:
            await interaction.followup.send("No receipt data was submitted.", ephemeral=True)
            return
        
        await interaction.followup.send(f'Please upload receipt image (Accepted file formats: png, jpg, jpeg', ephemeral = True)

        try:
            msg = await self.bot.wait_for("message", 
                                          check = lambda msg: msg.author == interaction.user and bool(msg.attachments), 
                                          timeout=90)
            attachment = msg.attachments[0]

            # TODO: More file limits? Size limits? Check for file content?
            if attachment.content_type not in ("image/png", "image/jpeg", "image/jpg"):
                await interaction.followup.send("Invalid file format. Please upload a png, jpg, or jpeg.", ephemeral=True)
                return
            
            image_url = attachment.url

            await self.insert_receipt(modal.submit_receipt, image_url)
            await interaction.followup.send("Receipt successfully submitted for approval!", ephemeral=True)

        except TimeoutError:
            await interaction.followup.send("You didn't upload an image in time.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)

    async def insert_receipt(self, request : Receipt, image_url: str):
        table = os.getenv("ledger_table")
        print("Attempting to insert Receipt")

        async with self.bot.pg_pool.acquire() as connection:
            print("Got connection")
            # Insert the receipt into the database
            try:
                res = await connection.execute(f'''
                    INSERT INTO {table} (category, requestor, amount, date_purchase, description, submit_time, image_url)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                ''', request.category, request.requestor, request.amount, request.date_purchase, request.description, request.submit_time, image_url)
                
                print("Query result:", res)  # Check if this is reached
            
            except Exception as e:
                print(f"Error executing query: {e}") 

async def setup(bot):
    await bot.add_cog(Requests(bot))