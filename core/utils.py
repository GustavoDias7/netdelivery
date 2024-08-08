def remove_non_alphanumeric(value: str):
    return "".join([e for e in value if e.isalnum()])
