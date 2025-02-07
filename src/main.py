import discord
from discord import app_commands
from discord.ext import commands

from dotenv import load_dotenv
import os
import asyncio

import asyncpg

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
description = ''
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create a Bot instance
bot = commands.Bot(command_prefix='?', description=description, intents=intents)

# DB Stuff
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

async def create_db_pool():
    bot.pg_pool = await asyncpg.create_pool(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    
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
    dir = os.path.join(os.getcwd(), "src/cogs")
    
    for filename in os.listdir(dir):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load()
        await create_db_pool()  
        await bot.start(DISCORD_TOKEN)
        
# # Run the bot
# bot.run(DISCORD_TOKEN)

asyncio.run(main())