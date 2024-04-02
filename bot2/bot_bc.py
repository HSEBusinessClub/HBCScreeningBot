from aiogram import Bot, Dispatcher, executor, types
import os

API_TOKEN = '7187262577:AAGy6fTjGk2fZBMQDkeKboUBWgFuurQi54s'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Проблема с ботом", "Что такое HSE Business Club", "Открытая и закрытая часть",
               "Вакансии в департаментах", "Пройти первый этап отбора",
               "Пройти второй этап отбора", "Записаться на интервью"]
    keyboard.add(*buttons)
    await message.answer("Выберите опцию:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Проблема с ботом")
async def handle_problem(message: types.Message):
    contacts = ["@Username1", "@Username2", "@Username3"]
    contacts_message = "Если у вас есть проблемы с ботом, вы можете обратиться к следующим контактам: " + ", ".join(contacts)
    await message.answer(contacts_message)

@dp.message_handler(lambda message: message.text == "Что такое HSE Business Club")
async def hse_business_club_info(message: types.Message):
    info_text = "Информация о бк"
    photo_path = os.path.join(os.getcwd(), 'bot2/info_images/info_photo.jpg')
    await message.answer_photo(photo=open(photo_path, 'rb'))
    await message.answer(info_text)


@dp.message_handler(lambda message: message.text == "Открытая и закрытая часть")
async def hse_business_club_info(message: types.Message):
    info_text = "Информация об открытой и закрытой частях"
    photo_path = os.path.join(os.getcwd(), 'bot2/info_images/open_closed.jpg')
    await message.answer_photo(photo=open(photo_path, 'rb'))
    await message.answer(info_text)
    
@dp.message_handler(lambda message: message.text == "Вакансии в департаментах")
async def send_vacancies_photos(message: types.Message):
    vacancies_folder_path = os.path.join(os.getcwd(), 'bot2/depart_photos')
    for photo_file in os.listdir(vacancies_folder_path):
        photo_path = os.path.join(vacancies_folder_path, photo_file)
        await message.answer_photo(photo=open(photo_path, 'rb'))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
