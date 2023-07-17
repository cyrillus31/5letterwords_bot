def is_letter(symbol: str) -> bool:
    try:
        ascii_code = ord(symbol)
        if 1040 <= ascii_code <= 1103:
            return True
        else: 
            return False
    except TypeError:
        return False


def is_valid_string(message: str) -> bool:
    if len(message) != 5:
        return False
    
    valid_symbols = 0
    for symbol in message:
        if is_letter(symbol):
            valid_symbols += 1
    if valid_symbols > 0:
        return True
    return False


def add_wildcards(message: str) -> str:
    new_message = ""
    for symbol in message:
        if is_letter(symbol):
            new_message += symbol
        else:
            new_message += "_"
    return new_message
