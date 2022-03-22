import os
import random
import time
from discord import message

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

# Sudoku
ongoingSudoku = False
sudokuBoard = (f"```" + "\n" + # Length = 3 + 2
                    "  || A | B | C || D | E | F || G | H | I ||" + "\n" + # Length = 43 + 2
                    "  =========================================" + "\n" +
                    "1 ||   |   |   ||   |   |   ||   |   |   ||" + "\n" +
                    "  ||---|---|---||---|---|---||---|---|---||" + "\n" +
                    "2 ||   |   |   ||   |   |   ||   |   |   ||" + "\n" +
                    "  ||---|---|---||---|---|---||---|---|---||" + "\n" +
                    "3 ||   |   |   ||   |   |   ||   |   |   ||" + "\n" +
                    "  ||===|===|===||===|===|===||===|===|===||" + "\n" +
                    "4 ||   |   |   ||   |   |   ||   |   |   ||" + "\n" +
                    "  ||---|---|---||---|---|---||---|---|---||" + "\n" +
                    "5 ||   |   |   ||   |   |   ||   |   |   ||" + "\n" +
                    "  ||---|---|---||---|---|---||---|---|---||" + "\n" +
                    "6 ||   |   |   ||   |   |   ||   |   |   ||" + "\n" +
                    "  ||===|===|===||===|===|===||===|===|===||" + "\n" +
                    "7 ||   |   |   ||   |   |   ||   |   |   ||" + "\n" +
                    "  ||---|---|---||---|---|---||---|---|---||" + "\n" +
                    "8 ||   |   |   ||   |   |   ||   |   |   ||" + "\n" +
                    "  ||---|---|---||---|---|---||---|---|---||" + "\n" +
                    "9 ||   |   |   ||   |   |   ||   |   |   ||" + "\n" +
                    "  =========================================" + "\n" +
                    "```")
ongoingSudokuBoard = ""

