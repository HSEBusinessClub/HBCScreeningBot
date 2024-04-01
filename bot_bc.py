from aiogram import Bot, Dispatcher, executor, types

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

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
