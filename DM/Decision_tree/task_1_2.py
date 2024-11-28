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
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
import pickle
import graphviz
import joblib


# Функция для отображения прогресс-бара в консоли
def print_progress_bar(iteration, total, prefix='', length=50):
    percent = (iteration / total) * 100
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent:.2f}% Завершено', end='\r')

# Загружаем данные
def load_data(file_path):
    print("Загрузка данных...")
    data = pd.read_csv(file_path)
    return data

# Разделяем данные на обучающую и тестовую выборки
def split_data(data):
    X = data.iloc[:, :-1].values  # Признаки
    y = data.iloc[:, -1].values  # Целевая переменная
    return train_test_split(X, y, test_size=0.2, random_state=42)

# Функция для оценки индекса Джини
def gini_impurity(left, right):
    total_samples = len(left) + len(right)
    if total_samples == 0:
        return 0

    p_left = len(left) / total_samples
    p_right = len(right) / total_samples

    gini_left = 1 - sum((np.sum(left == c) / len(left)) ** 2 for c in np.unique(left))
    gini_right = 1 - sum((np.sum(right == c) / len(right)) ** 2 for c in np.unique(right))

    return p_left * gini_left + p_right * gini_right

# Функция для поиска лучшего сплита
def best_split(X, y):
    best_gini = float('inf')
    best_feature = None
    best_threshold = None

    for feature_index in range(X.shape[1]):
        thresholds = np.unique(X[:, feature_index])
        for threshold in thresholds:
            left_indices = X[:, feature_index] < threshold
            right_indices = X[:, feature_index] >= threshold
            if len(y[left_indices]) == 0 or len(y[right_indices]) == 0:
                continue

            gini = gini_impurity(y[left_indices], y[right_indices])
            if gini < best_gini:
                best_gini = gini
                best_feature = feature_index
                best_threshold = threshold

    return best_feature, best_threshold

# Рекурсивная функция для роста дерева
def grow_tree(X, y, depth=0, max_depth=None):
    n_samples, _ = X.shape
    if n_samples == 0 or (max_depth is not None and depth >= max_depth):
        return np.mean(y)

    best_feature, best_threshold = best_split(X, y)
    if best_feature is None:
        return np.mean(y)

    left_indices = X[:, best_feature] < best_threshold
    right_indices = X[:, best_feature] >= best_threshold

    left_child = grow_tree(X[left_indices], y[left_indices], depth + 1, max_depth)
    right_child = grow_tree(X[right_indices], y[right_indices], depth + 1, max_depth)

    return (best_feature, best_threshold, left_child, right_child)

# Функция предсказания
def predict(x, tree):
    if isinstance(tree, (int, float)):  # Если дошли до листа
        return int(tree)

    feature_index, threshold, left_child, right_child = tree
    if x[feature_index] < threshold:
        return predict(x, left_child)
    else:
        return predict(x, right_child)

# Функция для предсказания для набора данных
def predict_all(X, tree):
    return np.array([predict(x, tree) for x in X])

# Функция для оценки ROC AUC
def calculate_roc_auc(y_true, y_scores):
    roc_auc = roc_auc_score(y_true, y_scores)
    fpr, tpr, _ = roc_curve(y_true, y_scores)
    return roc_auc, fpr, tpr

# Визуализация ROC кривых
def plot_roc_curves(roc_curves_data):
    plt.figure(figsize=(10, 6))
    for label, (fpr, tpr) in roc_curves_data.items():
        plt.plot(fpr, tpr, label=f'ROC-кривая для {label} (площадь = {roc_auc_score(y_test, y_scores):.2f})')
    
    plt.plot([0, 1], [0, 1], 'k--', label='Случайное предположение')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Уровень ложноположительных результатов')  # Подпись оси X
    plt.ylabel('Уровень истинноположительных результатов')  # Подпись оси Y
    plt.title('Характеристика приемника-оператора (ROC)')  # Заголовок графика
    plt.legend(loc='lower right')  # Легенда в правом нижнем углу
    plt.savefig('roc_curves.png')  # Сохранение графика как изображения
    plt.show()  # Показ графика

# Сохранение дерева в файл
def save_tree(tree, filename):
    with open(filename, 'wb') as f:
        pickle.dump(tree, f)

# Загрузка дерева из файла
def load_tree(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

# Визуализация дерева и сохранение её
def visualize_tree(tree, feature_names, class_names, filename):
    # Сохранение дерева в формате Graphviz
    dot_data = export_graphviz(tree, out_file=None, 
                               feature_names=feature_names,  
                               class_names=class_names,  
                               filled=True, rounded=True,  
                               special_characters=True)  
    graph = graphviz.Source(dot_data)  
    graph.render(filename, format='png', cleanup=True)  # Сохранение дерева в файл формата PNG
    graph.view()  # Открывает дерево в системе

# Основной блок программы
if __name__ == "__main__":
    file_path = 'train.csv'
    data = load_data(file_path)
    X_train, X_test, y_train, y_test = split_data(data)

    best_auc = 0
    roc_curves_data = {}
    
    feature_names = data.columns[:-1].tolist()  # Получение имен признаков из DataFrame
    class_names = ['0', '1']  # Названия классов (можно изменить в зависимости от ваших данных)


    max_depths = [None, 5, 10, 15, 20]

    
    for index, depth in enumerate(max_depths):
        print_progress_bar(index + 1, len(max_depths), prefix="Подбор гиперпараметров")

        model = DecisionTreeClassifier(max_depth=depth)
        model.fit(X_train, y_train)  # Обучение модели

        # Визуализация для каждого дерева
        visualize_tree(model, feature_names, class_names, f'decision_tree_depth_{depth}')

        y_scores = model.predict(X_test)  # Предсказания на тестовой выборке
        roc_auc, fpr, tpr = calculate_roc_auc(y_test, y_scores)  # Получение ROC AUC
        
        print(f'Гиперпараметр max_depth={depth}, ROC AUC={roc_auc:.4f}')
        roc_curves_data[f'Максимальная глубина {depth}'] = (fpr, tpr)  # Сохранение данных для графиков

        save_tree(model, f'decision_tree_depth_{depth}.pkl')  # Сохранение обученной модели

        plot_roc_curves(roc_curves_data)  # Визуализация ROC кривых

    while True:
        user_input = input("Введите данные для предсказания (через запятую) или 'exit' для выхода: ")
        if user_input.lower() == 'exit':
            break
        try:
            input_data = np.array([float(i) for i in user_input.split(',')]).reshape(1, -1)
            prediction = model.predict(input_data)  # Получение предсказания

            print(f'Предсказание: {prediction[0]}')
        except ValueError:
            print("Ошибка: убедитесь, что вводимые данные числовые и разделены запятыми.")

    filename = input("Введите название файла дерева для загрузки (или 'none' для пропуска): ")
    if filename != 'none':
        loaded_model = load_tree(filename)
        loaded_predictions = predict_all(X_test, loaded_model)
        print("Предсказания загруженного дерева:", loaded_predictions)
