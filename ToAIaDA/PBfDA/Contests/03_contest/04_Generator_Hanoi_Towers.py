def hanoi(n, source='a', target='b', auxiliary='c'):
    if n > 0:
        yield from hanoi(n - 1, source, auxiliary, target)
        yield (source, target)
        yield from hanoi(n - 1, auxiliary, target, source)