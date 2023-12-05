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
                item['price'] = int(cl.find('price').get_text().strip())
                item['rating'] = float(cl.find('rating').get_text().strip())
                item['reviews'] = int(cl.find('reviews').get_text().strip())
                item['sporty'] = True if cl.find('sporty').get_text().strip() == 'yes' else False
                item['new'] = True if cl.find('new').get_text().strip() == '+' else False
                item['exclusive'] = True if cl.find('exclusive').get_text().strip() == 'yes' else False
            except:
                pass

            items.append(item)

    return items

items = list()

for i in range(1, 101):
    file_name = f'tasks/zip_var_53_4/{i}.xml'
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
menu.whrite_json(stat, 'answers/result_stat_4.json')
print(f"MAX price -> {stat['max']}\nMIN price -> {stat['min']}\nAVG price -> {round(stat['avg'], 2)}\n")

# частота метки
ram_counter = menu.frequency_label(items, 'color')
print("Частотность созвездий: ", ram_counter)