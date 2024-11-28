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


import math

def f_norm(x, mu, s):
    return (1+math.erf((x-mu)/math.sqrt(2)/s))/2

def p_value(x, mu, s):
    if x>=mu:
        return 2*(1-f_norm(x, mu, s))
    return 2*f_norm(x, mu, s)

def main(num):
    if num == 1:    
        u0, u1 = 4, 3
        best = 8
        p0 = u0 / best
        p1 = u1 / best
        for n in range(100, 0, -1):
            sig0, sig1 = math.sqrt(n * p0 * (1 - p0)), math.sqrt(n * p1 * (1 - p1))
            if p_value(math.ceil(n*0.95), p0, sig0) == 0 and p_value(math.ceil(n*0.95), p1, sig1) == 0:
                continue
            else:
                print(f'Ответ: {n+1}')
                break
    elif num == 2:
        u0, u1 = 4, 3
        best = 7
        p0 = u0 / best
        p1 = u1 / best
        for n in range(100, 0, -1):
            sig0, sig1 = math.sqrt(n * p0 * (1 - p0)), math.sqrt(n * p1 * (1 - p1))
            print(f'n = {n}\np0 p_value0 = {p_value(math.ceil(n*0.95), p0, sig0)}\np1 p_value1 = {p_value(math.ceil(n*0.95), p1, sig1)}')
    else:
        print('Не правильный вариант ответа!!!')

if __name__ == '__main__':
    response = int(input('Выберите действие:\n1. Просмотреть ответ;\n2. Просмотреть все часы.\n> '))
    main(response)