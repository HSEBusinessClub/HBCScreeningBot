from aiogram import Bot, Dispatcher, executor, types
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = '7187262577:AAGy6fTjGk2fZBMQDkeKboUBWgFuurQi54s'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class UserSelection(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()
    q7 = State()
    q8 = State()
    q9 = State()
    q10 = State()
    q11 = State()
    q12 = State()
    q13 = State()
    q14 = State()
    q15 = State()

# для обычного пользователя
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Проблема с ботом", "Что такое HSE Business Club", "Открытая и закрытая часть",
               "Вакансии в департаментах", "Пройти первый этап отбора",
               "Пройти второй этап отбора", "Записаться на интервью"]
    keyboard.add(*buttons)
    await message.answer("Выберите опцию:", reply_markup=keyboard)

#Проблема с ботом
@dp.message_handler(lambda message: message.text == "Проблема с ботом")
async def handle_problem(message: types.Message):
    contacts = ["@Username1", "@Username2", "@Username3"]
    contacts_message = "Если у вас есть проблемы с ботом, вы можете обратиться к следующим контактам: " + ", ".join(contacts)
    await message.answer(contacts_message)

#Что такое HSE Business Club"
@dp.message_handler(lambda message: message.text == "Что такое HSE Business Club")
async def hse_business_club_info(message: types.Message):
    info_text = "Информация о бк"
    photo_path = os.path.join(os.getcwd(), 'bot2/info_images/info_photo.jpg')
    await message.answer_photo(photo=open(photo_path, 'rb'))
    await message.answer(info_text)

#Открытая и закрытая часть
@dp.message_handler(lambda message: message.text == "Открытая и закрытая часть")
async def hse_business_club_info(message: types.Message):
    info_text = "Информация об открытой и закрытой частях"
    photo_path = os.path.join(os.getcwd(), 'bot2/info_images/open_closed.jpg')
    await message.answer_photo(photo=open(photo_path, 'rb'))
    await message.answer(info_text)

