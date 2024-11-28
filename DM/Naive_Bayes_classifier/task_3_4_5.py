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
import re

def tokenize(directory, array_size, position):
    word_count = {}
    total_words = 0

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                text = file.read()
                text = re.sub(r'[^\w\s]', '', text)
                words = text.split()
                total_words += len(words)

                for word in words:
                    if word not in word_count:
                        word_count[word] = [0] * array_size
                    word_count[word][position] += 1

    return word_count, total_words

def message_tokenize(directory):
    messages = []

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                text = file.read()
                text = re.sub(r'[^\w\s]', '', text)
                messages.append(text)

    return messages

def common_token(directory, number_of_words):
    word_count = {}

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                text = file.read()
                text = re.sub(r'[^\w\s]', '', text)
                words = text.split()

                for word in words:
                    if word not in word_count:
                        word_count[word] = 0
                    word_count[word] += 1

    sorted_words = sorted(word_count.items(), key=lambda item: item[1], reverse=True)
    top_words = [word for word, count in sorted_words[:number_of_words]]
    return top_words

def specific_words_tokenize(directory, specific_words, array_size, position):
    word_count = {}
    total_words = 0

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                text = file.read()
                text = re.sub(r'[^\w\s]', '', text)
                words = text.split()
                total_words += len(words)

                for word in words:
                    if word in specific_words:
                        if word not in word_count:
                            word_count[word] = [0] * array_size
                        word_count[word][position] += 1

    return word_count, total_words

def merge_token(dict1, dict2):
    merged_dict = {}

    for key in dict1:
        merged_dict[key] = dict1[key]

    for key in dict2:
        if key in merged_dict:
            for i in range(len(merged_dict[key])):
                merged_dict[key][i] += dict2[key][i]
        else:
            merged_dict[key] = dict2[key]

    return merged_dict

def prob_words(word_count, total_spam, total_non_spam, smoothing):
    probabilities = {}
    V = len(word_count)

    for word, counts in word_count.items():
        p_spam = (counts[0] + smoothing) / (total_spam + smoothing * (V + 1))
        p_non_spam = (counts[1] + smoothing) / (total_non_spam + smoothing * (V + 1))
        probabilities[word] = [p_spam, p_non_spam]

    return probabilities

def message_prediction(probabilities, message):
    message = re.sub(r'[^\w\s]', '', message)
    words = message.split()

    for word in words:
        if word in probabilities:
            spam_probability *= (probabilities[word][0])
            non_spam_probability *= (probabilities[word][1])
        else:
            spam_probability *= 0.1
            non_spam_probability *= 0.9

    if (spam_probability + non_spam_probability == 0 ):
        return 0
    else:
        total_probability = spam_probability / (spam_probability + non_spam_probability)
        return total_probability

def run_classifier(spam_text, check_text, non_spam_text):
    mes = message_tokenize(check_text)
    
    spam, spam_len = tokenize(spam_text, 2, 0)
    non_spam, non_spam_len = tokenize(non_spam_text, 2, 1)
    
    token = merge_token(spam,  non_spam)
    
    token_wer = prob_words(token, 30, 30, 0.01)
    
    comtok3 = token_wer

    for i, message in enumerate(mes):
        spam_prob = message_prediction(comtok3, message)
        print(f"Сообщение №{i + 1} вероятность спама: {spam_prob}")

    while True:
        user_message = input("Введите ваше сообщение (или 'quit' для выхода): ")
        if user_message.lower() == 'quit':
            break  # Выход из цикла при вводе 'quit'
        spam_prob = message_prediction(comtok3, user_message)
        print(f"Вероятность спама: {spam_prob:.4f}")

if __name__ == "__main__":
    run_classifier('spam_text', 'check_text', 'non_spam_text')
