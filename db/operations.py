from sqlalchemy.orm import sessionmaker
from .models import engine, Base
from sqlalchemy import (
    text,
    select,
)


main_session = sessionmaker(engine) # sessionmaker return session class itself(not instance)


def get_convenient_filters(table, filters):
    """
    Divide filters to two parts:
        for string columns modify filters for searching "like %column_value%",
        other filters remain untouched.
    Return both filter parts
    """
    filters_without_strings_columns = {**filters}
    filters_with_strings_columns = []
    for column_name, column_value in filters.items():
        if type(column_value) == str:
            like_search = \
            getattr(table.c, column_name) \
            .ilike(f"%{column_value}%")

            filters_with_strings_columns.append(like_search)
            del filters_without_strings_columns[column_name]

    return filters_without_strings_columns, filters_with_strings_columns


def insert_row(tablename: str, columns: dict):
    """Insert new row in table"""
    engine.echo = True

    with main_session.begin() as session:
        table = Base.metadata.tables.get(tablename)
        new_row = table.insert().values(**columns)
        session.execute(new_row)

    engine.echo = False

def select_from_table(tablename: str, filters: dict):
    """
    Select rows from table with or without filters 
    and receive only pointed columns or all columns
    """

    with main_session.begin() as session:
        table = Base.metadata.tables.get(tablename)
        columns_to_select = []

        if filters.get("columns"):
            for column_name in filters["columns"]:
                columns_to_select.append(getattr(table.c, column_name))
        else:
            columns_to_select.append(table)
        
        del filters["columns"]

        non_string_filters, string_filters = get_convenient_filters(table, filters)

        query = \
        select(*columns_to_select) \
        .filter_by(**non_string_filters) \
        .where(*string_filters)
        
        rows = session.execute(query).all()

    return rows
    
def update_row(row_id: int, tablename: str, update_fields: dict):
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
