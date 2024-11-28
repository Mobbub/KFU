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


import random, time, math
import matplotlib.pyplot as plt

from task_1 import generate_y

def get_frequencies_and_amplitudes(a0, a, b, period=500):
    frequencies = []
    amplitudes = []

    frequencies.append(0)
    amplitudes.append(abs(a0))

    for k in range(1, len(a) + 1):
        frequency = k / period
        amplitude = (a[k-1]**2 + b[k-1]**2)**0.5
        frequencies.append(frequency)
        amplitudes.append(amplitude)
    
    return frequencies, amplitudes

def fourier_series(t, a0, a, b, N, T=500, Pi2=2 * math.pi):
    result = a0 
    for n in range(1, N + 1):
        result += a[n - 1] * math.cos(Pi2 * n * t / T)
        result += b[n - 1] * math.sin(Pi2 * n * t / T)
    return result

def calculate_fourier_coefficients_s(x, y, N, Pi2=2 * math.pi, T=500, n_harmonics=2, learning_rate=0.001, max_iterations=5000, batch_size=50):
    a0 = 0.0
    a = [random.random() for _ in range(n_harmonics)]
    b = [random.random() for _ in range(n_harmonics)]

    for _ in range(max_iterations):
        indices = random.sample(range(len(x)), batch_size)
        x_batch = [x[i] for i in indices]
        y_batch = [y[i] for i in indices]

        predictions = [fourier_series(xi, a0, a, b, N) for xi in x_batch]
        error = [predictions[i] - y_batch[i] for i in range(batch_size)]

        a0_gradient = sum(2 * e for e in error) / batch_size
        a_gradient = [
            sum(2 * error[i] * math.cos(Pi2 * n * x_batch[i] / T) for i in range(batch_size)) / batch_size
            for n in range(1, n_harmonics + 1)
        ]
        b_gradient = [
            sum(2 * error[i] * math.sin(Pi2 * n * x_batch[i] / T) for i in range(batch_size)) / batch_size
            for n in range(1, n_harmonics + 1)
        ]

        a0 -= learning_rate * a0_gradient
        a = [a[i] - learning_rate * a_gradient[i] for i in range(n_harmonics)]
        b = [b[i] - learning_rate * b_gradient[i] for i in range(n_harmonics)]

    return a0, a, b

def calculate_fourier_coefficients_p(t, y, N, Pi2=2 * math.pi, T=500):
    a0 = 0.0
    a = [random.random() for _ in range(N)]
    b = [random.random() for _ in range(N)]
    
    alpha = 0.001
    num_iterations = 5000 
    
    for _ in range(num_iterations):
        predictions = [fourier_series(ti, a0, a, b, N) for ti in t]
        error = [predictions[i] - y[i] for i in range(len(t))]
        
        a0_gradient = sum(2 * e for e in error) / len(error)
        a_gradient = [
            sum(2 * error[i] * math.cos(Pi2 * n * t[i] / T) for i in range(len(t))) / len(t)
            for n in range(1, N + 1)
        ]
        b_gradient = [
            sum(2 * error[i] * math.sin(Pi2 * n * t[i] / T) for i in range(len(t))) / len(t)
            for n in range(1, N + 1)
        ]
        
        a0 -= alpha * a0_gradient
        a = [a[i] - alpha * a_gradient[i] for i in range(N)]
        b = [b[i] - alpha * b_gradient[i] for i in range(N)]
    
    return a0, a, b

def drawing_graphs(t, y, y_n_g, y_s_p):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

    ax1.plot(t, y, label='Исходная f', color='blue')
    ax1.plot(t, y_n_g, color='red', linestyle='--')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.grid()

    ax2.plot(t, y, label='Истинная f', color='blue')
    ax2.plot(t, y_s_p, color='red', linestyle='--')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.grid()

    plt.show()

def main(y):
    t = [i for i in range(1, 501)]

    start_time_n_p = time.time()
    a0, a, b = calculate_fourier_coefficients_p(t, y, N=2)
    y_n_g = [fourier_series(ti, a0, a, b, N=2) for ti in t]
    end_time_n_p = time.time()

    start_time_s_p = time.time()
    a0gs, ags, bgs = calculate_fourier_coefficients_s(t, y, N=2)
    y_s_p = [fourier_series(ti, a0gs, ags, bgs, N=2) for ti in t]
    end_time_s_p = time.time()

    print(f'Время работы алгоритма с обычным градиентным спуском (в секундах): {end_time_n_p - start_time_n_p}\nВремя работы алгоритма со стахостическим градиентным спуском (в секундах): {end_time_s_p - start_time_s_p}\n\nКоэффициент a0: {a0}\nКоэффициенты a: {a}\nКоэффициенты b: {b}')
    freg, ampl = get_frequencies_and_amplitudes(a0, a, b)
    print(f'Частоты: {freg}\n\nКоэффициент a0gs: {a0gs}\nКоэффициенты ags: {ags}\nКоэффициенты bgs: {bgs}')
    freggs, amplgs = get_frequencies_and_amplitudes(a0gs, ags, bgs)
    print("Частоты:", freggs)
    
    drawing_graphs(t, y, y_n_g, y_s_p)
    
    return 0

if __name__ == '__main__':
    k = int(input('Введите ваш номер в журнале:\n> '))
    y = generate_y(k)
    main(y)