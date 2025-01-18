import discord 
from discord import ui, app_commands
from discord.ext import commands
from datetime import datetime

class My_Modal(ui.Modal, title = "Example Modal"):
    answer = ui.TextInput(label = "Testing?", 
                          style = discord.TextStyle.short, 
                          placeholder = "Yes?", 
                          default = "Yes/No", 
                          required = True,
                          max_length= 3)
    
    async def on_submit(self, interaction):
        embed = discord.Embed(title = self.title,
                              description = f'**{self.answer.label}**\n{self.answer}',
                              timestamp = datetime.now(),
                              color = discord.Color.blue())
        embed.set_author(name = interaction.user, icon_url=interaction.user.avatar)

        await interaction.response.send_message(embed = embed)

class Test_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Linking Test_cog')

    @commands.command()
    async def send(self, ctx):
        embed_msg = discord.Embed(title="test", 
                                description="kachow", 
                                color=discord.Color.blue())
        
        embed_msg.set_thumbnail(url=ctx.author.avatar)
        embed_msg.add_field(name = "Field", value = "Value", inline = False)
        embed_msg.set_footer(text="Footer Text", icon_url = ctx.author.avatar)
        embed_msg.set_image(url = ctx.guild.icon)

        await ctx.send(embed=embed_msg)
    
    @app_commands.command(name="test")
    async def modal(self, interaction: discord.Interaction):
        await interaction.response.send_modal(My_Modal())

async def setup(bot):
    await bot.add_cog(Test_cog(bot))