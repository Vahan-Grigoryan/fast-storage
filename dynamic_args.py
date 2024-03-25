"""
This file stores all optioanl CLI args of program.
This file dynamicly changes by main.set_columns_as_cli_args.
Dont't change this file manually!!!
"""

args = (
    (
        ("--id",), 
        {
        'type': int,
        'metavar': '',
        'help': '''\
            option for point id of row,
            can be used as filter(in read operation) or
            pointer to row for update, delete operations
        '''
        }
    ),
    (("--dyn_table-dyn_col",), {'metavar': '', 'help': 'dyn_table table column.', 'type':int}),
    (("--tmpdata-name",), {'metavar': '', 'help': 'tmpdata table column.'}),
    (("--tmpdata-data",), {'metavar': '', 'help': 'tmpdata table column.'}),
    (("--tmpdata-important",), {'metavar': '', 'help': 'tmpdata table column.'}),
    (("--tmpdata-urgently",), {'metavar': '', 'help': 'tmpdata table column.'}),
    (("--tmpdata-additional_column",), {'metavar': '', 'help': 'tmpdata table column.', 'type':int}),
    (("--tmpdata-additional_column2",), {'metavar': '', 'help': 'tmpdata table column.', 'type':int}),
)
