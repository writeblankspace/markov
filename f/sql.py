# Functions used to build the SQL query
# with respect to NULL


def eq(column: str, word: str | None) -> str:
    if word:
        return f"{column} = ?"
    else:
        # word is None
        return f"{column} IS NULL"


def fmt_value_list(len: int) -> str:
    return ", ".join("?" for _ in range(len))


# Get rid of None in data
def remove_none(*data: str | None) -> tuple[str, ...]:
    return tuple([x for x in data if x])
