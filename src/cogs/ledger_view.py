import discord
from discord import app_commands
from discord.ext import commands
from typing import List

class Ledger_View(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Linking Ledger View Cog')

    async def view_budget_autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        #TODO: Hardcoded rn, load from budget
        choices = ['Social', 'Fundraising', 'Cats']
        
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices if current.lower() in choice.lower()
        ]
    
    @app_commands.command(name="select_test", description="Testing multi-select")
    @app_commands.describe(budget = "What budget do you want to view?")
    @app_commands.autocomplete(budget=view_budget_autocomplete)
    async def view_budget(self, interaction: discord.Interaction, budget: str):
        await interaction.response.send_message(f"You want to view the '{budget}' budget")

async def setup(bot):
    await bot.add_cog(Ledger_View(bot))