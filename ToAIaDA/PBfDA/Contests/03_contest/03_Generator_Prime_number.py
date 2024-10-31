def prime_nums():
    num = 2
    primes = []
    while True:
        is_prime = all(num % prime != 0 for prime in primes)
        if is_prime:
            primes.append(num)
            yield num
        num += 1