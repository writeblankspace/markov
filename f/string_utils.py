import re


def censor(string: str) -> str:
    """
    Returns a censored version of the string, Roblox-style.

    Regular expressions to censor must be in `./censor.txt`, with one expression
    per line."""

    res: str = string

    # Open the file of regular expressions
    try:
        with open("./censor.txt", "r") as file:
            patterns: list[str] = file.readlines()
    except FileNotFoundError:
        # The file doesn't exist
        # So this must mean nothing needs to be censored
        return res

    for pattern in patterns:
        res = re.sub(
            pattern=pattern.rstrip("\n"),  # it has a trailing newline smh
            repl=lambda x: "#" * (x.end() - x.start()),  # Roblox censor
            string=res,
            flags=re.IGNORECASE
        )

    return res
