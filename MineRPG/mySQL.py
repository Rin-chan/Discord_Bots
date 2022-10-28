from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, MetaData, String, BIGINT

# Start up database
user = "rin"
password = "123456"
engine = create_engine("mysql://{}:{}@localhost/minerpg".format(user, password), echo = True)
meta = MetaData(engine)

users = Table(
    'users', meta,
    Column('id', BIGINT, primary_key = True),
    Column('level', Integer, nullable=False, default=1),
    Column('exp', Integer, nullable=False, default=1),
    Column('exploring', Integer, nullable=False, default=1),
    Column('digging', Integer, nullable=False, default=1),
    Column('mining', Integer, nullable=False, default=1),
    Column('farming', Integer, nullable=False, default=1),
    Column('fighting', Integer, nullable=False, default=1),
)

items = Table(
    'items', meta,
    Column('id', Integer, primary_key = True),
    Column('type', String(25)),
    Column('name', String(50)),
)

meta.create_all(engine)