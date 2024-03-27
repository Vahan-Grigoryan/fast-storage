"""
This file stores all optioanl CLI args of program.
This file dynamicly changes by main.set_columns_as_cli_args.
Dont't change this file manually!!!
"""

args = (
    (("--tmpdata-name",), {'metavar': '', 'help': 'tmpdata table column.'}),
    (("--tmpdata-data",), {'metavar': '', 'help': 'tmpdata table column.'}),
    (("--tmpdata-important",), {'metavar': '', 'help': 'tmpdata table column.'}),
    (("--tmpdata-urgently",), {'metavar': '', 'help': 'tmpdata table column.'}),
    (("--dyn_table-dyn_col",), {'metavar': '', 'help': 'dyn_table table column.', 'type':int}),
)
