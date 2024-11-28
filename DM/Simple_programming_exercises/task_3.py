def replace_vowels(input_string):
    # Создаем строку с гласными буквами русского языка
    vowels = 'яеиуоыэаю'
    
    # Проходим по каждой гласной букве
    for vowel in vowels:
        # Пока в исходной строке есть двойные гласные, заменяем их на одиночные
        while vowel * 2 in input_string:
            input_string = input_string.replace(vowel * 2, vowel)
        # Пока в исходной строке есть тройные гласные, заменяем их на одиночные
        while vowel * 3 in input_string:
            input_string = input_string.replace(vowel * 3, vowel)
        # Пока в исходной строке есть четверные гласные, заменяем их на одиночные
        while vowel * 4 in input_string:
            input_string = input_string.replace(vowel * 4, vowel)
        # Пока в исходной строке есть пятерные гласные, заменяем их на одиночные
        while vowel * 5 in input_string:
            input_string = input_string.replace(vowel * 5, vowel)
    
    # Возвращаем обработанную строку
    return input_string

# Получаем строку от пользователя
user_input = input()

# Вызываем функцию replace_vowels и выводим результат
result = replace_vowels(user_input)
print(result)