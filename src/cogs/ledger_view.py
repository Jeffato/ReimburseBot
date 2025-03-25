import discord
from discord import app_commands
from discord.ext import commands
from typing import List

import os

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
    
    @app_commands.command(name="check_budget", description="View spending and allocation of a budget")
    @app_commands.describe(budget_category = "What budget do you want to view?")
    @app_commands.autocomplete(budget_category=view_budget_autocomplete)
    async def view_budget(self, interaction: discord.Interaction, budget_category: str):
        #TODO: Hardcoded rn, load from budget
        choices = ['Social', 'Fundraising', 'Cats']

        if budget_category not in choices:
            await interaction.response.send_message("Invalid Budget. Please try again and select from the list of options", ephemeral = True)
        
        budget_table = os.getenv("budget_table")
        ledger_table = os.getenv("ledger_table")

        print(f"Requesting to view '{budget_category}' budget")

        async with self.bot.pg_pool.acquire() as connection:
            print("Got connection")
            try:
                amount_query = f'''SELECT amount FROM {budget_table} WHERE category = $1'''
                record = await connection.fetchrow(amount_query, budget_category)
                budget_amount = record["amount"]

                pending_query = f'''SELECT SUM(amount) FROM {ledger_table} WHERE category = $1 AND approval_status IN ('Under-Review')'''
                pending_amount = await connection.fetchval(pending_query, budget_category) or 0

                approved_query = f'''SELECT SUM(amount) FROM {ledger_table} WHERE category = $1 AND approval_status IN ('Pending-Reimbursement', 'Approved')'''
                approved_amount = await connection.fetchval(approved_query, budget_category) or 0

                total_spending = pending_amount + approved_amount

                embed = discord.Embed(title=f"{budget_category} Budget")
                embed.add_field(name="Pending + Approved Reimbursements",
                                value=f"(${pending_amount} + ${approved_amount})",
                                inline=True)
                embed.add_field(name="", value="", inline=False)
                embed.add_field(name="Spending",
                                value=f"${total_spending}",
                                inline=True)
                embed.add_field(name="Allocated",
                                value=f"${budget_amount}",
                                inline=True)
                embed.add_field(name="Remaining",
                                value=f"${budget_amount - total_spending}",
                                inline=True)
                embed.set_footer(icon_url= self.bot.user.avatar.url)
                
                await interaction.response.send_message(embed = embed, ephemeral= True)
            
            except Exception as e:
                print(f"Error executing query: {e}") 

async def setup(bot):
    await bot.add_cog(Ledger_View(bot))