@bot.command(name="playsudoku", help="Play Sudoku")
async def sudoku(ctx):
    global ongoingSudoku
    global ongoingSudokuBoard
    
    if ongoingSudoku:
        await ctx.send(f"There is a game of sudoku running.")
        return

    ongoingSudoku = True
    ongoingSudokuBoard = sudokuBoard
    
    while True:
        doNotReset = True
        sudoku_Solution = [0, 0, 0, 0, 0, 0, 0, 0, 0, #1
                       0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, #4
                       0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, #7
                       0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0,81):
            column = i%9
            row = i//9
            alrExistRand = []
            boxColumn = column//3
            boxRow = row//3

            while True:
                exist = False

                while True:
                    rand = random.randint(1,9)
                    try:
                        alrExistRand.index(rand)
                    except:
                        break

                # Exist in column
                for j in range(0,9):
                    if sudoku_Solution[j*9+column] == rand:
                        exist = True
                        alrExistRand.append(rand)
                        break

                # Exist in row
                for j in range(0,9):
                    if exist:
                        break

                    if sudoku_Solution[row*9+j] == rand:
                        exist = True
                        alrExistRand.append(rand)
                        break

                # Exist in box
                for j in range(0,9):
                    if exist:
                        break

                    # Row 1 of box
                    if j < 3:
                        if sudoku_Solution[boxRow*27+boxColumn*3+j] == rand:
                            exist = True
                            alrExistRand.append(rand)
                            break

                    # Row 2 of box
                    elif j < 6:
                        if sudoku_Solution[boxRow*27+boxColumn*3+j+6] == rand:
                            exist = True
                            alrExistRand.append(rand)
                            break

                    # Row 3 of box
                    else:
                        if sudoku_Solution[boxRow*27+boxColumn*3+j+12] == rand:
                            exist = True
                            alrExistRand.append(rand)
                            break

                if exist == False:
                    sudoku_Solution[i] = rand
                    break
                elif len(alrExistRand) == 9:
                    doNotReset = False
                    break

        if doNotReset:
            break
            
    # Easy Difficulty
    alrExistRand = []
    filledInByRand = []
    userAnswer = [0, 0, 0, 0, 0, 0, 0, 0, 0, #1
                0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, #4
                0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, #7
                0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0]
    starting = 93
    for i in range(0,78):
        row = 0
        column = 0

        while True:
            rand = random.randint(0,80)
            try:
                alrExistRand.index(rand)
            except:
                alrExistRand.append(rand)
                break
            
        if rand < 9:
            row = 0
        elif rand < 18:
            row = 88
        elif rand < 27:
            row = 176
        elif rand < 36:
            row = 264
        elif rand < 45:
            row = 352
        elif rand < 54:
            row = 440
        elif rand < 63:
            row = 528
        elif rand < 72:
            row = 616
        else:
            row = 704

        colRand = rand%9
        if colRand == 0:
            column = 4
        elif colRand == 1:
            column = 8
        elif colRand == 2:
            column = 12
        elif colRand == 3:
            column = 17
        elif colRand == 4:
            column = 21
        elif colRand == 5:
            column = 25
        elif colRand == 6:
            column = 30
        elif colRand == 7:
            column = 34
        elif colRand == 8:
            column = 38
            
        userAnswer.pop(rand)
        userAnswer.insert(rand, sudoku_Solution[rand])
        filledInByRand.append(row+column)
        ongoingSudokuBoard = ongoingSudokuBoard[:(starting+row+column)] + str(sudoku_Solution[rand]) + ongoingSudokuBoard[(starting+row+column)+1:]
        
    print(str(sudoku_Solution))
    soduku_game = await ctx.send(ongoingSudokuBoard)
    
    @bot.command(name="sudoku", help="Choose sudoku with area code and value (Eg. Rsudoku A1 3)")
    async def soduku_choice(ctx, choice, value):
        global ongoingSudokuBoard
        starting = 93
        row = 0
        column = 0
        ansCol = 0
        ansRow = 0

        if ongoingSudoku == False:
            await ctx.send(f"There is no game of sudoku running.")
            return
        
        try:
            if choice[0] == "A":
                ansCol = 0
                column = 4
            elif choice[0] == "B":
                ansCol = 1
                column = 8
            elif choice[0] == "C":
                ansCol = 2
                column = 12
            elif choice[0] == "D":
                ansCol = 3
                column = 17
            elif choice[0] == "E":
                ansCol = 4
                column = 21
            elif choice[0] == "F":
                ansCol = 5
                column = 25
            elif choice[0] == "G":
                ansCol = 6
                column = 30
            elif choice[0] == "H":
                ansCol = 7
                column = 34
            elif choice[0] == "I":
                ansCol = 8
                column = 38
            else:
                await ctx.send(f"Invalid input.")
                return
        except:
            await ctx.send(f"Invalid input.")
            return

        try:
            if choice[1] == "1":
                ansRow = 0
                row = 0
            elif choice[1] == "2":
                ansRow = 1
                row = 88
            elif choice[1] == "3":
                ansRow = 2
                row = 176
            elif choice[1] == "4":
                ansRow = 3
                row = 264
            elif choice[1] == "5":
                ansRow = 4
                row = 352
            elif choice[1] == "6":
                ansRow = 5
                row = 440
            elif choice[1] == "7":
                ansRow = 6
                row = 528
            elif choice[1] == "8":
                ansRow = 7
                row = 616
            elif choice[1] == "9":
                ansRow = 8
                row = 704
            else:
                await ctx.send(f"Invalid input.")
                return
        except:
            await ctx.send(f"Invalid input.")
            return

        try:
            filledInByRand.index(row+column)
            await ctx.send(f"You cannot fill in one that has been filled by default.")
            return
        except:
            pass

        try:
            int(value)
        except:
            await ctx.send(f"Invalid input.")
            return

        userAnswer.pop(ansRow*9+ansCol)
        userAnswer.insert(ansRow*9+ansCol, int(value))
        ongoingSudokuBoard = ongoingSudokuBoard[:(starting+row+column)] + value + ongoingSudokuBoard[(starting+row+column)+1:]
        await soduku_game.edit(content=ongoingSudokuBoard)

    @bot.command(name="checksudoku", help="Check if your answer is correct. (You will not be able to change your answers afterward)")
    async def soduku_check(ctx):
        global ongoingSudoku
        
        if ongoingSudoku == False:
            await ctx.send(f"There is no game of sudoku running.")
            return

        print(str(userAnswer))
        print(str(sudoku_Solution))
        if userAnswer == sudoku_Solution:
            await ctx.send(f"It is correct. Congratulations.")
        else:
            await ctx.send(f"It is incorrect. Try again next time.")

        ongoingSudoku = False

