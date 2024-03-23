from .models import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (
    create_engine,
    update,
    Table,
)


engine = create_engine("sqlite:///db\db.sqlite")
main_session = sessionmaker(engine) # sessionmaker return session class itself(not instance)

Base.metadata.reflect(engine)
Base.metadata.create_all(engine)


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
        query = update(table).where(table.c.id == row_id).values(**update_fields)
        session.execute(query)

    print("Updated")

def delete_row(row_id: int, tablename: str):
    """Delete one row"""

    with main_session.begin() as session:
        table = Base.metadata.tables.get(tablename)
        query = table.delete().where(table.c.id == row_id)
        session.execute(query)

    print("Deleted")
