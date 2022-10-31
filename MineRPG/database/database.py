from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .Enemy import Enemy
from .User import User
from . import Base

# Start up database
user = "rin"
password = "123456"
engine = create_engine("mysql://{}:{}@localhost/minerpg".format(user, password), echo = True)

session = scoped_session(sessionmaker())
session.configure(bind=engine, autoflush=False, expire_on_commit=False)

Base.query = session.query_property()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
