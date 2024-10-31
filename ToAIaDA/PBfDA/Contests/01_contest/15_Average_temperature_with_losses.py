temps = input().split(';')
temps = [int(temp) for temp in temps if temp != '']
print(sum(temps) / len(temps))
