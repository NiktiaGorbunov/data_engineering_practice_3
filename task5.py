import requests
from bs4 import BeautifulSoup
import menu

WEBSITE = 'https://ekipirovka.ru'

PAGES = ['https://ekipirovka.ru/catalog/turisticheskaya_odezhda/?PAGEN_1=1',
         'https://ekipirovka.ru/catalog/turisticheskaya_odezhda/?PAGEN_1=2',
         'https://ekipirovka.ru/catalog/turisticheskaya_odezhda/?PAGEN_1=3',
         'https://ekipirovka.ru/catalog/turisticheskaya_odezhda/?PAGEN_1=4',
         ]


def create_html(pages, path):
    for i, page in enumerate(pages):

        r = requests.get(page)
        soup = BeautifulSoup(r.text, 'html.parser')

        catalog_items = soup.html.find('div', attrs={'class': 'catalog-item-table-view'})

        whrite_html(str(catalog_items), f'{path}{i}.html')

def create_html_from_items(pages, path):
    for i, page in enumerate(pages):

        r = requests.get(page)
        soup = BeautifulSoup(r.text, 'html.parser')

        catalog_items = soup.html.find('div', attrs={'class': 'body_text'})

        whrite_html(str(catalog_items), f'{path}{i}.html')

def whrite_html(items: str, path_name: str):
    with open(path_name, 'w', encoding='utf-8') as f:
        f.write(items)



def handle_file_from_pages(file_name):
    items = list()
    with (open(file_name, encoding='utf-8') as file):
        text = ""

        for row in file.readlines():
            text += row

        bs = BeautifulSoup(text, 'html.parser')
        item_cards = bs.find_all('div', attrs={'class': 'catalog-item-card'})

        for card in item_cards:
            item = dict()

            item['id'] = card.find('div', attrs={'class': 'moby-block moby-block-avail'})['data-element-id']
            item['image'] = WEBSITE+card.find('div', attrs={'class': 'item-image'}).find('picture').source['srcset']
            item['type'] = card.find('div', attrs={'class': 'item-all-title'}).find('a').get_text().split(' ')[0].strip()
            item['name'] = ' '.join(card.find('div', attrs={'class': 'item-all-title'}).find('a').get_text().split(' ')[1:]).strip()
            try:
                item['price'] = card.find('div', attrs={'class': 'item-price-cont'}).find('meta', attrs={'itemprop': 'price'})['content']
            except:
                item['price'] = '0'
            item['availability'] = card.find('div', attrs={'class': 'item-price-cont'}).find('meta', attrs={'itemprop': 'availability'})['content']
            item['vote'] = int(card.find('div', attrs={'class': 'vote-block'}).find('td', attrs={'class': 'vote-result'}).get_text().strip()[1:-1])
            item['link'] = WEBSITE+card.find('div', attrs={'class': 'buy_more'}).find('div', attrs={'class': 'add2basket_block'}).find('span')['onclick'][17:-2]
            items.append(item)
        return items

def handle_file_from_item(file_name):
    with (open(file_name, encoding='utf-8') as file):
        text = ""

        for row in file.readlines():
            text += row

        bs = BeautifulSoup(text, 'html.parser')
        # card = bs.find_all('div', attrs={'class': 'catalog-item-card'})

        item = dict()

        item['id'] = bs.find('div', attrs={'class': 'catalog-detail-element'})['id'].split('_')[-1]
        item['image'] = WEBSITE+bs.find('div', attrs={'class': 'catalog-detail-picture'}).find('picture').source['srcset']
        item['type'] = bs.find('h1').get_text().split(' ')[0].strip()
        item['name'] = ' '.join(bs.find('h1').get_text().split(' ')[1:]).strip()
        try:
            item['price'] = bs.find('div', attrs={'class': 'price_buy_detail'}).find('meta', attrs={'itemprop': 'price'})['content']
        except:
            item['price'] = '0'

        item['vote'] = int(bs.find('div', attrs={'class': 'iblock-vote'}).find('td', attrs={'class': 'vote-result'}).get_text().strip()[1:-1])

        specifications = bs.find('div', attrs={'class': 'catalog-detail-properties'}).find_all('div', attrs={'class': 'catalog-detail-property'})
        property = dict()
        for i in specifications:
             name = i.find('span', attrs={'class': 'name'}).get_text().strip()
             property[name] = ' '.join(i.find('span', attrs={'class': 'val'}).get_text().strip().split())

        item['property'] = property



        return item


