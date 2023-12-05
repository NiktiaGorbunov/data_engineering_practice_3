
from bs4 import BeautifulSoup
import menu

def handle_file(file_name):

    with (open(file_name, encoding='utf-8') as file):
        text = ""

        for row in file.readlines():
            text += row

        item = dict()

        bs = BeautifulSoup(text, 'html.parser')
        build = bs.html.body.div.find_all('div')

        item['city'] = build[0].get_text().split(":")[1].strip()

        item['edifice'] = build[1].h1.get_text().split(":")[1].strip()
        street = build[1].p.get_text().replace("Индекс", ":Индекс")
        item['street'] = street.split(':')[1].strip()
        item['index'] = int(street.split(':')[3].strip())

        item['floors'] = int(build[2].find_all('span', attrs={'class': 'floors'})[0].get_text().split(':')[1].strip())
        item['year'] = int(build[2].find_all('span', attrs={'class': 'year'})[0].get_text().strip().split()[-1])
        item['parking'] = True if build[2].find_all('span')[2].get_text().split(':')[1].strip() == 'есть' else False

        item['img'] = build[3].find('img')['src']

        item['rating'] = float(build[4].find_all('span')[0].get_text().split(":")[1].strip())
        item['views'] = int(build[4].find_all('span')[1].get_text().split(":")[1].strip())

        # print(item['city'])
        # print(item['edifice'])
        # print(item['street'])
        # print(item['index'])
        # print(item['floors'])
        # print(item['year'])
        # print(item['parking'])
        # print(item['img'])
        # print(item['rating'])
        # print(item['views'])

        return item


items = list()

for i in range(1, 1000):
    file_name = f'tasks/zip_var_53_1/{i}.html'
    items.append(handle_file(file_name))

# обработанные данные
menu.whrite_json(items, 'answers/result_all_1.json')

# сортировка
print('До сортировки:', items[0:1000])
items = menu.sort_data(items, 'rating')
print('После сортировки:', items[0:1000])

# фильтрация
filter_items = menu.filter_data(items, 'floors', 1)
menu.whrite_json(filter_items, 'answers/result_filtered_1.json')

# cтатистические характеристики
stat = menu.get_statistics(items, 'rating')
menu.whrite_json(stat, 'answers/result_stat_1.json')
print(f"MAX rating -> {stat['max']}\nMIN rating -> {stat['min']}\nAVG rating -> {round(stat['avg'], 2)}\n")

# частота метки
city_counter = menu.frequency_label(items, 'city')
print("Частотность городов: ", city_counter)