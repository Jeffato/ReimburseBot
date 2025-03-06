import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import traceback

from receipt import Receipt

class Receipt_Modal(discord.ui.Modal, title="Reimbursement Request"):
    category = discord.ui.TextInput(
        label = "Select request Budget",
        placeholder = 'Social',
        default = ""
    )
    requestor = discord.ui.TextInput(
        label = 'Name',
        placeholder = 'Joe Shmoe',
        default = ""
    )
    amount_requested = discord.ui.TextInput(
        label = "Amount (USD)",
        style = discord.TextStyle.short,
        placeholder = "12.99",
        default = ""
    )
    date_purchase = discord.ui.TextInput(
        label = "Purchase Date (YYYY-MM-DD)",
        style = discord.TextStyle.short,
        placeholder = "2025-04-01",
        default = ""
    )
    description_purchase = discord.ui.TextInput(
        label = 'Describe your purchase',
        style = discord.TextStyle.long,
        placeholder = 'Cups @ 12.99 for brolympics',
        max_length = 300,
        default = ""
    )

    def __init__(self, receipt: Receipt = None):
        super().__init__()
        
        if receipt:
            self.category.default = receipt.category
            self.requestor.default = receipt.requestor
            self.amount_requested.default = str(receipt.amount)  
            self.date_purchase.default = str(receipt.date_purchase)
            self.description_purchase.default = receipt.description
            self.submit_time = receipt.submit_time
            self.submit_receipt = receipt
        
        else:
            self.submit_time = datetime.now()
            self.receipt_id = None 
            self.submit_receipt = None

    async def on_submit(self, interaction: discord.Interaction):
        request = Receipt(self.category.value, 
                          self.requestor.value, 
                          self.amount_requested.value, 
                          self.date_purchase.value, 
                          self.description_purchase.value, 
                          self.submit_time)
        
        if self.submit_receipt:
            request.id = self.submit_receipt.id
            request.image_url = self.submit_receipt.image_url
        
        self.submit_receipt = request
        await interaction.response.send_message(f'Processing... {request.toString()}', ephemeral = True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)