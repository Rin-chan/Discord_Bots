from datetime import datetime, timedelta
import os
from secrets import choice
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy import func, select
import discord

from discord.ext import commands, tasks
from dotenv import load_dotenv

# Start up Discord
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='R', intents=intents)

# Default channel for bot
channel_id = 1015585266519511102 # Send to General in my server

# Start up database
user = "rin"
password = "123456"
engine = create_engine("mysql://{}:{}@localhost/task_board".format(user, password), echo = True)
meta = MetaData(engine)

reminders = Table(
    'reminders', meta,
    Column('id', Integer, primary_key = True),
    Column('user', String(50)),
    Column('title', String(100)),
    Column('description', String(250)),
    Column('dateline', DateTime),
)

meta.create_all(engine)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    
    if not checkForPings.is_running():
        checkForPings.start()

# Still not working
@tasks.loop(minutes=1)
async def checkForPings():
    channel = bot.get_channel(channel_id) # Send to General in my server
    
    todayDate = datetime.now()
    all_reminders = reminders.select().where(reminders.c.dateline >= todayDate, reminders.c.dateline <= todayDate + timedelta(minutes=1))
    conn = engine.connect()
    all_reminders_result = conn.execute(all_reminders)
    
    guild = channel.guild
    for reminder in all_reminders_result:
        if guild.get_user(reminder[1]) is not None:
            await channel.send("Reminder: {} @{}".format(reminder[2], reminder[1]))
        else:
            await channel.send("No user")
    
@bot.command(name="rem", help="View your current reminders")
async def view_reminders(ctx):
    todayDate = datetime.now()
    user_reminders = reminders.select().where(reminders.c.user == ctx.author.id).where(reminders.c.dateline >= todayDate)
    user_reminders_count = select([func.count()]).select_from(reminders).where(reminders.c.user == ctx.author.id).where(reminders.c.dateline >= todayDate)
    conn = engine.connect()
    reminder_result = conn.execute(user_reminders)
    count_result = conn.execute(user_reminders_count).scalar()
    
    message = ctx.author.name + "'s Reminders"
    
    if count_result > 0:
        message += "\n```" 
        for reminder in reminder_result:
            message += ("\nID: {}, Title: {}, Description: {}, End Date: {}".format(reminder[0], reminder[2], reminder[3], reminder[4]))
        message += "\n```"
    else:
        message += "\nThere are no reminders."
    
    await ctx.send(message)
    
@bot.command(name="addrem", help="Add a new reminder")
async def add_reminders(ctx):
    title_rem = ""
    description_rem = ""
    dateline_rem = ""
            
    def check(m):
        return m.author == ctx.author
    
    async def getDateTimeRem():
        while True:
            rem_datetime = await bot.wait_for("message", check=check)
            try:
                rem_datetime = datetime.strptime(rem_datetime.content, '%d/%m/%y %H:%M:%S')
                return rem_datetime
            except:
                continue
    
    async def getReactionRem():
        while True:
            rem_reaction, user = await bot.wait_for("reaction_add")
            
            if rem_reaction.emoji == "👍" and user == ctx.author:
                return True
            elif rem_reaction.emoji == "👎" and user == ctx.author:
                return False
            else:
                continue
        
    await ctx.send("Title?")
    title_rem = await bot.wait_for("message", check=check)
    
    await ctx.send("Description?")
    description_rem = await bot.wait_for("message", check=check)
    
    await ctx.send("Dateline? (dd/mm/yy HH:MM:SS)")
    dateline_rem = await getDateTimeRem()
        
    reminder_message = await ctx.send("New Reminder by {}\n".format(ctx.author.name) +
                   "```\n" +
                   "Title: {}\n".format(title_rem.content) +
                   "Description: {}\n".format(description_rem.content) +
                   "Dateline: {}\n".format(dateline_rem) +
                   "```\n"+
                   "Confirm?")
    
    await reminder_message.add_reaction("👍")
    await reminder_message.add_reaction("👎")
    reaction = await getReactionRem()
    
    if reaction:
        ins = reminders.insert().values(user=ctx.author.id, title=title_rem.content, description=description_rem.content, dateline=dateline_rem)
        conn = engine.connect()
        conn.execute(ins)
        await ctx.send("Reminder has been successfully added")
    else:
        await ctx.send("Reminder has been deleted")
    
