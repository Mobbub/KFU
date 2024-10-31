result = []
num1 = int(input())
log_old = input().split()
num2 = int(input())
log_new = input().split()

for log in log_new:
    if log not in log_old:
        result.append(log)

result = list(set(result))

print(*sorted(result))