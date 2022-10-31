from database.database import engine, session
from database.User import User
from database.Enemy import Enemy

def check_User_in_DB(userId):
    result = User.query.filter_by(id=userId).scalar()
    
    if (result == None):
        return False
    return True

def add_User(userId):
    user = User(id=userId)
    session.add(user)
    session.commit()

def get_User(userId):
    result = User.query.filter_by(id=userId).first()
    return result

def update_User(user):
    session.add(user)
    session.commit()

def add_Enemy(userId, name, hp, damage):
    ins1 = Enemy(name=name, hp=hp, damage=damage)
    session.add(ins1)
    session.flush()

    user = User.query.filter_by(id=userId).first()
    user.enemy_id = ins1.id
    session.add(user)
    session.commit()

def get_Enemy(enemyId):
    result = Enemy.query.filter_by(id=enemyId).first()
    return result

# INCOMPLETE
def update_Enemy(enemy):
    session.add(enemy)
    session.commit()

def delete_Enemy(user, enemy):
    user.enemy_id = None
    session.add(user)
    session.delete(enemy)
    session.commit()
