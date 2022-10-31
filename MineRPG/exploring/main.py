from random import randint

from content.enemies.enemy_chicken import Chicken
from content.enemies.enemy_bat import Water_Bat
from .database import check_User_in_DB, add_User, get_User, update_User, add_Enemy, get_Enemy, update_Enemy, delete_Enemy

def monsters_available(level):
    monsters = []

    monsters.append(Chicken)

    if level < 10:
        monsters.append(Water_Bat)

    return monsters

def random_monster_generator(monstersList):
    ran = randint(0, (len(monstersList)-1))
    return monstersList[ran]

async def go_adventure(ctx):
    if not check_User_in_DB(ctx.author.id):
        add_User(ctx.author.id)
    
    user_result = get_User(ctx.author.id)

    if (user_result.enemy_id == None):
        monstersList = monsters_available(user_result.level)
        monster_chosen = random_monster_generator(monstersList)
        add_Enemy(ctx.author.id, monster_chosen.get_name(), monster_chosen.get_hp(), monster_chosen.get_damage())
        user_result = get_User(ctx.author.id)

    enemy_result = get_Enemy(user_result.enemy_id)

    user_result.hp = user_result.hp - enemy_result.damage
    enemy_result.hp = enemy_result.hp - user_result.damage

    message = f"```\n"
    message += f"You dealt {user_result.damage} to {enemy_result.name}.\nYou took {enemy_result.damage} damage.\n\nYour HP: {user_result.hp}\nEnemy HP: {enemy_result.hp}\n"
    
    update_User(user_result)
    update_Enemy(enemy_result)

    if (user_result.hp <= 0):
        delete_Enemy(user_result, enemy_result)

        message += f"\nYou have fainted."

    if (enemy_result.hp <= 0):
        delete_Enemy(user_result, enemy_result)

        message += f"\nYou have killed {enemy_result.name}."

    message += "```"

    await ctx.send(message)

