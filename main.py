import argparse, prepare_main
from db import operations as db_operations


# Prepare CLI args
args_parser = argparse.ArgumentParser(allow_abbrev=False)
args_parser.add_argument(
    "operation",
    choices=("create", "read", "update", "delete", "show-columns")
)
args_parser.add_argument(
    "tablename",
    choices=db_operations.Base.metadata.tables.keys()
)

prepare_main.set_columns_as_cli_args()

prepare_main.add_available_args(args_parser)
args = args_parser.parse_args()


# Do corresponding thing based on CLI args
if args.operation == "show-columns":
    prepare_main.show_columns(args.tablename)

elif args.operation == "read":
    columns_to_filter = prepare_main.validate_pointed_columns(args, args.tablename, for_other_operations=True)
    db_operations.select_from_table(args.tablename, **columns_to_filter)

elif args.operation == "create":
    required_columns = prepare_main.validate_pointed_columns(args, args.tablename)
    db_operations.insert_row(args.tablename, **required_columns)

elif args.operation == "update":
    columns_to_update = prepare_main.validate_pointed_columns(args, args.tablename, for_other_operations=True)
    db_operations.update_row(args.row_id, args.tablename, **columns_to_update)

elif args.operation == "delete":
    db_operations.delete_row(args.row_id, args.tablename)
