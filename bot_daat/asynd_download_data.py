import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup

# Функция для асинхронного запроса к URL
async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

# Массив с URL-адресами для запросов
urls = ['https://cbr.ru/scripts/XML_daily.asp?date_req=1/9/2010', 'https://cbr.ru/scripts/XML_daily.asp?date_req=10/10/2012', 'https://cbr.ru/scripts/XML_daily.asp?date_req=10/10/2013', 'https://cbr.ru/scripts/XML_daily.asp?date_req=14/01/2016']

async def main(valute_from: str):
    # Создание сессии для асинхронных HTTP-запросов
    async with aiohttp.ClientSession() as session:
        # Асинхронная функция для обработки всех URL-адресов
        tasks = [fetch_url(session, url) for url in urls]
        # Запуск всех задач одновременно
        responses = await asyncio.gather( * tasks)
    
    print(type(response))

    # Вывод результатов запросов
    for response in responses:
        xml = BeautifulSoup(response, 'xml')
        valute = ""

        if valute_from.lower().replace(" ", "") == "доллар" or valute_from.lower().replace(" ", "") == "долларов" or valute_from.lower().replace(" ", "") == "доллара":
            valute = "USD"
        elif valute_from.lower().replace(" ", "") == "бел. руб":
            valute = "BYN"
        elif valute_from.lower().replace(" ", "") == "гривн" or valute_from.lower().replace(" ", "") == "гривна":
            valute = "UAH"
        elif valute_from.lower().replace(" ", "") == "лир" or valute_from.lower().replace(" ", "") == "лира":
            valute = "TRY"
        elif valute_from.lower().replace(" ", "") == "евро":
            valute = "EUR"
        elif valute_from.lower().replace(" ", "") == "рублей"  or valute_from.lower().replace(" ", "") == "рубля" or valute_from.lower().replace(" ", "") == "рубль":
            return ("1")
        
        res = xml.find(string=valute).find_next('VunitRate').text.replace(",", ".")
 
    return res



if __name__ == "__main__":
    st = time.time()
    asyncio.run(main("доллар"))
    en = time.time()
    print(en - st)