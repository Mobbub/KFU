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


import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from tqdm import tqdm
import os
from sklearn.decomposition import PCA

def read_data(file_path):
    """Читает данные из CSV файла"""
    try:
        data = pd.read_csv(file_path)
        print(f"Данные успешно прочитаны. Размер данных: {data.shape}")
        return data
    except Exception as e:
        print(f"Ошибка при чтении данных: {e}")

def preprocess_data(data):
    """Обрабатывает данные: кодирует категориальные переменные и шкалирует числовые"""
    data.fillna(0, inplace=True)

    # Оставляем только нужные столбцы для кластеризации
    data = data[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']].copy()
    categorical_cols = ['Sex', 'Embarked']
    numerical_cols = ['Pclass', 'Age', 'SibSp', 'Parch', 'Fare']

    # Кодирование категориальных переменных
    for col in categorical_cols:
        data.loc[:, col] = data[col].astype(str)
        le = LabelEncoder()
        data.loc[:, col] = le.fit_transform(data[col])
    
    # Шкалирование числовых переменных
    scaler = StandardScaler()
    data[numerical_cols] = scaler.fit_transform(data[numerical_cols])

    print("Данные успешно подготовлены и шкалированы.")
    return data

def optimal_kmeans(data):
    """Выполняет кластеризацию методом K-средних и находит оптимальное количество кластеров"""
    inertia = []
    K = range(1, 11)
    
    for k in tqdm(K, desc='Вычисление инерции'):
        kmeans = KMeans(n_clusters=k, random_state=0)
        kmeans.fit(data)
        inertia.append(kmeans.inertia_)
    
    # Визуализация локтя
    plt.figure(figsize=(10, 6))
    plt.plot(K, inertia, marker='o')
    plt.title('Метод локтя для выбора числа кластеров')
    plt.xlabel('Число кластеров K')
    plt.ylabel('Инерция')
    plt.grid()
    plt.show()

    return np.argmin(np.diff(inertia, 2)) + 2

def visualize_kmeans(data, kmeans):
    """Визуализирует результаты кластеризации K-средних"""
    pca = PCA(n_components=2)
    data_2d = pca.fit_transform(data)
    
    plt.figure(figsize=(10, 6))

    # Создаем дискретные цвета для каждого кластера
    scatter = plt.scatter(data_2d[:, 0], data_2d[:, 1], 
                          c=kmeans.labels_, 
                          cmap='tab10',  # Используем набор дискретных цветовых градиентов
                          s=100, 
                          alpha=0.6, 
                          edgecolor='k', 
                          marker='o')
    
    # Центры кластеров
    centers = kmeans.cluster_centers_
    centers_2d = pca.transform(centers)
    plt.scatter(centers_2d[:, 0], centers_2d[:, 1], 
                c='red', s=200, marker='X', label='Центры кластеров')

    plt.title('Результаты кластеризации методом K-средних')
    plt.xlabel('Компонента 1')
    plt.ylabel('Компонента 2')
    
    # Добавляем цветовую легенду
    plt.colorbar(scatter, label='Кластеры', ticks=range(len(np.unique(kmeans.labels_))))  
    plt.legend()
    plt.grid()
    plt.show()

def hierarchical_clustering(data):
    """Выполняет иерархическую кластеризацию и визуализирует дендрограмму"""
    plt.figure(figsize=(10, 6))
    dendrogram = sch.dendrogram(sch.linkage(data, method='ward'))
    plt.title('Дендрограмма')
    plt.xlabel('Идентификаторы образцов')
    plt.ylabel('Расстояние')
    plt.show()

def main():
    os.makedirs('processed_data', exist_ok=True)

    df = read_data('titanic.csv')
    df_processed = preprocess_data(df)

    print("Запуск кластеризации методом K-средних...")
    optimal_k = optimal_kmeans(df_processed)
    
    # Повторный запуск K-средних с оптимальным количеством кластеров
    kmeans = KMeans(n_clusters=optimal_k, random_state=0)
    kmeans.fit(df_processed)

    # Визуализация кластеров K-средних
    visualize_kmeans(df_processed.values, kmeans)

    print("Запуск иерархической кластеризации...")
    hierarchical_clustering(df_processed)

if __name__ == '__main__':
    main()
