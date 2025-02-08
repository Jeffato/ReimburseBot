import discord
from discord import app_commands
from discord.ext import commands

from receipt import Receipt
from datetime import datetime

class Ledger_Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Linking Ledger_Admin Cog')
    
    @app_commands.command(name="view_queue", description="Open pending reimbursement requests")
    async def view(self, interaction: discord.Interaction):
        # SQL query to get all (or some) of the entries in ledger with 'under-review tag' -> order by oldest to newest
        # Create array, store in list of receipts
        # Create embed to display request details w/ buttons accept, edit, reject
        pass

    @app_commands.command(name="test_embed_button", description="Testing")
    async def view_testing(self, interaction: discord.Interaction):    
        # Check if queue is empty

        receipt = Receipt("Cats", 
                "Helios", 
                "12.99", 
                "2025-01-01",
                "Churu for best boy", datetime.now())

        embed = discord.Embed(title="Request Details", description = receipt.description)
        embed.add_field(name = "Requested By:", value = receipt.requestor, inline = False)
        embed.add_field(name = "Budget", value = receipt.category, inline = True)
        embed.add_field(name="Amount", value = receipt.amount, inline=True)
        embed.add_field(name="", value="", inline=False)
        embed.add_field(name="Submitted On:", value = receipt.submit_time, inline=True)
        embed.add_field(name="Purchased on:", value = receipt.date_purchase, inline=True)
        
        # TODO: Change to actual numbers
        embed.set_footer(text= "Requests in Queue: 27",
                        icon_url= self.bot.user.avatar.url)

        await interaction.response.send_message(embed = embed, ephemeral= True)

async def setup(bot):
    await bot.add_cog(Ledger_Admin(bot))