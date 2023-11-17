import json

def whrite_json(items: list, path_name: str):
    json_items = json.dumps(items)
    with open(path_name, 'w', encoding='utf-8') as f:
        f.write(json_items)

def sort_data(items: list, key: str):
    sort_items = sorted(items, key=lambda x: x[key], reverse=True)

    return sort_items

def filter_data(items: list,  key: str, params: str):
    filter_items = []

    for product in items:
        try:
            if product[key] == params:
                filter_items.append(product)
        except:
            pass

    return filter_items


def get_statistics(items: list,  key: str):
    stat = dict()
    stat['max'] = 0
    stat['min'] = 0
    stat['avg'] = 0

    sum_bonus = 0.0
    for product in items:
        stat['max'] = max(float(stat['max']), float(product[key]))
        stat['min'] = min(float(stat['min']), float(product[key]))
        sum_bonus += float(product[key])

    stat['avg'] = sum_bonus / len(items)

    return stat

def frequency_label(items: list, label):
    counter = dict()

    for product in items:
        try:
            value = counter.setdefault(product[label], 0)
            if value >= 0:
                value += 1
                counter.update({product[label]: value})
        except:
            pass

    counter = dict(sorted(counter.items(), key=lambda item: -item[1]))
    return counter