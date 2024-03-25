import argparse, prepare_main, textwrap, argument_actions
from db import operations as db_operations


# Prepare CLI args
args_parser = argparse.ArgumentParser(
    usage = "%(prog)s {positional arguments} [options]",
    formatter_class = argparse.RawDescriptionHelpFormatter,
    allow_abbrev = False,
    description = textwrap.dedent(
    """
    Welcome to fast-storage, small replacement for notes!
    Utility created for use in environments, where more work does from command line
    and intends to be used instead of storing data in some temporary files.
    fast-storage can store simple data(string, integer, boolean) in db rows
    and provide CRUD operations with them.
    By default created only one table - tmpdata
    Examples of use:
        %(prog)s show-columns tmpdata
        %(prog)s create tmpdata --tmpdata-name "New name" --tmpdata-data "New info" --tmpdata-important True
        %(prog)s read tmpdata
        %(prog)s read tmpdata --tmpdata-data "New info"
        %(prog)s update tmpdata --id <id-received-from-read-operation> --tmpdata-important False
        %(prog)s delete tmpdata --id <id-received-from-read-operation>
    """
    ),
)
args_parser.add_argument(
    "operation",
    choices = (
        "create",
        "read",
        "update",
        "delete",
        "show-columns",
        "execute",
    ),
    help = "Operation with notes/rows or execute custom query"
)
args_parser.add_argument(
    "tablename_or_raw_query",
    action = argument_actions.TableOrQuery,
    nargs = '+',
    help = "One name of existing tables"
)

prepare_main.set_columns_as_cli_args()

prepare_main.add_available_args(args_parser)
args = args_parser.parse_args()


# Do corresponding thing based on CLI args
if args.operation == "show-columns":
    prepare_main.show_columns(args.tablename_or_raw_query)

elif args.operation == "read":
    columns_to_filter = prepare_main.validate_pointed_columns(args, args.tablename_or_raw_query, for_other_operations=True)
    db_operations.select_from_table(args.tablename_or_raw_query, **columns_to_filter)

elif args.operation == "create":
    required_columns = prepare_main.validate_pointed_columns(args, args.tablename_or_raw_query)
    db_operations.insert_row(args.tablename_or_raw_query, **required_columns)

elif args.operation == "update":
    columns_to_update = prepare_main.validate_pointed_columns(args, args.tablename_or_raw_query, for_other_operations=True)
    db_operations.update_row(args.row_id, args.tablename_or_raw_query, **columns_to_update)

elif args.operation == "delete":
    db_operations.delete_row(args.row_id, args.tablename_or_raw_query)

elif args.operation == "execute":
    db_operations.execute_any_query(args.tablename_or_raw_query)
