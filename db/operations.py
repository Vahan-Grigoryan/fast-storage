from sqlalchemy.orm import sessionmaker
from .models import engine, Base
from sqlalchemy import (
    text,
)


main_session = sessionmaker(engine) # sessionmaker return session class itself(not instance)

def insert_row(tablename: str, **columns):
    """Insert new row in table"""
    engine.echo = True

    with main_session.begin() as session:
        table = Base.metadata.tables.get(tablename)
        new_row = table.insert().values(**columns)
        session.execute(new_row)

    engine.echo = False

def select_from_table(tablename: str, **filters):
    """Select rows from table with or without filters"""

    with main_session.begin() as session:
        table = Base.metadata.tables.get(tablename)
        query = table.select().filter_by(**filters)
        rows = session.execute(query).all()
    
    print(rows)

def update_row(row_id: int, tablename: str, **update_fields):
    """Update one row"""

    with main_session.begin() as session:
        table = Base.metadata.tables.get(tablename)
        query = table.update().where(table.c.id == row_id).values(**update_fields)
        session.execute(query)

    print("Updated")

def delete_row(row_id: int, tablename: str):
    """Delete one row"""

    with main_session.begin() as session:
        table = Base.metadata.tables.get(tablename)
        query = table.delete().where(table.c.id == row_id)
        session.execute(query)

    print("Deleted")

def execute_any_query(raw_query: str):
    """
    Execute any query to db,
    can be used for creating, altering tables and other specific queries
    """

    with main_session.begin() as session:
        session.execute(text(raw_query))

    print("Executed")
