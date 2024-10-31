x = int(input())

steps = 0

while x != 1:
    if x % 2 == 0:
        x = x // 2
    else:
        x = 3 * x + 1
    steps += 1

print(steps)