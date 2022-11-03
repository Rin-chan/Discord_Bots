from database.database import engine, session
from database.User import User

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