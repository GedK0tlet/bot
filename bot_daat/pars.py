import requests
from bs4 import BeautifulSoup
import time

backs = ['доллар', 'долларов', 'доллара', 'дол', 'доллары']
evro = ['евро', 'еврик', 'евр']
bel_rub = ['бел. руб', 'бел', 'бел рубли', 'белорусские рубли', ' бел.', 'бел. рубли']
lir = ['лир', 'лира', 'лиры', 'лиров', 'лирки', 'лирольки', 'турецкие лиры']
rub = ['рубли', 'рубля', 'рубль', 'рублей', 'руб', 'рубчиков']
grivn = ['гривн', 'гривна', 'грн', 'гривны', 'гривнята', 'грн.']

def course(valute_from: str, date: str):
    response = ""
    d = date.split('.')
    file_name = f"{d[0]}:{d[1]}:{d[2]}"

    file = open(f"course/{file_name[1:]}.txt", "r")
    response = file.read()
    file.close()

    xml = BeautifulSoup(response, 'xml')
    valute = ""
    val_name = valute_from.lower().replace(" ", "")
    if val_name in backs:
        valute = "USD"
    elif val_name in bel_rub:
        valute = "BYN"
    elif val_name in grivn:
        valute = "UAH"
    elif val_name in lir:
        valute = "TRY"
    elif val_name in evro:
        valute = "EUR"
    elif val_name in rub:
        return ("1")
    
    res = xml.find(string=valute).find_next('VunitRate').text.replace(",", ".")
 
    return res
