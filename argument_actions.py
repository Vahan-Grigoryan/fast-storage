from argparse import Action
from db import operations as db_operations


class TableOrQuery(Action):
    def __call__(self, parser, namespace, values, option_string):
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



