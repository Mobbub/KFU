def get_excel_column_name(n):
    if n < 1:
        raise ValueError("Номер столбца должен быть больше 0")
    
    column_name = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        column_name = chr(65 + remainder) + column_name
    return column_name

n = int(input())
print(get_excel_column_name(n))