''' Removed due to discord limitation
# Snake Game
snakeBoard = ""
whiteCharSnake = "⬜"
blackCharSnake = "⬛"
appleCharSnake = "🍎"
ongoingSnakeGame = False
numberOfTiles = 12
eachRow = numberOfTiles+1
timePerMove = 1
movement = 1
apple = 0
lengthOfSnake = 1

@bot.command(name="snake", help="Start a game of snake (Not fully working)")
async def snakeGame(ctx):
    global ongoingSnakeGame
    global movement
    global apple
    global snakeBoard
    global lengthOfSnake

    if ongoingSnakeGame:
        await ctx.send("There is an ongoing game of snake.")
        return

    ongoingSnakeGame = True
    movement = 1
        
    # Creating starting board
    rowChosen = eachRow * 5
    columnChosen = 3
    positionOfSnake = rowChosen+columnChosen

    while True:
        apple = random.randint(1, (eachRow*numberOfTiles))
        if apple == (rowChosen*columnChosen):
            continue
        else:
            break

    snakeBoard = (whiteCharSnake * numberOfTiles + "\n") * numberOfTiles

    snake_game = await ctx.send(snakeBoard)
    for emoji in ('🔼', '🔽', '◀', '▶'):
        await snake_game.add_reaction(emoji)

    snakeBoard = snakeBoard[:apple] + appleCharSnake +  snakeBoard[(apple):-1]
    snakeBoard = snakeBoard[:positionOfSnake] + blackCharSnake + snakeBoard[(positionOfSnake+1):-1]
    snakeBoard = snakeBoard.replace("\n", "")

    newboard = ""
    currentRow = 0
    endOfRow = numberOfTiles

    while True:
        newboard += snakeBoard[currentRow:endOfRow] + "\n"
        currentRow = endOfRow
        endOfRow = currentRow + numberOfTiles
        if currentRow == (eachRow*numberOfTiles):
            break

    snakeBoard = newboard
    await snake_game.edit(content=snakeBoard)
    
    # Detect user's choice
    @bot.event
    async def on_reaction_add(reaction, user):
        global movement
        if user != bot.user:
            if str(reaction.emoji) == "🔼":
                await snake_game.remove_reaction("🔼", user)
                movement = -eachRow
            if str(reaction.emoji) == "🔽":
                await snake_game.remove_reaction("🔽", user)
                movement = eachRow
            if str(reaction.emoji) == "◀":
                await snake_game.remove_reaction("◀", user)
                movement = -1
            if str(reaction.emoji) == "▶":
                await snake_game.remove_reaction("▶", user)
                movement = 1

    # Snake moving
    while True:
        time.sleep(timePerMove)

        snakeBoard = (whiteCharSnake * numberOfTiles + "\n") * numberOfTiles
        snakeBoard = snakeBoard[:apple] + appleCharSnake +  snakeBoard[(apple):-1]

        if movement == -1 or movement == 1:
            snakeBoard = snakeBoard[:positionOfSnake] + (lengthOfSnake*blackCharSnake) + snakeBoard[(positionOfSnake+1):-1]
        else:
            count = 0
            while count < lengthOfSnake:
                if movement == eachRow:
                    snakeBoard = snakeBoard[:positionOfSnake-eachRow-(eachRow*count)] + (blackCharSnake) + snakeBoard[(positionOfSnake-eachRow-(eachRow*count)+1):-1]
                else:
                    snakeBoard = snakeBoard[:positionOfSnake+eachRow+(eachRow*count)] + (blackCharSnake) + snakeBoard[(positionOfSnake+eachRow+(eachRow*count)+1):-1]
                count += 1

        snakeBoard = snakeBoard.replace("\n", "")

        if positionOfSnake == apple:
            while True:
                apple = random.randint(1, (eachRow*numberOfTiles))
                if apple == positionOfSnake:
                    continue
                else:
                    lengthOfSnake += 1
                    break

        positionOfSnake += movement

        newboard = ""
        currentRow = 0
        endOfRow = numberOfTiles

        while True:
            newboard += snakeBoard[currentRow:endOfRow] + "\n"
            currentRow = endOfRow
            endOfRow = currentRow + numberOfTiles
            if currentRow == (numberOfTiles*numberOfTiles):
                break

        snakeBoard = newboard
        
        if movement == 1:
            if (positionOfSnake+movement-1)%eachRow == 0:
                await ctx.send("Your snake died.")
                ongoingSnakeGame = False
                lengthOfSnake = 1
                break
        elif movement == -1:
            if (positionOfSnake+movement+3)%eachRow == 0:
                await ctx.send("Your snake died.")
                ongoingSnakeGame = False
                lengthOfSnake = 1
                break
        elif movement == eachRow:
            if (positionOfSnake+movement) > ((numberOfTiles*numberOfTiles)+numberOfTiles*3):
                await ctx.send("Your snake died.")
                ongoingSnakeGame = False
                lengthOfSnake = 1
                break
        elif movement == -eachRow:
            if ((positionOfSnake+movement)+numberOfTiles*2) < 0:
                await ctx.send("Your snake died.")
                ongoingSnakeGame = False
                lengthOfSnake = 1
                break
        await snake_game.edit(content=snakeBoard)\
'''

bot.run(TOKEN)