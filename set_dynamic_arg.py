import re


def set_arg(arg: str, options: dict = {}) -> None:
    """
    Change dynamic_args module on fly.
    Add new optional arg(if not exist) in dynamic_args.args tuple.
    """

    with open("dynamic_args.py", "r") as file:
        lines = file.readlines()
    
    line_to_insert = f"    ((\"--{arg}\",), {options}),\n"
    # line below need for replace 'python_type' with python_type(remove quotes)
    line_to_insert = re.sub(r"'type':\s?'(\w+)'", r"'type':\1", line_to_insert)

    if line_to_insert in lines: return

    lines.insert(
        len(lines)-1, 
        line_to_insert
    )

    with open("dynamic_args.py", "w") as file:
        file.writelines(lines)
