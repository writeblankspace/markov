# Functions used to build the SQL query 
# with respect to NULL

def eq(column: str, word: str) -> str:
    if word:
        return f"{column} = ?"
    else:
        # word is None
        return f"{column} IS NULL"

# Get rid of None in data
def remove_none(*data: tuple[str | None]) -> tuple[str]:
    return tuple([x for x in data if x])