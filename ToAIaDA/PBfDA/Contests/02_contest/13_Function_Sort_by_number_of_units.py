def sort_key(num: str):
    return num.count('1'), -int(num)