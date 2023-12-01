from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

user_table = Table('user', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('username', String(255), unique=True),
                   Column('email', String(255), unique=True),
                   Column('hashed_password', String(255)))
