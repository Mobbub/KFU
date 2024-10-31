def min_number(n):
    if n == 0:
        return 10
    if n == 1:
        return 1

    digits = []
    for i in range(9, 1, -1):
        while n % i == 0:
            digits.append(i)
            n //= i

    if n > 1:
        return 0

    digits.sort()
    result = int(''.join(map(str, digits)))
    return result