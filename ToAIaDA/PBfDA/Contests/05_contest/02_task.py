import matplotlib.pyplot as plt

plt.figure(figsize=(7, 5))

plt.scatter([0.0, 0.1, 0.2, 0.35, 0.45, 0.5, 0.6, 0.8, 0.9],
      [0.75, 0.8, 0.3, 0.65, 0.7, 0.35, 0.6, 0.45, 0.65],
      color='red', label='red', marker='o', s=25, edgecolors='black')

plt.scatter([0.15, 0.25, 0.35, 0.5, 0.75, 0.85, 0.9, 0.95, 1.0],
      [0.1, 0.6, 0.2, 0.95, 0.55, 0.5, 0.6, 0.05, 0.05],
      color='green', label='green', marker='o', s=25, edgecolors='black')

plt.scatter([0.1, 0.25, 0.35, 0.4, 0.45, 0.6, 0.65, 0.8, 0.85],
      [0.95, 0.15, 0.3, 0.7, 0.65, 0.45, 0.1, 0.1, 0.75],
      color='blue', label='blue', marker='o', s=25, edgecolors='black')

plt.xlim(-0.2, 1.2)
plt.ylim(-0.2, 1.2)

plt.xlabel('')
plt.ylabel('')

plt.title('')

label_colors = ['red', 'green', 'blue']

plt.legend(handlelength=3, scatterpoints=3, loc='upper right', labelcolor=label_colors) 

plt.show()