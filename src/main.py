import discord
from discord.ext import commands
import random

import os
from dotenv import load_dotenv

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
    print(f'We have logged in as {bot.user}')

# Command: roll
@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

# Command: test
@bot.command()
async def test(ctx, arg):
    """Test command."""
    await ctx.send(arg)

# Run the bot
bot.run(DISCORD_TOKEN)