@bot.command(name="oldrem", help="View your old reminders")
async def view_old_reminders(ctx):
    todayDate = datetime.now()
    user_reminders = reminders.select().where(reminders.c.user == ctx.author.id).where(reminders.c.dateline <= todayDate)
    user_reminders_count = select([func.count()]).select_from(reminders).where(reminders.c.user == ctx.author.id).where(reminders.c.dateline <= todayDate)
    conn = engine.connect()
    reminder_result = conn.execute(user_reminders)
    count_result = conn.execute(user_reminders_count).scalar()
    
    message = ctx.author.name + "'s Old Reminders"
    
    if count_result > 0:
        message += "\n```" 
        for reminder in reminder_result:
            message += ("\nID: {}, Title: {}, Description: {}, End Date: {}".format(reminder[0], reminder[2], reminder[3], reminder[4]))
        message += "\n```"
    else:
        message += "\nThere are no reminders."
    
    await ctx.send(message)

@bot.command(name="editrem", help="Edit your reminders using the ID of the reminder")
async def edit_reminders(ctx, ID):
    def check(m):
        return m.author == ctx.author
    
    async def getDateTimeRem():
        while True:
            rem_datetime = await bot.wait_for("message", check=check)
            try:
                rem_datetime = datetime.strptime(rem_datetime.content, '%d/%m/%y %H:%M:%S')
                return rem_datetime
            except:
                continue
            
    user_reminders = reminders.select().where(reminders.c.user == ctx.author.id).where(reminders.c.id == ID)
    user_reminders_count = select([func.count()]).select_from(reminders).where(reminders.c.user == ctx.author.id).where(reminders.c.id == ID)
    conn = engine.connect()
    reminder_result = conn.execute(user_reminders).one_or_none()
    count_result = conn.execute(user_reminders_count).scalar()
    
    if count_result == 0:
        message = "There are no reminders."
        await ctx.send(message)
        return
    elif count_result == 1:
        message =  reminder_result[2] + " Reminder"
        message += "\n```" 
        message += ("\nID: {}\nTitle: {}\nDescription: {}\nEnd Date: {}".format(reminder_result[0], reminder_result[2], reminder_result[3], reminder_result[4]))
        message += "\n```"
        await ctx.send(message)
        
        while True:
            await ctx.send("What would you like to edit? (1 for Title, 2 for Description, 3 for End Date, 4 to quit.)")
            choice_rem = await bot.wait_for("message", check=check)
            
            if choice_rem.content == "1":
                await ctx.send("Enter new title (or type \"quit\" to exit)")
                new_title = await bot.wait_for("message", check=check)
                
                if new_title.content.lower() == "quit":
                    break
                else:
                    conn = engine.connect()
                    update_title = reminders.update().values(title=new_title.content).where(reminders.c.id == ID)
                    conn.execute(update_title)
                    await ctx.send("Successfully updated title")
                    break
            elif choice_rem.content == "2":
                await ctx.send("Enter new description (or type \"quit\" to exit)")
                new_description = await bot.wait_for("message", check=check)
                
                if new_description.content.lower() == "quit":
                    break
                else:
                    conn = engine.connect()
                    update_description = reminders.update().values(description=new_description.content).where(reminders.c.id == ID)
                    conn.execute(update_description)
                    await ctx.send("Successfully updated description")
                    break
            elif choice_rem.content == "3":
                await ctx.send("Enter new end date (dd/mm/yy HH:MM:SS)")
                new_dateline = await getDateTimeRem()
                
                conn = engine.connect()
                update_dateline = reminders.update().values(dateline=new_dateline).where(reminders.c.id == ID)
                conn.execute(update_dateline)
                await ctx.send("Successfully updated date")
                break
            elif choice_rem.content == "4":
                await ctx.send("Edit cancelled")
                break
            else:
                await ctx.send("That is not a valid choice")
        
        return
    else:
        message = "Something went wrong"
        await ctx.send(message)
        return
    
@bot.command(name="deleterem", help="Delete your reminders using the ID of the reminder")
async def delete_reminders(ctx, ID):
    def check(m):
        return m.author == ctx.author
    
    user_reminders = reminders.select().where(reminders.c.user == ctx.author.id).where(reminders.c.id == ID)
    user_reminders_count = select([func.count()]).select_from(reminders).where(reminders.c.user == ctx.author.id).where(reminders.c.id == ID)
    conn = engine.connect()
    reminder_result = conn.execute(user_reminders).one_or_none()
    count_result = conn.execute(user_reminders_count).scalar()
    
    if count_result == 0:
        message = "There are no reminders."
        await ctx.send(message)
        return
    elif count_result == 1:
        await ctx.send("Are you sure you want to delete {}? (Type y to confirm)".format(reminder_result[2]))
        confirm = await bot.wait_for("message", check=check)
            
        if confirm == "y":
            conn = engine.connect()
            delete_rem = reminders.delete().where(reminders.c.id == ID)
            conn.execute(delete_rem)
            await ctx.send("Successfully deleted {}".format(reminder_result[2]))
        else:
            await ctx.send("Delete cancelled")
            
        return
    else:
        message = "Something went wrong"
        await ctx.send(message)
        return

bot.run(TOKEN)