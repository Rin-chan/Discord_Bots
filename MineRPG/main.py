# Base imports
import os

# Discord imports
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Other files
from database import database
from exploring import main as exploring



# Start up Discord
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='M', intents=intents)

# When main.py is first runned
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="adv", help="Go on an adventure")
async def go_adventure(ctx):
    await exploring.go_adventure(ctx)



bot.run(TOKEN)