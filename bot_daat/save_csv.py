from csv import DictWriter
from pars import course
from sql import from_db_take


backs = ['доллар', 'долларов', 'доллара', 'дол', 'доллары']
evro = ['евро', 'еврик', 'евр']
bel_rub = ['бел. руб', 'бел', 'бел рубли', 'белорусские рубли', ' бел.', 'бел. рубли']
lir = ['лир', 'лира', 'лиры', 'лиров', 'лирки', 'лирольки', 'турецкие лиры']
rub = ['рубли', 'рубля', 'рубль', 'рублей', 'руб', 'рубчиков']
grivn = ['гривн', 'гривна', 'грн', 'гривны', 'гривнята', 'грн.']

def setup_data_csv_result(month: str):
    data = from_db_take(month)
    card_payer = []
    many_money: float = 0
    result: float = 0
    array_valute_person = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    s = []

    for item in data:
        if not item["username"] in card_payer:
            card_payer.append(item["username"])
        try:
            many_money = float(item["many_money"].replace(".", ""))
            many_money = float(item["many_money"].replace(".", ""))
            many_money = float(item["many_money"].replace(",", ""))
            many_money = float(item["many_money"].replace(",", ""))
        except Exception:
            many_money= float(item["many_money"])
        
        koef = float(course(item["valute"], item["date"]))
        result += (float(many_money) * koef)
    
    for payer in card_payer:
        array_valute_person = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for item in data:
            valute = item["valute"].lower().replace(" ", "")
            if item["username"] == payer:
                if valute in backs:
                    array_valute_person[0] += float(item['many_money'])
                elif valute in bel_rub:
                    array_valute_person[1] += float(item['many_money'])
                elif valute in grivn:
                    array_valute_person[2] += float(item['many_money'])
                elif valute in lir:
                    array_valute_person[3] += float(item['many_money'])
                elif valute in evro:
                    array_valute_person[4] += float(item['many_money'])
                elif valute in rub:
                    array_valute_person[5] += float(item['many_money'])

        s.append([payer, array_valute_person])      
    names = ["Кто", "Доллары", "Бел. Рубли", "Гривны", "Лиры", "Евро", "Рубли", "Всего"]

    with open("data.csv", mode="w", encoding='utf-8') as w_file:
        dictwriter_object = DictWriter(w_file, fieldnames=names)
        dict_info_first = {
                "Кто": f"Кто",
                "Доллары": f"Доллары",
                "Бел. Рубли": f"Бел. Рубли",
                "Гривны": f"Гривны",
                "Лиры": f"Лиры",
                "Евро": f"Евро",
                "Рубли": f"Рубли",
            }
        dictwriter_object.writerow(dict_info_first)
        print("-------s--------")
        print(s)
        print("-------s--------")
        for item in s:
            dict_info = {
                "Кто": f"{item[0]}",
                "Доллары": f"{item[1][0]}",
                "Бел. Рубли": f"{item[1][1]}",
                "Гривны": f"{item[1][2]}",
                "Лиры": f"{item[1][3]}",
                "Евро": f"{item[1][4]}",
                "Рубли": f"{item[1][5]}",
            }

            dictwriter_object.writerow(dict_info)
        dictwriter_object.writerow({
                "Всего": f"Итог: {result} руб."
            })
        w_file.close()

def all_data( month: str):
    print("all_data")
    data = from_db_take(month)
    print(data)
    print("all_data")
    names = ["id", "Кто", "На что", "Сколько", "Валюта", "Адрес скрина", "Дата"]
    with open("all_data.csv", mode="w", encoding='utf-8') as w_file:
        dict_info = {
                "id": f"id",
                "Кто": f"Кто",
                "На что": f"На что",
                "Сколько": f"Сколько",
                "Валюта": f"Валюта",
                "Адрес скрина": f"Ссылка на скрин оплаты",
                "Дата": f"Дата",
            }
        
        dictwriter_object = DictWriter(w_file, fieldnames=names)
        dictwriter_object.writerow(dict_info)

        for item in data:
            dict_info = {
                "id": f"{item['id']}",
                "Кто": f"{item['username']}",
                "На что": f"{item['theme']}",
                "Сколько": f"{item['many_money']}",
                "Валюта": f"{item['valute']}",
                "Адрес скрина": f"{item['path']}",
                "Дата": f"{item['date']}",
            }
            dictwriter_object.writerow(dict_info)
        w_file.close()