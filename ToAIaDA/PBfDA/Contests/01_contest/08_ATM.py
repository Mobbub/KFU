N = int(input())

nom = [5000, 1000, 500, 200, 100]

cup = [0, 0, 0, 0, 0]

for i in range(len(nom)):
    cup[i] = N // nom[i]
    N -= cup[i] * nom[i]

print(*cup)