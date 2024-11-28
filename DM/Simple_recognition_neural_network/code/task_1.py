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


import numpy as np
import matplotlib.pyplot as plt

import pickle

def load_dataset():
    with open("dataset_5_px.pkl", "rb") as f:
        dataset = pickle.load(f)
    
    x_train = dataset['images']
    y_train = dataset['labels']

    x_train = x_train.astype("float32")  # Убедимся, что это float32

    x_train = np.reshape(x_train, (x_train.shape[0], -1))  # (N, 25)

    num_classes = np.max(y_train) + 1

    y_train = np.eye(num_classes)[y_train]

    return x_train, y_train

def train_predict_task_1():
    images, labels = load_dataset()

    weights_input_to_hidden = np.random.uniform(-0.5, 0.5, (20, 25))
    weights_hidden_to_output = np.random.uniform(-0.5, 0.5, (5, 20))
    bias_input_to_hidden = np.zeros((20, 1))
    bias_hidden_to_output = np.zeros((5, 1))

    logs = ''
    epochs = 20
    e_loss = 0
    e_correct = 0
    learning_rate = 0.01
    logs+=f'Кол-во эпох: {epochs}\nlearning_rate: {learning_rate}\n'
    for epoch in range(epochs):
        logs+=f"Эпоха №{epoch}\n"
        for image, label in zip(images, labels):
            image = np.reshape(image, (-1, 1))
            label = np.reshape(label, (-1, 1))

            hidden_raw = bias_input_to_hidden + weights_input_to_hidden @ image
            hidden = 1 / (1 + np.exp(-hidden_raw))

            output_raw = bias_hidden_to_output + weights_hidden_to_output @ hidden
            output = 1 / (1 + np.exp(-output_raw))

            e_loss += 1 / len(output) * np.sum((output - label) ** 2, axis=0)
            e_correct += int(np.argmax(output) == np.argmax(label))

            delta_output = output - label
            weights_hidden_to_output += -learning_rate * delta_output @ np.transpose(hidden)
            bias_hidden_to_output += -learning_rate * delta_output

            delta_hidden = np.transpose(weights_hidden_to_output) @ delta_output * (hidden * (1 - hidden))
            weights_input_to_hidden += -learning_rate * delta_hidden @ np.transpose(image)
            bias_input_to_hidden += -learning_rate * delta_hidden
        logs+=f"Loss: {round((e_loss[0] / images.shape[0]) * 100, 3)}%\nAccuracy: {round((e_correct / images.shape[0]) * 100, 3)}%\n"
        e_loss = 0
        e_correct = 0

    test_image = plt.imread("pic/resized_image.jpg", format="jpeg")

    gray = lambda rgb: np.dot(rgb[..., :3], [0.299, 0.587, 0.114])
    test_image = 1 - (gray(test_image).astype("float32") / 255)

    test_image = np.resize(test_image, (5, 5)).reshape(-1, 1)

    hidden_raw = bias_input_to_hidden + weights_input_to_hidden @ test_image
    hidden = 1 / (1 + np.exp(-hidden_raw))

    output_raw = bias_hidden_to_output + weights_hidden_to_output @ hidden
    output = 1 / (1 + np.exp(-output_raw))
    
    logs += f'\nТочность: {round(np.max(output) * 100, 2)}'    
    return output.argmax(), logs

    # plt.imshow(test_image.reshape(5, 5), cmap="Greys")
    # plt.title(f"Предикт: {output.argmax()}")
    # plt.show()