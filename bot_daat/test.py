# import requests
# from bs4 import BeautifulSoup
# import time

# # url = 'https://Your-url'
# headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

# # response= requests.get(url.strip(), headers=headers, timeout=10)

# data_test = {'valute': 'доллар', 'date':'02:09:2024'}

# def course(valute_from: str, date: str):
#     print(date)
#     response = ""
#     # if valute_from.lower().replace(" ", "") != "рублей" or valute_from.lower().replace(" ", "") != "рубля" or valute_from.lower().replace(" ", "") != "рубль":
#     #     # response = requests.get(f'https://cbr.ru/scripts/XML_daily.asp?date_req={date}')
#     #     url = "https://cbr.ru/scripts/XML_daily.asp?date_req={date}"
#     #     response= requests.get(url.strip(), headers=headers, timeout=10)
#     with open(f"course/{date}.txt", "r") as f:
#         response = f.read()


#     xml = BeautifulSoup(response, 'xml')
#     valute = ""

#     if valute_from.lower().replace(" ", "") == "доллар" or valute_from.lower().replace(" ", "") == "долларов" or valute_from.lower().replace(" ", "") == "доллара":
#         valute = "USD"
#     elif valute_from.lower().replace(" ", "") == "бел. руб":
#         valute = "BYN"
#     elif valute_from.lower().replace(" ", "") == "гривн" or valute_from.lower().replace(" ", "") == "гривна":
#         valute = "UAH"
#     elif valute_from.lower().replace(" ", "") == "лир" or valute_from.lower().replace(" ", "") == "лира":
#         valute = "TRY"
#     elif valute_from.lower().replace(" ", "") == "евро":
#         valute = "EUR"
#     elif valute_from.lower().replace(" ", "") == "рублей"  or valute_from.lower().replace(" ", "") == "рубля" or valute_from.lower().replace(" ", "") == "рубль":
#         return ("1")
    
#     res = xml.find(string=valute).find_next('VunitRate').text.replace(",", ".")
 
#     return res

# start = time.time()
# print(course(data_test['valute'], data_test["date"]))
# end = time.time()

# print(end - start)

s = []
card_payer = ['Шарики - 100 - доллар - 08.08.2024', 'Кружки - 200 - евро - 01.09.2024']
data = [{'id': 8, 'username': 'Шарики - 100 - доллар - 08.08.2024', 'theme': 'Шарики ', 'many_money': ' 100 ', 'valute': ' доллар ', 'path': '-', 'date': ' 08.08.2024', 'month': 'asd'}, {'id': 9, 'username': 'Кружки - 200 - евро - 01.09.2024', 'theme': 'Кружки ', 'many_money': ' 200 ', 'valute': ' евро ', 'path': '-', 'date': ' 01.09.2024', 'month': 'asd'}]

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


backs = ['доллар', 'долларов', 'дол', 'долл', 'бакс', 'баксов']
evro = ['евро', 'еврик', 'евр']
bel_rub = ['бел. руб', 'белорусские рубли', 'белруб', 'бел руб']
lir = ['лир', 'лира', 'лиры', 'лиров', 'лирки', 'лирольки']
rub = ['рубли', 'рубля', 'рубль', 'рублей', 'руб', 'рубчиков']
grivn = ['гривн', 'гривна', 'гривен']
for payer in card_payer:
    array_valute_person = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    for item in data:
        valute =  item["valute"].lower().replace(" ", "")
        if valute in backs:
             array_valute_person[0] += float(item['many_money'])
        elif valute in evro:
             array_valute_person[1] += float(item['many_money'])
        elif valute in bel_rub:
             array_valute_person[2] += float(item['many_money'])
        elif valute in lir:
             array_valute_person[3] += float(item['many_money'])
        elif valute in grivn:
             array_valute_person[4] += float(item['many_money'])
        elif valute in rub:
             array_valute_person[5] += float(item['many_money'])
        else:
             print(f"not found {valute}")
    s.append([payer, array_valute_person]) 

print(s)