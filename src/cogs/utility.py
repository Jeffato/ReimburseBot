import discord
from discord import app_commands
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Linking Utility Cog')

    # Example Embed
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

    @app_commands.command(name="test_db", description="Test database connection")
    async def test_db(self, interaction: discord.Interaction):
        try:
            async with self.bot.pg_pool.acquire() as connection:
                result = await connection.fetchval('SELECT 1')
                await interaction.response.send_message(f"Database connection successful! Result: {result}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Database connection failed: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Utility(bot))