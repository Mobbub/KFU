def extract_complex_numbers(nested_list):
    # Инициализация списка для хранения найденных комплексных чисел
    complex_numbers = []

    # Проходим по всем элементам во вложенном списке
    for element in nested_list:
        # Проверяем, является ли элемент списком
        if isinstance(element, list):
            # Если это список, проходим по его подэлементам
            for sub_element in element:
                # Проверяем, является ли подэлемент комплексным числом
                if isinstance(sub_element, complex):
                    # Добавляем комплексное число в итоговый список
                    complex_numbers.append(sub_element)
        # Проверяем, является ли элемент комплексным числом
        elif isinstance(element, complex):
            # Добавляем комплексное число в итоговый список
            complex_numbers.append(element)

    # Возвращаем найденные комплексные числа в виде кортежа
    return tuple(complex_numbers)

# Пример вложенного списка с различными типами данных
ex_list = [1, 2.7, 5j, [4j, 5.0j, 6, 7.7j], 8j, [9j, 10j]]

# Вызов функции для извлечения комплексных чисел из списка
result = extract_complex_numbers(ex_list)

# Печать результата
print(result)
