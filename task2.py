import json
from bs4 import BeautifulSoup
import menu

def handle_file(file_name):

    items = list()

    with (open(file_name, encoding='utf-8') as file):
        text = ""

        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')
        products = site.html.body.find_all('div', 'product-item')

        for product in products:
            item = dict()
            item['id'] = product.a['data-id']
            item['link'] = product.find_all('a')[1]['href']
            item['img_url'] = product.find_all('img')[0]['src']
            item['title'] = product.find_all('span')[0].get_text().strip()
            item['price'] = int(product.price.get_text().replace("₽", "").replace(" ", "").strip())
            item['bonus'] = int(product.strong.get_text().replace("+ начислим ", "").replace(" бонусов", "").strip())

            props = product.ul.find_all('li')
            for prop in props:
                item[prop['type']] = prop.get_text().strip()

            items.append(item)

    return items

items = list()

for i in range(1, 92):
    file_name = f'tasks/zip_var_53_2/{i}.html'
    items += handle_file(file_name)

# обработанные данные
menu.whrite_json(items, 'answers/result_all_2.json')

# сортировка
print('До сортировки:', items[0:92])
items = menu.sort_data(items, 'price')
print('После сортировки:', items[0:92])

# фильтрация
filter_items = menu.filter_data(items, 'matrix', 'OLED')
menu.whrite_json(filter_items, 'answers/result_filtered_2.json')

# cтатистические характеристики
stat = menu.get_statistics(items, 'bonus')
print(f"MAX bonus -> {stat['max']}\nMIN bonus -> {stat['min']}\nAVG bonus -> {round(stat['avg'], 2)}\n")

# частота метки
ram_counter = menu.frequency_label(items, 'ram')
print("Частотность оперативной памяти: ", ram_counter)