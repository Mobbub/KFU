def is_prime(*numbers, check='mask'):
    def check_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    results = tuple(check_prime(n) for n in numbers)

    if check == 'any':
        return any(results)
    elif check == 'all':
        return all(results)
    else:
        return results