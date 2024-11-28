###########################################################################

#        #     #                            #
# #      #     # #                        # #
#  #           #  #                      #  #
#  #     #     #   #                    #   #
# #      #     #    #                  #    #
#        #     #     #                #     #
# #      #     #      #              #      #
#  #     #     #       #            #       #
#   #    #     #        #          #        #
#   #    #     #         #        #         #
#   #    #     #          #      #          #
#  #     #     #           #    #           #
# #      #     #            #  #            #
#        #     #             #              #
 
#                    #                    #                            #
# #                 # #                   # #                        # #
#  #               #   #                  #  #                      #  #
#  #              #     #                 #   #                    #   #
# #              #       #                #    #                  #    #
#               #         #               #     #                #     #
# #            #           #              #      #              #      #
#  #          #             #             #       #            #       #
#   #        #################            #        #          #        #
#   #       #                 #           #         #        #         #
#   #      #                   #          #          #      #          #
#  #      #                     #         #           #    #           #
# #      #                       #        #            #  #            #
#       #                         #       #             #              #

'''this.provod@gmail.com Кулебакин Иван Викторович'''
##########################################################################


from math import sqrt, pi, atan, erf
import matplotlib.pyplot as plt
   
def gauss_met(matrix, column):
    matrix_size = len(matrix)
    for i in range(matrix_size):
        for j in range(i + 1, matrix_size): 
            ratio = matrix[j][i] / matrix[i][i]
            for k in range(matrix_size):
                matrix[j][k] -= ratio * matrix[i][k]
            column[j] -= ratio * column[i]
    matrix_size = len(matrix)
    solutions = [0] * matrix_size 
    for i in range(matrix_size - 1, -1, -1):
        solutions[i] = column[i]
        for j in range(i + 1, matrix_size):
            solutions[i] -= matrix[i][j] * solutions[j]
        solutions[i] /= matrix[i][i]
    return solutions

def approx_poly(x,t,r): # в cписke x любыe числa
    M = [[] for _ in range(r+1)]
    b = []

    for l in range(r+1):
        for q in range(r+1):
            M[l].append(sum(list(map(lambda z: z**(l+q), t))))
        b.append(sum(xi*ti**l for xi, ti in zip(x, t)))
    a = gauss_met(M, b)
    return a

def poly_fit(x, y, degree):
    coeffs = [0] * (degree + 1)
    for i in range(degree + 1):
        sum_x = 0
        sum_xy = 0
        for j in range(len(x)):
            sum_x += x[j] ** i
            sum_xy += x[j] ** i * y[j]
        coeffs[i] = sum_xy / sum_x
    
    y_pred = [sum(coeffs[k] * x[i] ** k for k in range(degree + 1)) for i in range(len(x))]

    n = len(y)
    residuals = [y[i] - y_pred[i] for i in range(n)]
    if n > len(coeffs):
           s_err = sqrt(sum(r ** 2 for r in residuals) / (n - len(coeffs)))
    else:
        # Обработайте ошибку, например, выведите сообщение или верните значение по умолчанию.
       print("Ошибка: Количество точек данных должно быть больше, чем количество коэффициентов.")
       s_err = float('inf')  # Или какое-то другое значение
    
    t_values = []
    p_values = []
    dof = n - 2
    for i in range(len(coeffs)):
        t_value = coeffs[i] / (s_err / sqrt(sum(x[j] ** (2 * i) for j in range(n))))
        t_values.append(t_value)
        p_value = 2 * (1 - t_dist_cdf(abs(t_value), dof))
        p_values.append(p_value)
    
    return p_values

def t_dist_cdf(t, dof):
    return 0.5 + atan(t / sqrt(dof)) / pi

def calculate_power(n, alpha, effect_size):
    z_alpha = -erf(sqrt(alpha))
    z_beta = effect_size * sqrt(n) - z_alpha
    power = erf(z_beta / sqrt(2))
    return power

def graf(x1, t1, x2, t2):
    plt.plot(t2, x2, label='Итоговый')
    plt.plot(t1, x1, label='Изначальный')

    plt.legend()

    plt.xlabel('Время (t)')
    plt.ylabel('Значение (x)')

    plt.title('Графики зависимости x от t')

    plt.show()

def main(r):
    x = [6449, 6398, 6355, 6255, 6140, 6155, 6314, 6420, 6591, 6645, 6522, 6401, 6330, 6135, 6150.5, 6189, 6281, 6287, 6348, 6536, 6448, 6420, 6453.5, 6650, 6847, 6803, 6750, 6815.5, 6900, 6985]
    t = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    
    alf = 0.05 # вероятность ошибки первого рода
    effect_size = 0.8 # размер эффекта

    coef_pol = approx_poly(x, t, r)
    p = poly_fit(x, t, r)
    power = calculate_power(len(x), alf, effect_size)
    print(f'Коэф. полинома: {coef_pol}\np: {p}\nМощность: {power}')
    
    x_new = coef_pol[0]
    coef_pol_new = coef_pol[1:]
    count = 1
    
    for i in range(len(coef_pol_new)):
        x_new += coef_pol_new[i]*31**count
        count+=1
    
    x2=x+[x_new]
    t2 = t+[31]

    graf(x, t, x2, t2)

if __name__ == '__main__':
    r = int(input('Введите степень полинома:\n> '))
    main(r)
    
# лукоил акция
# data = {
#     '14.08.2024': 6449,
#     '15.08.2024': 6398,
#     '16.08.2024': 6355,
#     '19.08.2024': 6255,
#     '20.08.2024': 6140,
#     '21.08.2024': 6155,
#     '22.08.2024': 6314,
#     '23.08.2024': 6420,
#     '26.08.2024': 6591,
#     '27.08.2024': 6645,
#     '28.08.2024': 6522,
#     '29.08.2024': 6401,
#     '30.08.2024': 6330,
#     '02.09.2024': 6135,
#     '03.09.2024': 6150.5,
#     '04.09.2024': 6189,
#     '05.09.2024': 6281,
#     '06.09.2024': 6287,
#     '09.09.2024': 6348,
#     '10.09.2024': 6536,
#     '11.09.2024': 6448,
#     '12.09.2024': 6420,
#     '13.09.2024': 6453.5,
#     '16.09.2024': 6650,
#     '17.09.2024': 6847,
#     '18.09.2024': 6803,
#     '19.09.2024': 6750,
#     '20.09.2024': 6815.5,
#     '23.09.2024': 6900,
#     '24.09.2024': 6985,
# }
