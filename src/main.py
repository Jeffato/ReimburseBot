import discord
from discord import app_commands
from discord.ext import commands

from dotenv import load_dotenv
import os

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

# Basic Commands
@bot.tree.command(name="simple_slash")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!", ephemeral=True)

@bot.tree.command(name="parrot")
@app_commands.describe(thing_to_say = "What should I say?")
async def say(interaction: discord.Interaction, thing_to_say : str):
    await interaction.response.send_message(f"{interaction.user.name} (You) said: '{thing_to_say}'")

# Run the bot
bot.run(DISCORD_TOKEN)