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


import requests, re, csv, datetime
from bs4 import BeautifulSoup

def get_price(item):
    return int(item['price'])

def high_price(data):
    sorted_data = sorted(data.items(), key=lambda x: get_price(x[1]), reverse=True)
    result = {key: value for key, value in sorted_data}
    
    now = datetime.datetime.now()
    train_date = f"train_{now.strftime('%Y-%m-%d_%H-%M-%S')}"
    with open(f'{train_date}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'name', 'price', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for key, value in result.items():
            row = {'id': key, 'name': value['name'], 'price': value['price'], 'date': value['date']}
            writer.writerow(row)
        
    return 'Данные сохраненны'
    
def low_price(data):
    sorted_data = sorted(data.items(), key=lambda x: get_price(x[1]))
    result = {key: value for key, value in sorted_data}
    
    now = datetime.datetime.now()
    train_date = f"train_{now.strftime('%Y-%m-%d_%H-%M-%S')}"
    with open(f'{train_date}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'name', 'price', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for key, value in result.items():
            row = {'id': key, 'name': value['name'], 'price': value['price'], 'date': value['date']}
            writer.writerow(row)
        
    return 'Данные сохраненны'
    
def price_range(data, low_num, max_num):
    result = {}
    for i in range(1,len(data)+1):
        if low_num <= data[i]['price'] <= max_num:
            result[i] = data[i]

    now = datetime.datetime.now()
    train_date = f"train_{now.strftime('%Y-%m-%d_%H-%M-%S')}"
    with open(f'{train_date}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'name', 'price', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for key, value in result.items():
            row = {'id': key, 'name': value['name'], 'price': value['price'], 'date': value['date']}
            writer.writerow(row)
        
    return 'Данные сохраненны'
    
def main(item):
    result = {}
    months = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря': 12
    }

    link = 'https://krym.kupiprodai.ru/lichnoe/simferopol_odezhdamuzhskaya/param2160'
    response = requests.get(link).text
    soup = BeautifulSoup(response, 'html.parser')

    block = soup.find('body')
    step_1 = block.find('div', attrs={'class':'width100'})
    step_2 = step_1.find_all(class_='center1200 box-sizing')

    for element_st_2 in step_2:
        try:
            step_3 = element_st_2.find_all(class_='width100 content margin_bottom_50')
        except:
            pass

    for element_st_3 in step_3:
        try:
            step_4 = element_st_3.find_all(class_='content_layout')
        except:
            pass

    for element_st_4 in step_4:
        try:
            step_5 = element_st_4.find_all(class_='content_left')
        except:
            pass

    for element_st_5 in step_5:
        try:
            step_6 = element_st_5.find('ul', id = 'cat')
        except:
            pass

    step_7 = step_6.find_all('li')

    count = 0
    for prod in step_7:
        try:
            title = prod.find('a', class_='list_title').text.strip()  
            price = prod.find('span', class_='list_price').text.strip()
            date = prod.find('span', class_='list_data').text.strip()
            date = date.replace('\n', ' ').replace('\t', '')
            count+=1
            if count not in result:
                result[count] = {'name': '', 'price': '', 'date': ''}
            result[count]['name'] = f'"{title}"'
            
            number_str = re.sub(r'[^0-9]', '', price)
            num = int(number_str) 
            result[count]['price'] = num
            
            day = int(str(date).split(" ")[0])
            month = months[date.split(" ")[1]]
            result[count]['date'] = f"{day}.{month:02d}"
        except:
            pass
    
    if item == 1:
        return high_price(result)
    elif item == 2:
        return low_price(result)
    elif item == 3:
        start_num = int(input('Введите начало диапазона\n> '))
        end_num = int(input('Введите конец диапазона\n> '))
        return price_range(result, start_num, end_num)

if __name__ == '__main__':
    while True:
        item = int(input('Мы парсим сайт объявлений "КупиПродай", а если быть более точнее, то категорию - Мужская одежда, обувь. Локация - Симферополь.\nУкажите номер фильтра полученного списка продуктов:\n1. С начало высокая цена;\n2. С начало низкая цена;\n3. Указать диапазон цены.\n> '))
        print(main(item))
        continue