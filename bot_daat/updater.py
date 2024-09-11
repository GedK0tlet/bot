import asyncio
import aiohttp
from datetime import datetime
import time
import os.path

year = datetime.today().strftime("%Y")
defoult_url = "https://cbr.ru/scripts/XML_daily.asp?date_req="

month_day = {
    "01": 31,
    "02": 29,
    "03": 31,
    "04": 30,
    "05": 31,
    "06": 30,
    "07": 31,
    "08": 31,
    "09": 30,
    "10": 31,
    "11": 30,
    "12": 31,
}

def days(count):
    array = []
    day = ""
    for i in range(1, count+1):
        if len(str(i)) == 1:
            day = f"0{i}"
            array.append(day)
        elif len(str(i)) == 2:
            day = f"{i}"
            array.append(day)
    return array
    # return [i for i in range(1, count+1)]


def verifly(months: str):
    res = months.split(",")
    listik = []
    for m in res:
        listik.append([days(month_day[m]), m])
    
    return listik

def create_urls(listik):
    array = []
    for month in listik:
        for day in month[0]:
            array.append(f"{day}/{month[1]}/{year}")
    
    return array, listik

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def update(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, f"{defoult_url}{url}") for url in urls]
        response = await asyncio.gather(*tasks)
    
        return response
    
def create_files(list_data, date):
    for i in range(len(list_data)):
        # if not os.path.exists(f"course/{date[0][0][i]}:{date[0][1]}:{year}.txt")
        file = open(f"course/{date[0][0][i]}:{date[0][1]}:{year}.txt", "w+")
        file.write(list_data[i])
        file.close()


async def updater_m(months):
    a, m = create_urls(verifly(months))
    task = asyncio.create_task(update(a))
    res = await task
    create_files(res, m)
    # return res, m


# st = time.time()
# res, m = updater_m("08")
# create_files(res, m)
# end = time.time()
# print(end-st)