from bs4 import BeautifulSoup
import menu


def handle_file(file_name):

    with open(file_name, encoding='utf-8') as file:
        xml = file.read()

        item = dict()

        site = BeautifulSoup(xml, 'xml')

        item['name'] = site.find('star').find('name').get_text().strip()
        item['constellation'] = site.find('star').find('constellation').get_text().strip()
        item['spectral-class'] = site.find('star').find('spectral-class').get_text().strip()
        item['radius'] = site.find('star').find('radius').get_text().strip()
        item['rotation'] = site.find('star').find('rotation').get_text().strip()
        item['age'] = site.find('star').find('age').get_text().strip()
        item['distance'] = site.find('star').find('distance').get_text().strip()
        item['absolute-magnitude'] = site.find('star').find('absolute-magnitude').get_text().strip()

        return item

items = list()

for i in range(1, 500):
    file_name = f'D:/Рабочий стол/tasks/zip_var_53_3/{i}.xml'
    items.append(handle_file(file_name))


# обработанные данные
menu.whrite_json(items, 'answers/result_all_3.json')

# сортировка
print('До сортировки:', items[0:500])
items = menu.sort_data(items, 'name')
print('После сортировки:', items[0:500])

# фильтрация
filter_items = menu.filter_data(items, 'constellation', 'Овен')
menu.whrite_json(filter_items, 'answers/result_filtered_3.json')

# cтатистические характеристики
stat = menu.get_statistics(items, 'radius')
print(f"MAX radius -> {stat['max']}\nMIN radius -> {stat['min']}\nAVG radius -> {round(stat['avg'], 2)}\n")

# частота метки
ram_counter = menu.frequency_label(items, 'constellation')
print("Частотность созвездий: ", ram_counter)