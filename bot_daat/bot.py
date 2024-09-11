import asyncio
# import requests
import sqlite3
bot_api = "7116558072:AAGimSr8PBVo-cfi5Ji2d2VtqGVby05Y4DQ"
from aiogram import Bot, types, Dispatcher
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram import F
from aiogram.fsm.context import FSMContext
import requests
from aiogram.filters.command import Command
from aiogram.types import ContentType
import os
from random import randint
from aiogram.types.input_file import FSInputFile
from sql import wrote_in_db
from save_csv import setup_data_csv_result, all_data
import time
from updater import updater_m, create_files

bot = Bot(token=bot_api)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text_hello = """
    /start - вызовет это же сообщение
    /document_result - покажет документ с расходами (финальная таблица)
    /document_stat - покажет документ с расходами (подробно)
    /delete <id> - удалить строку по ее номеру(номер(id) указан в document_stat в колонке id, треугольные ковычки указывать не нужно)
    Для работы этого бота, достаточно отправлять фотографию с подписью необходимого действия. К примеру для записи зарплаты, необходимо сделать следующий формат сообщения:
    -----------
    *Фотогрфия* (опционально)
    Расход(ы) (это ключевое слово и оно должно быть первым ОБЯЗАТЕЛЬНО)
    С чьей карты были расходы (Имя должно быть уникальным для каждого плательщика)
    Тема - сумма - валюта - дата
    ....
    Тема - сумма - валюта - дата
    P.S. - на данный момент бот понимает валюты в такой форме записи:
    доллар | долларов | доллара
    бел. руб
    гривн | гривна 
    лир | лира
    евро 
    рублей | рубля | рубль
    -----------
    *Фотогрфия*
    Расходы
    Илья
    Шарики - 1000 - рублей - 20.03.2024
    Цветы - 750 - лир - 25.03.2024
    Билеты на самолет - 2000 - долларов - 21.06.2024
    """
    await message.answer(text_hello)

@dp.message(Command("document_stat"))
async def doc_stat(message: types.Message,  command: CommandObject):
    month_m = ""
    if command.args is None:
        await message.answer(
            "Ошибка: не переданы аргументы"
        )
        return
    try:
        month_m = command.args.split(" ", maxsplit=1)[0]
        try:
            print("stststs")
            all_data(month_m)
            print("stat")
            await message.answer("Собираю документ...")
            time.sleep(3)
            document = FSInputFile("all_data.csv")
            await bot.send_document(message.chat.id, document)
        except Exception:
            await message.answer("Что-то пошло не так :/")
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/document_stat <month>"
        )

#17192 +
@dp.message(Command("document_result"))
async def doc_res(message: types.Message, command: CommandObject):
    month_m = ""
    if command.args is None:
        await message.answer(
            "Ошибка: не переданы аргументы"
        )
        return
    try:
        month_m = command.args.split(" ", maxsplit=1)[0]
        try:
            await message.answer("Собираю документ...")
            setup_data_csv_result(month_m)
            document = FSInputFile("data.csv")
            await bot.send_document(message.chat.id, document)
        except Exception:
            await message.answer("Что-то пошло не так :/")
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/document_result <month>"
        )

@dp.message(Command("new_table"))
async def new_table(message: types.Message, command: CommandObject):
    new_table = ""
    new_table = command.args.split(" ", maxsplit=1)
    with open("month.txt", "w") as f:
        f.write(new_table[0])
    await message.answer(f"была создана таблица под идентификатором {new_table[0]}")


@dp.message(Command("delete"))
async def delete_by_id(message: types.Message, command: CommandObject):
    id_row = ""
    if command.args is None:
        await message.answer(
            "Ошибка: не переданы аргументы"
        )
        return
    try:
        id_row = command.args.split(" ", maxsplit=1)
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/delete <id>"
        )
    try:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM DataS WHERE id=?", (id_row[0],))
        connection.commit()
        connection.close()
        await message.answer("Удаление прошло успешно")
    except Exception:
        await message.answer("Что-то пошло не так, возможно объект с этим номером уже удален")
        
@dp.message(Command("update_data"))
async def update_data(message: types.Message, command: CommandObject):
    month_m = ""
    if command.args is None:
        await message.answer(
            "Ошибка: не переданы аргументы"
        )
        return
    try:
        month_m = command.args.split(" ", maxsplit=1)[0]
        try:
            await message.answer("Приступаю к обновлению")
            await updater_m(month_m)
            await message.answer("обновление выполнено")
        except Exception:
            await message.answer("Во время обновления выпала ошибка")
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/document_result <month>"
        )



@dp.message(F.content_type == ContentType.PHOTO)
async def rashod(message: types.Message):
    photo_info = message.photo[-1] 
    photo_file = await bot.get_file(photo_info.file_id) 
    photo_url = f'https://api.telegram.org/file/bot{bot_api}/{photo_file.file_path}' 

    # await message.answer(f"answer - {title}\nphoto - {photos[0]}\nlink - {photo_url}")

    img_data = requests.get(photo_url).content
    num = randint(1,99999999)
    with open(f'images/img{num}.jpg', 'wb') as handler:
        handler.write(img_data)

    text_msg = message.caption
    try:
        path = f"http://92.63.100.11:7373/img{num}"
    except Exception:
        path = "-"
    
    ar = []
    ar = text_msg.split()
    if ar[0].lower() == "расходы" or ar[0].lower() == "расход" or ar[0].lower() == "траты":
        ar = text_msg.split("\n")
        items_pay = []
        for line in ar:
            items_pay.append(line.split("-"))
        for item in items_pay:
            if len(item) > 1:
                # write_in_csv(ar[1], item[0], item[1], item[2], item[3], path)
                wrote_in_db(ar[1], item[0], item[1], item[2], path, item[3])

@dp.message(F.text)
async def rashod_text(message: types.Message):
    text_msg = message.text
    path = "-"
    
    ar = []
    ar = text_msg.split()
    if ar[0].lower() == "расходы" or ar[0].lower() == "расход" or ar[0].lower() == "траты":
        ar = text_msg.split("\n")
        items_pay = []
        for line in ar:
            items_pay.append(line.split("-"))
        for item in items_pay:
            if len(item) > 1:
                wrote_in_db(ar[1], item[0], item[1], item[2], path, item[3])

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