def task_1():
    items = list()

    for i in range(0, 4):
        file_name = f'tasks/var_53_5_1/{i}.html'
        items += handle_file_from_pages(file_name)

    # обработанные данные
    menu.whrite_json(items, 'answers/result_all_5_1.json')

    # for item in items:
    #     print(item)
    #
    # print(len(items))

    # сортировка
    print('До сортировки:', items[0:16])
    items = menu.sort_data(items, 'price')
    print('После сортировки:', items[0:16])

    # фильтрация
    filter_items = menu.filter_data(items, 'availability', 'InStock')
    menu.whrite_json(filter_items, 'answers/result_filtered_5_1.json')

    # cтатистические характеристики
    stat = menu.get_statistics(items, 'price')
    print(f"MAX price -> {stat['max']}\nMIN price -> {stat['min']}\nAVG price -> {round(stat['avg'], 2)}\n")

    # частота метки
    ram_counter = menu.frequency_label(items, 'type')
    print("Частотность видов одежды: ", ram_counter)

    return items, "---------------------\nЗадача №1 выполнена\n---------------------\n"


def task_2():
    items = list()

    for i in range(0, 88):
        file_name = f'tasks/var_53_5_2/{i}.html'
        items.append(handle_file_from_item(file_name))

    # for item in items:
    #     print(item)
    #
    # print(len(items))

    # обработанные данные
    menu.whrite_json(items, 'answers/result_all_5_2.json')

    # сортировка
    print('До сортировки:', items[0:16])
    items = menu.sort_data(items, 'price')
    print('После сортировки:', items[0:16])

    # фильтрация
    filter_items = filter_data(items, 'Производитель', 'ВЕК')
    menu.whrite_json(filter_items, 'answers/result_filtered_5_2.json')

    # cтатистические характеристики
    stat = menu.get_statistics(items, 'price')
    print(f"MAX price -> {stat['max']}\nMIN price -> {stat['min']}\nAVG price -> {round(stat['avg'], 2)}\n")

    # частота метки
    ram_counter = frequency_label(items, 'Материал')
    print("Частотность материалов: ", ram_counter)

    return "---------------------\nЗадача №2 выполнена\n---------------------\n"

def filter_data(items: list,  key: str, params: str):
    filter_items = []

    for product in items:
        try:
            if product['property'][key] == params:
                filter_items.append(product)
        except:
            pass

    return filter_items

def frequency_label(items: list, label):
    counter = dict()

    for product in items:
        try:
            value = counter.setdefault(product['property'][label], 0)
            if value >= 0:
                value += 1
                counter.update({product['property'][label]: value})
        except:
            pass

    counter = dict(sorted(counter.items(), key=lambda item: -item[1]))
    return counter

def main():
    # ПОДЗАДАЧА 1
    # спарсить страницы-каталоги, где размещена информаця сразу по нескольким объектам. Обработать данные

    # записать страницы в файл
    # create_html(PAGES, 'tasks/var_53_5_1/')
    #
    items, status = task_1()
    print(status)

    # ПОДЗАДАЧА 2
    # спарсить нескольких страниц (минимум 10), посвященных только одному объекту. Обработать данные

    # записать объекты в файл
    # item_pages = []
    # for item in items:
    #     item_pages.append(item['link'])
    #
    # create_html_from_items(item_pages, 'tasks/var_53_5_2/')

    status = task_2()
    print(status)


if __name__ == '__main__':
    main()