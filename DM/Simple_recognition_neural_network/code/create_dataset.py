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


import os
import numpy as np
from PIL import Image
import pickle

def create_mnist_like_dataset(data_dir, image_size=(10, 10)):
    X = []  # Список для изображений
    y = []  # Список для меток классов

    # Проходим по всем классам в папке
    for label in os.listdir(data_dir):
        label_dir = os.path.join(data_dir, label)

        if os.path.isdir(label_dir):
            # Проходим по всем изображениям в папке класса
            for img_file in os.listdir(label_dir):
                img_path = os.path.join(label_dir, img_file)

                try:
                    # Открываем изображение и меняем его размер, если нужно
                    with Image.open(img_path) as img:
                        img = img.convert('L')  # Преобразуем в градации серого
                        if img.size != image_size:
                            img = img.resize(image_size, Image.ANTIALIAS)

                        # Преобразуем изображение в массив и нормализуем
                        img_array = np.array(img) / 255.0  # Нормализация

                        X.append(img_array)
                        y.append(int(label))  # Добавляем метку класса
                except Exception as e:
                    print(f"Ошибка при обработке файла {img_path}: {e}")

    # Преобразуем списки в numpy массивы
    X = np.array(X)
    y = np.array(y)

    # Сохраняем датасет
    dataset = {'images': X, 'labels': y}
    with open('mnist_like_dataseыыt.pkl', 'wb') as f:
        pickle.dump(dataset, f)

    print(f'Датасет содержит {len(X)} изображений')

data_directory = 'dataset_10_px'
create_mnist_like_dataset(data_directory)
