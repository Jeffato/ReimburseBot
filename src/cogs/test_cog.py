import discord
from discord.ext import commands

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

async def setup(bot):
    await bot.add_cog(Test_cog(bot))