def set_arg(arg: str) -> None:
    with open("dynamic_args.py", "r") as file:
        lines = file.readlines()
    
    lines.insert(
        len(lines)-1, 
        '    (("--%s",), {"help":"%s HELP"}),\n' % (arg, arg)
    )

    with open("dynamic_args.py", "w") as file:
        file.writelines(lines)
