import argparse, prepare_fs, textwrap, argument_actions
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
        %(prog)s execute create table dyn_table "(id integer primary key autoincrement NOT NULL, dyn_col int default 111)"

    Pay attention:
        you can also use "stdin" keyword as stdin value for ONLY STRING columns values like: --tmpdata-data stdin
    """
    ),
    epilog = textwrap.dedent(
    """
    Pay attention:
        you can also use "stdin" keyword as stdin value for ONLY STRING columns values like: --tmpdata-data stdin
    """
    )
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
args_parser.add_argument(
    "--id",
    type = int,
    metavar = '',
    help = '''\
        point id of row, can be used as filter(in read operation) or
        pointer to row for update, delete operations
    '''
)
args_parser.add_argument(
    "--columns",
    action = argument_actions.AvailableColumns,
    metavar = '',
    nargs = '+',
    help = '''\
        point which columns will be received,
        can be used only for read operations, else option will be ignored
    '''
)

prepare_fs.set_columns_as_cli_args()

prepare_fs.add_available_args(args_parser)
args = args_parser.parse_args()


# Do corresponding thing based on CLI args
if __name__ == "__main__":
    if args.operation == "show-columns":
        prepare_fs.show_columns(args.tablename_or_raw_query)
    
    elif args.operation == "read":
        columns_to_filter = prepare_fs.validate_pointed_columns(args, args.tablename_or_raw_query, for_other_operations=True)
        columns_to_filter["columns"] = args.columns
        rows = db_operations.select_from_table(args.tablename_or_raw_query, columns_to_filter)
        prepare_fs.pretty_show(rows)
    
    elif args.operation == "create":
        required_columns = prepare_fs.validate_pointed_columns(args, args.tablename_or_raw_query)
        db_operations.insert_row(args.tablename_or_raw_query, required_columns)
    
    elif args.operation == "update":
        columns_to_update = prepare_fs.validate_pointed_columns(args, args.tablename_or_raw_query, for_other_operations=True)
        db_operations.update_row(args.id, args.tablename_or_raw_query, columns_to_update)
    
    elif args.operation == "delete":
        db_operations.delete_row(args.id, args.tablename_or_raw_query)
    
    elif args.operation == "execute":
        db_operations.execute_any_query(args.tablename_or_raw_query)
