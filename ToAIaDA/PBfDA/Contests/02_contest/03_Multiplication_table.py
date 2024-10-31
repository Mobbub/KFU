def get_offset_str(num):
    if num < 10:
        return '   '
    if num > 9 and num < 100:
        return '  '
    elif num > 99:
        return ' '

dimentions = input().split()
row = int(dimentions[0])
col = int(dimentions[1])

print('    |', end='')
for i in range(1, col + 1):
    offset = get_offset_str(i)
    print(f'{offset}{i}', end='')
print()
print('   --', end='')
for i in range(1, col + 1):
    print('----', end='')
print()

for i in range(1, row + 1):
    offset = get_offset_str(i)
    print(f'{offset}{i}|', end='')
    for j in range(1, col + 1):
        inner_offset = get_offset_str(i * j)
        print(f'{inner_offset}{i * j}', end='')
    print()