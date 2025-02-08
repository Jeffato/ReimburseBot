import discord
from discord import app_commands
from discord.ext import commands

from datetime import datetime
from receipt import Receipt

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
        
        # Check if queue is empty

        receipt = Receipt("Cats", 
                "Helios", 
                "12.99", 
                "2025-01-01",
                "Churu for best boy", 
                datetime.now())
        
        receipt.image_url = "https://cdn.discordapp.com/attachments/1064590036466683967/1337532519674806384/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIzLTA4L3Jhd3BpeGVsX29mZmljZV8zMF9hX3N0dWRpb19zaG90X29mX2NhdF93YXZpbmdfaW1hZ2VzZnVsbF9ib2R5X182YzRmM2YyOC0wMGJjLTQzNTYtYjM3ZC05NDM0NTgwY2FmNDcucG5n.png?ex=67a8727a&is=67a720fa&hm=d83516cff1a178e85decf8218addc0e0de09f76f7f3112149c248b0a44bdb48a&"
        
        view = Request_Manager()

        embed = discord.Embed(title="Request Details", description = receipt.description)
        embed.add_field(name = "Requested By:", value = receipt.requestor, inline = False)
        embed.add_field(name = "Budget", value = receipt.category, inline = True)
        embed.add_field(name = "Amount", value = receipt.amount, inline=True)
        embed.add_field(name = "", value="", inline=False)
        embed.add_field(name = "Submitted On:", value = receipt.submit_time, inline=True)
        embed.add_field(name = "Purchased on:", value = receipt.date_purchase, inline=True)
        embed.set_image(url = receipt.image_url)
        
        # TODO: Change to actual numbers
        embed.set_footer(text= "Requests in Queue: 27",
                        icon_url= self.bot.user.avatar.url)

        await interaction.response.send_message(embed = embed, view = view, ephemeral= True)

# TODO: Update logic for each button
class Request_Manager(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Approve', style=discord.ButtonStyle.success)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Approved Request', ephemeral=True)
        self.value = True
        self.stop()
    
    @discord.ui.button(label='Edit', style=discord.ButtonStyle.primary)
    async def edit(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Opening edit menu...', ephemeral=True)
        self.value = False
        self.stop()

    @discord.ui.button(label='Reject', style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Rejected Request', ephemeral=True)
        self.value = False
        self.stop()
    
    @discord.ui.button(label='Prev', style=discord.ButtonStyle.secondary)
    async def prev_entry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Prev entry', ephemeral=True)
        self.value = False
        self.stop()

    @discord.ui.button(label='Next', style=discord.ButtonStyle.secondary)
    async def next_entry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Next entry', ephemeral=True)
        self.value = False
        self.stop()

async def setup(bot):
    await bot.add_cog(Ledger_Admin(bot))