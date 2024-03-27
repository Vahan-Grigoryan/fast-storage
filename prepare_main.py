import set_dynamic_arg, sys
from db import operations as db_operations


def add_available_args(args_parser):
    """Add all optioanl args from dynamic_args module"""

    import dynamic_args

    for flags, options in dynamic_args.args: 
        args_parser.add_argument(*flags, **options)


def show_columns(tablename: str):
    """Show available columns and types from given table"""

    table = db_operations.Base.metadata.tables.get(tablename)

    for column in table.c:
        print(
            f"{column.name}",
            column.type,
            "optional" if column.nullable or column.default or column.primary_key else "required",
            f"default: {column.default if column.default else 'not specified'}",
        )

    print(f"""\
    \nHint: use --<tablename>-<column_name> for point column value(except id column), for example: \
    \n--{tablename}-name name1 \
    \n--{tablename}-data data1 \
    \n--id 7
    """)

def pretty_show(rows):
    """Pretty show received rows"""
    
    if not len(rows): print("Nothing to show (◕‿◕)")
    for row in rows:
        print("---------------")
        for column_name, column_value in row._mapping.items():
            if type(column_value) == str:
                print(f"{column_name}:\n\n{column_value}\n\n")
            else:
                print(f"{column_name}: {column_value}")


def set_columns_as_cli_args():
    """Dynamicly add all columns(from all tables) as optional command line args"""

    for tablename, table in db_operations.Base.metadata.tables.items():
        for column in table.c[1:]:
            # [1:] there used for exclude id column
            arg_options = {
                "metavar": "",
                "help": f"{tablename} table column."
            }
            if str(column.type) == "INTEGER":
                arg_options['type'] = 'int'

            set_dynamic_arg.set_arg(f"{tablename}-{column.name}", arg_options)


def validate_pointed_columns(args, tablename: str, for_other_operations: bool = False):
    """
    Case when for_other_operations = False:
        Assuming user try create row,
        check for point all required columns of given table,
        return columns of given table if all valid,
        else raise ValueError
    Case when for_other_operations = True:
        Assuming user try select(or update row) row/rows with/without any filters,
        check if any optional param provided,
        return dict with corresponding params and them values
    Also note that option names will be converted 
    to valid table column names with corresponding values, examples:
        "--tmpdata-name column_value" will be converted to "{'name': column_value}" 
    """
    from fs import args_parser

    table = db_operations.Base.metadata.tables.get(tablename)
    columns_with_values = {}

    for column in table.c:
        if column.name == "id" and getattr(args, "id"):
            column_value = getattr(args, "id")
        elif column.name == "id" and not getattr(args, "id"):
            continue
        else:
            column_value = getattr(args, f"{tablename}_{column.name}")

        if column_value == "stdin":
            column_value = "".join(sys.stdin.readlines())

        if for_other_operations and column_value:
            if str(column.type) == "BOOLEAN":
                columns_with_values[column.name] = False if column_value == "False" else True
            else:
                columns_with_values[column.name] = column_value
        elif not for_other_operations:
            if column.name == "id":
                args_parser.error("You can't set id column, row not created")
            if not column_value and not (column.nullable or column.default):
                args_parser.error(f"Provide correct columns.\nUse \"show-columns {tablename}\" for list available options")
            elif column_value:
                if str(column.type) == "BOOLEAN":
                    if column_value == "False":
                        column_value = False
                    elif column_value == "True":
                        column_value = True
                    else:
                        raise ValueError(f"Available variants is True|False")
                    columns_with_values[column.name] = column_value
                else:
                    columns_with_values[column.name] = column_value

    return columns_with_values
