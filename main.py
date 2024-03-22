import argparse, set_dynamic_arg


def add_available_args():
    import dynamic_args

    for flags, options in dynamic_args.args: 
        args_parser.add_argument(*flags, **options)


args_parser = argparse.ArgumentParser()
set_dynamic_arg.set_arg(input("new_table: "))

add_available_args()
args_parser.parse_args()
