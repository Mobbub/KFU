pair = input().split()
lower = int(pair[0])
higher = int(pair[1])

odds = [item for item in range(lower, higher + 1) if item % 2 == 1]
print(len(odds))