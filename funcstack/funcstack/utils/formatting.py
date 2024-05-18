def indent_lines_after_first(text: str, prefix: str) -> str:
    n_spaces = len(prefix)
    spaces = ' ' * n_spaces
    lines = text.splitlines()
    if len(lines) > 1:
        return '\n'.join([lines[0]] + [spaces + line for line in lines[1:]])
    return lines[0]