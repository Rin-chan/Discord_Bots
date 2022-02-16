import os
import random
import time

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='R')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

''' When a new member joins the server
@bot.event
async def on_member_join(member):
    return
'''

''' Read message without prefix
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
'''


# Russian Roulette
playersRoulette = []
ongoingRoulette = False

@bot.command(name="startroulette", help="Start Russian Roulette")
async def russian_roulette(ctx):
    global ongoingRoulette

    if ongoingRoulette:
        await ctx.send("There is an ongoing roulette. Please wait for the current game to end.")
        return

    if len(playersRoulette) < 2:
        await ctx.send("Not enough players to start Russian roulette")
        return

    ongoingRoulette = True

    await ctx.send("Welcome to russian roulette.")
    await ctx.send("If you wanted to leave, it is too late.")
    await ctx.send("Now let's start the game.")

    for player in playersRoulette:
        await ctx.send(f"{player} picks up the gun.")
        await time.sleep(5)

        if random.randint(0, 6) == 0:
            playersRoulette.remove(player)
            await ctx.send(f"{player} has died.")

        if len(playersRoulette) == 1:
            await ctx.send(f"{playersRoulette[0]} has survived. At the cost of your friends.")
            playersRoulette.clear()
            return

        await ctx.send("Moving on")

@bot.command(name="joinroulette", help="Join Russian Roulette")
async def join_roulette(ctx):
    if ongoingRoulette:
        await ctx.send("There is an ongoing game.")
        return

    if playersRoulette.__contains__(ctx.author.name):
        await ctx.send(f"{ctx.author.name} have already joined the queue.")
        return
    playersRoulette.append(ctx.author.name)
    await ctx.send(f"{ctx.author.name} has joined the queue.")

@bot.command(name="leaveroulette", help="Leave Russian Roulette")
async def leave_roulette(ctx):
    if ongoingRoulette:
        await ctx.send("There is an ongoing game.")
        return

    if playersRoulette.__contains__(ctx.author.name) == False:
        await ctx.send(f"{ctx.author.name} is not in the queue.")
        return
    playersRoulette.remove(ctx.author.name)
    await ctx.send(f"{ctx.author.name} has left the queue.")

# Scissors Paper Rock
@bot.command(name="spr", help="Play Scissors Paper Rock (1: Scissors, 2: Paper, 3: Rock)")
async def scissors_paper_rock(ctx, choice):
    spr_BotNo = random.randint(1,3)
    choice = int(choice)

    if choice == 1:
        spr_player = "Scissors"
    elif choice == 2:
        spr_player = "Paper"
    elif choice == 3:
        spr_player = "rock"
    else:
        await ctx.send("Please choose a valid number")
        return

    if spr_BotNo == choice:
        await ctx.send(f"Both of you chose {spr_player}")
    elif (spr_BotNo == 3) and (choice == 1):
        await ctx.send("You chose scissors and the bot chose rock. You lose.")
    elif (spr_BotNo == 2) and (choice == 1):
        await ctx.send("You chose scissors and the bot chose paper. You win.")
    elif (spr_BotNo == 3) and (choice == 2):
        await ctx.send("You chose paper and the bot chose rock. You win.")
    elif (spr_BotNo == 1) and (choice == 2):
        await ctx.send("You chose paper and the bot chose scissors. You lose.")
    elif (spr_BotNo == 2) and (choice == 3):
        await ctx.send("You chose rock and the bot chose paper. You lose")
    elif (spr_BotNo == 1) and (choice == 3):
        await ctx.send("You chose rock and the bot chose scissors. You win.")
    else:
        await ctx.send(f"Something went wrong.")

bot.run(TOKEN)