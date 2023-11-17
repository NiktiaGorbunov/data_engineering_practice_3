from bs4 import BeautifulSoup
import menu


def handle_file(file_name):

    items = list()

    with open(file_name, encoding='utf-8') as file:
        xml = file.read()

        item = dict()

        clothing = BeautifulSoup(xml, 'xml').find_all('clothing')

        for cl in clothing:
            try:
                item['id'] = cl.find('id').get_text().strip()
                item['name'] = cl.find('name').get_text().strip()
                item['category'] = cl.find('category').get_text().strip()
                item['size'] = cl.find('size').get_text().strip()
                item['color'] = cl.find('color').get_text().strip()
                item['material'] = cl.find('material').get_text().strip()
                item['price'] = cl.find('price').get_text().strip()
                item['rating'] = cl.find('rating').get_text().strip()
                item['reviews'] = cl.find('reviews').get_text().strip()
                item['sporty'] = cl.find('sporty').get_text().strip()
                item['new'] = cl.find('new').get_text().strip()
                item['exclusive'] = cl.find('exclusive').get_text().strip()
            except:
                pass

            items.append(item)

    return items

items = list()

for i in range(1, 101):
    file_name = f'D:/Рабочий стол/tasks/zip_var_53_4/{i}.xml'
    items += handle_file(file_name)



# обработанные данные
menu.whrite_json(items, 'answers/result_all_4.json')

# сортировка
print('До сортировки:', items[0:100])
items = menu.sort_data(items, 'size')
print('После сортировки:', items[0:100])

# фильтрация
filter_items = menu.filter_data(items, 'category', 'Jacket')
menu.whrite_json(filter_items, 'answers/result_filtered_4.json')

# cтатистические характеристики
stat = menu.get_statistics(items, 'price')
print(f"MAX price -> {stat['max']}\nMIN price -> {stat['min']}\nAVG price -> {round(stat['avg'], 2)}\n")

# частота метки
ram_counter = menu.frequency_label(items, 'color')
print("Частотность созвездий: ", ram_counter)