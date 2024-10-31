import matplotlib.pyplot as plt

x = [i for i in range(1, 9)]
y_1 = [1.0E-1, 1.0E-2, 1.0E-3, 1.0E-4, 1.0E-5, 1.0E-6, 1.0E-7, 1.0E-8]
y_2 = [5.0E-1, 5.0E-2, 5.0E-3, 5.0E-4, 5.0E-5, 5.0E-6, 5.0E-7, 5.0E-8]
y_3 = [9.0E-1, 9.0E-2, 9.0E-3, 9.0E-4, 9.0E-5, 9.0E-6, 9.0E-7, 9.0E-8]

plt.figure(facecolor=None)
plt.semilogy(x, y_1, marker='^', color='blue', label='σ = 0.1')
plt.semilogy(x, y_2, marker='v', color='green', label='σ = 0.5')
plt.semilogy(x, y_3, marker='s', color='red', label='σ = 0.9')

plt.xlabel('Highest Degree of Polynomials P')
plt.ylabel('L2 error')
plt.title('Convergence plot')
plt.legend()
plt.show()