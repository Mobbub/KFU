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


import csv, math, dsmltf, random

def load(name):
    data = []
    with open(f'{name}.csv', mode='r') as file:
        spamreader = csv.DictReader(file, delimiter=',')
        for row in spamreader:
            data += [[float(row['Pclass']), float(row['Sex']), float(row['Age']), float(row['Embarked']), float(row['Survived'])]]
        
    x = [[1] + r[:4] for r in data]
    y = [r[4] for r in data]
    print(x, y)
    return x, y

def sigmoid(x):
    return 1.0/(1+math.exp(-x))

def sigmoid_d(x):
    return sigmoid(x)*(1-sigmoid(x))

def log_likelyhood_i(x_i, y_i, beta):
    # print(x_i)
    # print(y_i)
    # print(beta)
    if y_i == 1:
        return math.log(sigmoid(dsmltf.dot(x_i, beta)))
    return math.log(1-sigmoid(dsmltf.dot(x_i, beta)))

def log_likelyhood(x,y,beta):
    return sum(log_likelyhood_i(x_i, y_i, beta) for x_i,y_i in zip(x,y))

def log_partial_ij(x_i,y_i, beta,j):
    return (y_i - sigmoid(dsmltf.dot(x_i,beta)))*x_i[j]

def log_grad_i(x_i,y_i,beta):
    return [log_partial_ij(x_i,y_i, beta,j) for j,_ in enumerate(beta)]

def log_grad (x, y, beta):
    return dsmltf.reduce(dsmltf.vector_add, [log_grad_i(x_i,y_i,beta) for x_i,y_i in zip(x,y)])

def main(choice, name_file):
    if choice == 1:
        # Загрузка данных
        x_train, y_train = load('cleaned_titanic')

        x_test, y_test = load(name_file) # Предполагаем, что у вас есть отдельный файл для тестовых данных

        fn = dsmltf.partial(log_likelyhood,x_train,y_train)

        # Инициализация весов
        beta_0 = [random.random() for _ in range(5)] # 5 элементов, так как у нас 4 признака + 1 константа
        beta_hat, trash = dsmltf.gradient_descent(dsmltf.negate(fn), beta_0)
        
        print(beta_hat)
        
        # Подсчет метрик
        true_positives = 0
        false_positives = 0
        true_negatives = 0
        false_negatives = 0

        for x_i,y_i in zip(x_test, y_test):
            predict = sigmoid(dsmltf.dot(beta_hat, x_i))
            if y_i == 1 and predict >= 0.5:
                true_positives +=1
            elif y_i == 1:
                false_negatives +=1
            elif predict >= 0.5:
                false_positives +=1 
            else:
                true_negatives +=1

        print(true_positives)
        print(true_negatives)
        print(false_positives)
        print(false_negatives)
        
        precision = true_positives/(true_positives+false_positives)
        recall = true_positives/(true_positives+false_negatives)

        print("Точность:", precision)
        print("Полнота:", recall)
    else:
        x_train, y_train = load(name_file) 

        fn = dsmltf.partial(log_likelyhood,x_train,y_train)

        beta_0 = [random.random() for _ in range(5)] # 5 элементов, так как у нас 4 признака + 1 константа
        beta_hat, trash = dsmltf.gradient_descent(dsmltf.negate(fn), beta_0)
        
        print(beta_hat)
        
        new_class = float(input('Введите класс\n> '))
        new_sex = float(input('Введите пол\n> '))
        new_age = float(input('Введите возраст\n> '))
        new_emb = float(input('Введите путь направления\n> '))

        new_data = [1, new_class, new_sex, new_age, new_emb] 

        predict = sigmoid(dsmltf.dot(beta_hat, new_data))

        print('Предсказанный статус:', predict)

        if predict >= 0.5:
            print('Выжил')
        else:
            print('Умер')

if __name__ == '__main__':
    choice = int(input('Выберете действие:\n1. Проверить на тестовой выборке;\n2. Предсказать новые данные\n> '))
    if choice == 1:
        name_file = input('Введите имя файла тестовой выборки:\n> ')
        main(choice, name_file)
    elif choice == 2:
        main(choice, 'cleaned_titanic')
    else:
        print('Не правильный выбор!!!')
        
# Pclass - 1 - 3, Sex - 0 man, 1 woman, Age - (0 - 17) - 0, (18 - 40) -1, (41 + ) - 2, Embarked S - 0, Q - 1, C - 2