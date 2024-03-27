from argparse import Action
from db import operations as db_operations


class TableOrQuery(Action):
    def __call__(self, parser, namespace, values, option_string):
        """
        Check for value of "tablename_or_raw_query" arg,
        it can be "raw sql query" or one name of existing tables,
        """
        if getattr(namespace, "operation") == "execute":
            setattr(
                namespace,
                "tablename_or_raw_query",
                " ".join(values)
            )
        else:
            choices = tuple(db_operations.Base.metadata.tables.keys())
            if len(values) > 1:
                parser.error(f"Provide exactly one argument, choices are: {choices}")
            elif values[0] not in choices:
                parser.error(f"Available choices are: {choices}")

            setattr(
                namespace,
                "tablename_or_raw_query",
                values[0]
            )


class AvailableColumns(Action):
    def __call__(self, parser, namespace, values, option_string):
        """
        Check for valid value of "columns" arg,
        it can't be more(assumed more elements in list) than table columns
        or be list with invalid name of column 
        """
        tablename = getattr(namespace, "tablename_or_raw_query")
        if tablename != "execute":
            choices = tuple(
                column.name for column in db_operations.Base.metadata.tables.get(tablename).c
            )
            if len(values) > len(choices):
                parser.error(f"Columns more than available columns for {tablename}")
            
            for column_name in values:
                if column_name in choices: continue
                parser.error(f"Invalid column name: {column_name}, choices are: {choices}")
            
            setattr(
                namespace,
                "columns",
                values
            )

