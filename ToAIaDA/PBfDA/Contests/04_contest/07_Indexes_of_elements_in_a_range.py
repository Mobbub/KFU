def find_indices_in_range(vector):
    indices = [i for i, value in enumerate(vector) if -100 <= value <= 100]
    return indices

vector = list(map(int, input().split()))
indices = find_indices_in_range(vector)
print(" ".join(map(str, sorted(indices))))