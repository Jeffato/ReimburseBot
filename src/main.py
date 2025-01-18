import discord
from discord import app_commands
from discord.ui import Modal, TextInput, View
from discord.ext import commands
from datetime import datetime
import traceback

from dotenv import load_dotenv
import os
import asyncio

import random

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
description = ''

# Intents list
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create a Bot instance
bot = commands.Bot(command_prefix='?', description=description, intents=intents)

# Event: on_ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try: 
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)!")
    except Exception as e:
        print(e)

class Request(Modal, title="Reimbursement Request"):
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

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your feedback, {self.requestor}!', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        traceback.print_exception(type(error), error, error.__traceback__)

@bot.tree.command(name="request")
async def modal(interaction: discord.Interaction):
    await interaction.response.send_modal(Request())

# Example tree commands
@bot.tree.command(name="simple_slash")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!", ephemeral=True)

@bot.tree.command(name="parrot")
@app_commands.describe(thing_to_say = "What should I say?")
async def say(interaction: discord.Interaction, thing_to_say : str):
    await interaction.response.send_message(f"{interaction.user.name} (You) said: '{thing_to_say}'")

# Example basic commands
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}')


# @bot.command()
# async def send(ctx):
#     embed_msg = discord.Embed(title="test", 
#                                description="kachow", 
#                                color=discord.Color.blue())
    
#     embed_msg.set_thumbnail(url=ctx.author.avatar)
#     embed_msg.add_field(name = "Field", value = "Value", inline = False)
#     embed_msg.set_footer(text="Footer Text", icon_url = ctx.author.avatar)
#     embed_msg.set_image(url = ctx.guild.icon)

#     await ctx.send(embed=embed_msg)

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load()
        await bot.start(DISCORD_TOKEN)
        
# # Run the bot
# bot.run(DISCORD_TOKEN)

asyncio.run(main())