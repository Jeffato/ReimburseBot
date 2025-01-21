import discord
from discord import app_commands
from discord.ext import commands

from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
description = ''
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