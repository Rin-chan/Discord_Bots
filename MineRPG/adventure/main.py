from random import randint

from .database import check_User_in_DB, get_all_enemies, add_User, get_User, update_User, add_Enemy, get_Enemy, update_Enemy, delete_Enemy

def level_up(exp):
    level = 1

    if (exp > 10):
        level = 2
    elif (exp > 25):
        level = 3

    return level

def monsters_available(level):
    monsters = []

    for monster in get_all_enemies(level):
        monsters.append(monster)

    return monsters

def random_monster_generator(monstersList):
    ran = randint(0, (len(monstersList)-1))
    return monstersList[ran]

def calculate_max_hp(level):
    return level*5 + 5

def calculate_damage(weapon, level):
    return level+weapon

async def go_adventure(ctx):
    if not check_User_in_DB(ctx.author.id):
        add_User(ctx.author.id)
    
    user_result = get_User(ctx.author.id)

    if (user_result.enemy_id == None):
        monstersList = monsters_available(user_result.level)
        monster_chosen = random_monster_generator(monstersList)
        add_Enemy(ctx.author.id, monster_chosen)
        user_result = get_User(ctx.author.id)

    enemy_result = get_Enemy(user_result.enemy_id)

    user_result.hp = user_result.hp - enemy_result.damage
    enemy_result.hp = enemy_result.hp - user_result.damage

    message = f"```\n"
    message += f"You dealt {user_result.damage} to {enemy_result.name}.\nYou took {enemy_result.damage} damage.\n\nYour HP: {user_result.hp}/{calculate_max_hp(user_result.level)}\nEnemy HP: {enemy_result.hp}/{enemy_result.original_hp}\n"
    
    update_User(user_result)
    update_Enemy(enemy_result)

    if (user_result.hp <= 0):
        delete_Enemy(user_result, enemy_result)

        user_result.hp = calculate_max_hp(user_result.level)
        update_User(user_result)

        message += f"\nYou have fainted."

    if (enemy_result.hp <= 0):
        delete_Enemy(user_result, enemy_result)

        user_result.exp += enemy_result.exp
        user_result.gold += enemy_result.gold

        new_level = level_up(user_result.exp)
        if (new_level > user_result.level):
            user_result.level = new_level
            user_result.hp = calculate_max_hp(user_result.level)

        update_User(user_result)

        message += f"\nYou have killed {enemy_result.name}."

    message += "```"

    await ctx.send(message)

