from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, MetaData, String, BIGINT, ForeignKey, ForeignKeyConstraint

# Start up database
user = "rin"
password = "123456"
engine = create_engine("mysql://{}:{}@localhost/minerpg".format(user, password), echo = True)
meta = MetaData(engine)

users = Table(
    'users', meta,
    Column('user_id', BIGINT, primary_key = True),
    Column('hp', Integer, nullable=False, default=10),
    Column('damage', Integer, nullable=False, default=1),
    Column('level', Integer, nullable=False, default=1),
    Column('exp', Integer, nullable=False, default=1),
    Column('exploring', Integer, nullable=False, default=1),
    Column('digging', Integer, nullable=False, default=1),
    Column('mining', Integer, nullable=False, default=1),
    Column('farming', Integer, nullable=False, default=1),
    Column('fighting', Integer, nullable=False, default=1),
    Column('enemyId', Integer, ForeignKey("enemies.enemy_id")),
)

enemies = Table(
    'enemies', meta,
    Column('enemy_id', Integer, primary_key = True),
    Column('hp', Integer), 
    ForeignKeyConstraint(
        ["enemy_id"], ["users.enemyId"], name="fk_enemy_id_parent_enemyId"
    ),
)

meta.create_all(engine)