#Вакансии в департаментах
@dp.message_handler(lambda message: message.text == "Вакансии в департаментах")
async def show_departments(message: types.Message):
    departments = ["Design", "Event&Project", "SMM", "Production", "HR", "Special", "IT"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for department in departments:
        keyboard.add(department)
    keyboard.add("Назад к главному меню")
    await message.answer("Выберите департамент:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Назад к главному меню", state="*")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await send_welcome(message, state)

departments = {
    "Design": {
        "photo": "bot2/depart_photos/design.jpeg",
        "info": "Информация",
        "vacancies": "Доступные вакансии: "
    },
    "Event&Project": {
        "photo": "bot2/depart_photos/event.jpg",
        "info": "Информация",
        "vacancies": "Доступные вакансии: "
    },
    #add other
}

@dp.message_handler(lambda message: message.text in ["Design", "Event&Project", "SMM", "Production", "HR", "Special", "IT"])  # This handles clicks on department names
async def send_department_info(message: types.Message):
    department_name = message.text
    if department_name in departments:
        department = departments[department_name]
        photo_path = department["photo"]
        info_text = department["info"]
        vacancies_text = department["vacancies"]
        
        await message.answer_photo(photo=open(photo_path, 'rb'))
        await message.answer(f"{info_text}\n{vacancies_text}")



#Пройти первый этап
def generate_control_keyboard(include_back_button=True):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if include_back_button:
        keyboard.add(KeyboardButton("Назад к предудыщему вопросу"))
    keyboard.add(KeyboardButton("Отменить прохождение"))
    return keyboard

def generate_vacancy_keyboard(selected_vacancies=[]):
    vacancies = ["Vacancy 1", "Vacancy 2", "Vacancy 3", "Vacancy 4"]  # Your vacancy list
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for vacancy in vacancies:
        if vacancy not in selected_vacancies:
            keyboard.add(KeyboardButton(vacancy))
    
    keyboard.add(KeyboardButton("Отменить прохождение"))
    
    if selected_vacancies:
        keyboard.add(KeyboardButton("Завершить выбор вакансий"))
    
    return keyboard

@dp.message_handler(Text(equals="Пройти первый этап отбора"))
async def start_first_stage_selection(message: types.Message):
    await UserSelection.q1.set()  
    keyboard = generate_vacancy_keyboard()  
    await message.answer("По очереди выберите вакансии, на которые хотите подать", reply_markup=keyboard)

@dp.message_handler(state=UserSelection.q1)
async def handle_vacancy_selection(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    selected_vacancies = user_data.get("selected_vacancies", [])
    
    if message.text in ["Vacancy 1", "Vacancy 2", "Vacancy 3", "Vacancy 4"]:
        if message.text not in selected_vacancies:
            selected_vacancies.append(message.text)
            await state.update_data(selected_vacancies=selected_vacancies)
    
    if message.text == "Отменить прохождение":
        await state.finish()
        await message.answer("Процесс отбора отменен.", reply_markup=types.ReplyKeyboardRemove())
        await send_welcome(message, state)
        return
    
    if len(selected_vacancies) >= 3 or message.text == "Завершить выбор вакансий":
        await UserSelection.next() 
        await message.answer("Напишите пожалуйста свое ФИО", reply_markup=generate_control_keyboard())
    else:
        keyboard = generate_vacancy_keyboard(selected_vacancies)
        await message.answer("Выберите следующую вакансию или завершите выбор", reply_markup=keyboard)










#admin
class AdminAuth(StatesGroup):
    waiting_for_passcode = State()

class AdminStage(StatesGroup):
    selecting_stage = State()


#Меню админа
async def show_admin_menu(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Первый этап", "Второй этап", "Интервью"]
    keyboard.add(*buttons)
    await message.answer("Админ-меню:", reply_markup=keyboard)

#Вход как админ    
@dp.message_handler(commands=['admin'])
async def admin_login(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Пожалуйста, введите пасскод для аутентификации:")
    await AdminAuth.waiting_for_passcode.set()

@dp.message_handler(state=AdminAuth.waiting_for_passcode, content_types=types.ContentTypes.TEXT)
async def passcode_check(message: types.Message, state: FSMContext):
    if message.text == "123456":
        await state.finish()  
        await message.answer("Вы вошли как админ")
        await show_admin_menu(message)
    elif message.text == "Отменить вход как админ":
        await state.finish()  
        await message.answer("Вход как администратор отменен.", reply_markup=types.ReplyKeyboardRemove())
        await send_welcome(message, state)  
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add("Отменить вход как админ")
        await message.reply("Неверный пасскод. Попробуйте еще раз или отмените вход.", reply_markup=keyboard)

#Меню первого этапа
async def show_admin_stage_selection(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Начать первый этап", "Закрыть первый этап", "Выгрузить ДБ", "Статистика", "Назад"]
    keyboard.add(*buttons)
    await message.answer("Выберите действие для первого этапа:", reply_markup=keyboard)
    await AdminStage.selecting_stage.set()

@dp.message_handler(Text(equals="Первый этап"), state="*")
async def first_stage_options(message: types.Message):
    await show_admin_stage_selection(message)

@dp.message_handler(Text(equals="Назад"), state="*")
async def back_to_admin_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await show_admin_menu(message)

stages_state = {
    'stage_1': 'not_started',
    'stage_2': 'not_started',
    'stage_3': 'not_started',
}

#Начать первый этап
@dp.message_handler(lambda message: message.text == "Начать первый этап")
async def confirm_start_stage_1(message: types.Message, state: FSMContext):
    await AdminStage.selecting_stage.set()
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Да, начать", callback_data="confirm_start_stage_1"),
        InlineKeyboardButton("Нет, вернуться обратно", callback_data="cancel_start_stage_1")
    )
    await message.answer("Вы уверенны что хотите начать первый этап?", reply_markup=keyboard)

@dp.callback_query_handler(text="confirm_start_stage_1", state=AdminStage.selecting_stage)
async def start_stage_1(callback_query: types.CallbackQuery, state: FSMContext):
    if stages_state['stage_2'] != 'active' and stages_state['stage_3'] != 'active':
        stages_state['stage_1'] = 'active'
        await callback_query.message.answer("Первый этап начат.")
    else:
        await callback_query.message.answer("Нельзя начать первый этап, пока другие этапы активны или не закрыты.")
    await callback_query.answer()
    await state.finish()

@dp.callback_query_handler(text="cancel_start_stage_1", state=AdminStage.selecting_stage)
async def cancel_start_stage_1(callback_query: types.CallbackQuery, state: FSMContext):
    await show_admin_stage_selection(callback_query.message)
    await callback_query.answer()
    await state.finish()

# Закрыть первый этап 
@dp.message_handler(lambda message: message.text == "Закрыть первый этап")
async def confirm_close_stage_1(message: types.Message, state: FSMContext):
    if stages_state['stage_1'] == 'active':
        await AdminStage.selecting_stage.set() 
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("Да, закрыть", callback_data="confirm_close_stage_1"),
            InlineKeyboardButton("Нет, вернуться обратно", callback_data="cancel_close_stage_1")
        )
        await message.answer("Вы уверены, что хотите закрыть первый этап?", reply_markup=keyboard)
    else:
        await message.answer("Первый этап не активен, поэтому его нельзя закрыть.")

@dp.callback_query_handler(text="confirm_close_stage_1", state=AdminStage.selecting_stage)
async def close_stage_1(callback_query: types.CallbackQuery, state: FSMContext):
    stages_state['stage_1'] = 'closed'
    await callback_query.message.answer("Первый этап успешно закрыт.")
    await callback_query.answer()
    await state.finish()

@dp.callback_query_handler(text="cancel_close_stage_1", state=AdminStage.selecting_stage)
async def cancel_close_stage_1(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Закрытие первого этапа отменено.")
    await callback_query.answer()
    await state.finish()  








# Выйти из режима админ
@dp.message_handler(commands=['back'])
async def back_to_main(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Вы вышли из режима администратора.")
    await send_welcome(message, state)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
