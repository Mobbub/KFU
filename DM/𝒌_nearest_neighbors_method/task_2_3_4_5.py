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


import csv
import random
from collections import Counter
from math import sqrt
from sklearn.manifold import TSNE

def load_data(filename):
    data = []
    species_map = {'setosa': 1.0, 'versicolor': 2.0, 'virginica': 3.0}
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append([float(row['sepal_length']), float(row['sepal_width']),
                         float(row['petal_length']), float(row['petal_width']),
                         species_map[row['species']]])
    return data

def normalize(data):
    features = [list(map(float, row[:-1])) for row in data]
    
    means = [sum(col) / len(col) for col in zip(*features)]
    stds = [((sum((x - m) ** 2 for x in col) / len(col)) ** 0.5) for m, col in zip(means, zip(*features))]
    normalized_features = [
        [(x - m) / s if s > 0 else 0 for x, m, s in zip(row, means, stds)]
        for row in features
    ]
    return normalized_features, [row[-1] for row in data]

def euclidean_distance(a, b):
    return sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def knn_classify(train_data, test_instance, k):
    distances = []
    for train_instance in train_data:
        dist = euclidean_distance(train_instance[:-1], test_instance[:-1])
        distances.append((train_instance, dist))
        
    distances.sort(key=lambda x: x[1])
    neighbors = [distances[i][0] for i in range(k)]
    most_common = Counter(instance[-1] for instance in neighbors).most_common(1)
    return most_common[0][0]

def best_k(train_data, test_data):
    err = 0.0001
    best_accuracy = 0
    best_k_value = 1
    for k in range(1, 11):
        correct = 0
        for test_instance in test_data:
            predicted = knn_classify(train_data, test_instance, k)
            if predicted - test_instance[-1] >= err or predicted - test_instance[-1] >= -err:
                correct += 1
        accuracy = correct / len(test_data)
        print(f'K={k}, Точность={accuracy:.2f}')
        if accuracy > best_accuracy or (accuracy == best_accuracy and k > best_k_value):
            best_accuracy = accuracy
            best_k_value = k
            
    return best_k_value

def mean_by_column(matrix):
    n_rows = len(matrix)
    n_cols = len(matrix[0])
    means = []
    
    for col in range(n_cols):
        col_sum = 0
        for row in range(n_rows):
            col_sum += matrix[row][col]
        means.append(col_sum / n_rows)
    
    return means

def matrix_multiply(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

def vector_multiply(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]

def normalize_pca(v):
    norm = sum(x**2 for x in v)**0.5
    return [x / norm for x in v]

def power_iteration(A, num_iterations=1000):
    n = len(A)
    b_k = [random.uniform(-1, 1) for _ in range(n)]
    b_k = normalize_pca(b_k)

    for _ in range(num_iterations):
        b_k1 = vector_multiply(A, b_k)
        b_k1_norm = sum(x**2 for x in b_k1)**0.5
        b_k = normalize_pca(b_k1)

    return b_k1_norm, b_k

def find_eigenvalues_and_vectors(A, num_values=5):
    n = len(A)
    eigenvalues = []
    eigenvectors = []

    for _ in range(num_values):
        eigenvalue, eigenvector = power_iteration(A)
        eigenvalues.append(eigenvalue)
        eigenvectors.append(eigenvector)

        A = [[A[i][j] - eigenvalue * eigenvector[i] * eigenvector[j] for j in range(n)] for i in range(n)]

    return eigenvalues, eigenvectors

def pca(X, n_components=2):
    mean_values = [sum(column) / len(X) for column in zip(*X)]

    X_centered = [[x - mean for x, mean in zip(row, mean_values)] for row in X]

    n_samples = len(X)
    n_features = len(X[0])

    means = [sum(row[i] for row in X) / n_samples for i in range(n_features)]

    covariance_matrix = [[0] * n_features for _ in range(n_features)]
    
    for i in range(n_features):
        for j in range(n_features):
            cov_ij = sum((X[k][i] - means[i]) * (X[k][j] - means[j]) for k in range(n_samples)) / (n_samples - 1)
            covariance_matrix[i][j] = cov_ij

    eigenvalues, eigenvectors = find_eigenvalues_and_vectors(covariance_matrix)
    sorted_indices = sorted(range(len(eigenvalues)), key=lambda i: eigenvalues[i], reverse=True)
    sorted_eigenvectors = [[eigenvectors[j][i] for j in range(len(eigenvectors))] for i in sorted_indices]
    selected_eigenvectors = [sorted_eigenvectors[j] for j in range(n_components)]
    X_reduced = [[sum(a * b for a, b in zip(row, col)) for col in zip(*selected_eigenvectors)] for row in X_centered] 
    
    return X_reduced

def tsne(data, n_components=2):
    import numpy as np
    
    data = np.array(data)
    features = data[:, :-1].astype(float)
    tsne = TSNE(n_components=n_components, random_state=0)
    transformed = tsne.fit_transform(features)

    return transformed

def main():
    err = 0.0001
    data = load_data('iris.csv')
    normalized_data, trash = normalize(data)
    
    random.shuffle(normalized_data)
    train_size = int(0.8 * len(normalized_data))
    train_data = normalized_data[:train_size]
    test_data = normalized_data[train_size:]
    
    best_k_value = best_k(train_data, test_data)
    print(f'Лучший k: {best_k_value}')
    
    correct = 0
    for test_instance in test_data:
        predicted = knn_classify(train_data, test_instance, best_k_value)
        if predicted - test_instance[-1] >= err or predicted - test_instance[-1] >= -err:
            correct += 1
    accuracy = correct / len(test_data)
    print(f'Точность K-NN классификации: {accuracy:.2f}')

    pca_result = pca(data)
    pca_train = pca_result[:train_size]
    pca_test = pca_result[train_size:]

    pca_correct = 0
    for i, test_instance in enumerate(pca_test):
        predicted = knn_classify(pca_train, test_instance, best_k_value)
        if predicted - test_data[i][-1] >= err or predicted - test_data[i][-1] >= -err:
            pca_correct += 1

    pca_accuracy = pca_correct / len(pca_test)
    print(f'Точность K-NN классификации с использованием PCA: {pca_accuracy:.2f}')

    tsne_result = tsne(data)
    tsne_train = tsne_result[:train_size]
    tsne_test = tsne_result[train_size:]

    tsne_correct = 0
    for i, test_instance in enumerate(tsne_test):
        predicted = knn_classify(tsne_train, test_instance, best_k_value)
        if predicted - test_data[i][-1] >= err or predicted - test_data[i][-1] >= -err:
            tsne_correct += 1

    tsne_accuracy = tsne_correct / len(tsne_test)
    print(f'Точность K-NN классификации с использованием t-SNE: {tsne_accuracy:.2f}')

    
if __name__ == "__main__":
    main()