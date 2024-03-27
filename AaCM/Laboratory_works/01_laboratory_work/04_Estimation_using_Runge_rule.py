def runge(j_h, j_h_2, k):
    return abs(j_h - j_h_2) / (2 ** k - 1)

j_h = 2
j_h_2 = 3
k = 4

print(runge(j_h, j_h_2, k))