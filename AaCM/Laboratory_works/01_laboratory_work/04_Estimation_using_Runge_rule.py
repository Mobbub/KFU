def runge(j_h, j_h_2, k):
    return abs(j_h - j_h_2) / (2 ** k - 1)

j_h = 1/3
j_h_2 = 0.2800000000000001
k = 2

print(runge(j_h, j_h_2, k))