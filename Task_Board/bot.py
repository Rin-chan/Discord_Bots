from datetime import datetime
import os
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy import func, select
import discord

from discord.ext import commands
from dotenv import load_dotenv

# Start up Discord
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='R', intents=intents)

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

@bot.command(name="reminders", help="View your current reminders")
async def view_reminders(ctx):
    user_reminders = reminders.select().where(reminders.c.user == ctx.author.id)
    user_reminders_count = select([func.count()]).select_from(reminders).where(reminders.c.user == ctx.author.id)
    conn = engine.connect()
    reminder_result = conn.execute(user_reminders)
    count_result = conn.execute(user_reminders_count).scalar()
    
    message = ctx.author.name + "'s Reminders"
    
    if count_result > 0:
        message += "\n```" 
        for reminder in reminder_result:
            message += ("\n" + str(reminder))
        message += "\n```"
    else:
        message += "\nThere are no reminders."
    
    await ctx.send(message)
    
@bot.command(name="addrem", help="Add a new reminder")
async def view_reminders(ctx):
    title_rem = ""
    description_rem = ""
    dateline_rem = ""
            
    async def getDateTimeRem():
        while True:
            rem_datetime = await bot.wait_for("message")
            try:
                rem_datetime = datetime.strptime(rem_datetime.content, '%d/%m/%y %H:%M:%S')
                return rem_datetime
            except:
                continue
    
    def check(m):
        return m.author == ctx.author
    
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
    
bot.run(TOKEN)