import numpy as np

input_vector = [float(x) for x in input().split()]

squared_vector = np.square(np.array(input_vector))
sin_vector = np.sin(squared_vector)
min_value = np.min(sin_vector)

print(f"{min_value:.2f}")