from .database import check_User_in_DB, add_User, get_User

def calculate_max_hp(level):
    return level*5 + 5

async def get_details(ctx):
    if not check_User_in_DB(ctx.author.id):
        add_User(ctx.author.id)
    
    user_result = get_User(ctx.author.id)

    message = f"```\n{ctx.author.name}'s Stats\n\n"

    message += f"HP: {user_result.hp}/{calculate_max_hp(user_result.level)}\n"
    message += f"Damage: {user_result.damage}\n"
    message += f"Level: {user_result.level}\n"
    message += f"Exp: {user_result.exp}\n"
    message += f"Gold: {user_result.gold}\n"
    message += f"Weapon: {user_result.weapon.name}\n"
    message += f"Digging: {user_result.digging}\n"
    message += f"Mining: {user_result.mining}\n"
    message += f"Farming: {user_result.farming}\n"

    message += "```"
    await ctx.send(message)

async def get_inventory(ctx):
    if not check_User_in_DB(ctx.author.id):
        add_User(ctx.author.id)
    
    user_result = get_User(ctx.author.id)

    inventory = user_result.inventory

    message = f"```\n{ctx.author.name}'s Inventory\n\n"

    for i in  inventory:
        message += f"{i}\n"

    message += "```"
    await ctx.send(message)