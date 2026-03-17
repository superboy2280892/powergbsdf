import asyncio
import json
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# --- НАСТРОЙКИ ---
API_TOKEN = '8600981350:AAGf-8qD4qprbjhalDdUnzAstADgKVBZ7KQ'
DB_FILE = 'users_data.json'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- ЛОГИКА БАЗЫ ДАННЫХ (ФАЙЛ) ---
def load_passed_users():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                return set(json.load(f))
        except: return set()
    return set()

def save_passed_user(user_id):
    passed_users = load_passed_users()
    passed_users.add(user_id)
    with open(DB_FILE, 'w') as f:
        json.dump(list(passed_users), f)

passed_users_cache = load_passed_users()

# --- СОСТОЯНИЯ ТЕСТА ---
class Quiz(StatesGroup):
    q1, q2, q3 = State(), State(), State()

# --- КЛАВИАТУРЫ ---

def get_main_keyboard(user_id):
    builder = InlineKeyboardBuilder()
    is_passed = user_id in passed_users_cache
    
    quiz_text = "🚀 Пройти тест заново" if is_passed else "🚀 Пройти тест: ИП или Самозанятость?"
    builder.button(text=quiz_text, callback_data="start_quiz")
    
    if is_passed:
        builder.button(text="🏢 Раздел ИП", callback_data="ip_menu")
        builder.button(text="👤 Раздел Самозанятость", callback_data="samozan_menu")
    
    builder.button(text="ℹ️ Инфо", callback_data="info")
    builder.adjust(1) 
    return builder.as_markup()

def get_quiz_answers():
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Да", callback_data="quiz_yes")
    builder.button(text="❌ Нет", callback_data="quiz_no")
    builder.adjust(2)
    return builder.as_markup()

def get_ip_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Soon...", callback_data="ip_how")
    builder.button(text="Soon...", callback_data="ip_tax")
    builder.button(text="⬅️ В главное меню", callback_data="back_to_main")
    builder.adjust(1)
    return builder.as_markup()

def get_samozan_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Soon...", callback_data="samozan_how")
    builder.button(text="Soon...", callback_data="samozan_tax")
    builder.button(text="⬅️ В главное меню", callback_data="back_to_main")
    builder.adjust(1)
    return builder.as_markup()

# --- ОБРАБОТЧИКИ ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    
    if user_id in passed_users_cache:
        text = (
            f"С возвращением, {message.from_user.first_name}! 👋\n\n"
            "Все разделы разблокированы и доступны в меню ниже."
        )
    else:
        text = (
            f"Здравствуйте, {message.from_user.first_name}! 👋\n\n"
            "Пройдите короткий тест, чтобы открыть все функции бота и подобрать налоговый режим."
        )
    
    await message.answer(text, reply_markup=get_main_keyboard(user_id))


@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Главное меню:", 
        reply_markup=get_main_keyboard(callback.from_user.id)
    )
    await callback.answer()

@dp.callback_query(F.data == "info")
async def process_info(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="📂 GitHub", url="https://github.com")
    builder.button(text="⬅️ Назад", callback_data="back_to_main")
    builder.adjust(1)
    await callback.message.edit_text("Бот создан Моисеевой Екатериной. 🚀", reply_markup=builder.as_markup())
    await callback.answer()

# --- ЛОГИКА ТЕСТА ---

@dp.callback_query(F.data == "start_quiz")
async def start_quiz(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("1. Доход больше 2.4 млн рублей в год?", reply_markup=get_quiz_answers())
    await state.set_state(Quiz.q1)
    await callback.answer()

@dp.callback_query(Quiz.q1)
async def q1(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(q1=callback.data)
    await callback.message.edit_text("2. Планируете нанимать сотрудников?", reply_markup=get_quiz_answers())
    await state.set_state(Quiz.q2)
    await callback.answer()

@dp.callback_query(Quiz.q2)
async def q2(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(q2=callback.data)
    await callback.message.edit_text("3. Будете перепродавать чужие товары?", reply_markup=get_quiz_answers())
    await state.set_state(Quiz.q3)
    await callback.answer()

@dp.callback_query(Quiz.q3)
async def q3_final(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    
    save_passed_user(user_id)
    passed_users_cache.add(user_id)

    res = "⚖️ ИП" if "quiz_yes" in [data.get("q1"), data.get("q2"), callback.data] else "✅ Самозанятость"
    
    await callback.message.edit_text(
        f"Ваш результат: **{res}**\n\nРазделы разблокированы!",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard(user_id)
    )
    await state.clear()
    await callback.answer()

# --- КАТЕГОРИИ ---
@dp.callback_query(F.data == "ip_menu")
async def ip_menu(callback: types.CallbackQuery):
    await callback.message.edit_text("Раздел ИП:", reply_markup=get_ip_keyboard())
    await callback.answer()

@dp.callback_query(F.data == "samozan_menu")
async def samozan_menu(callback: types.CallbackQuery):
    await callback.message.edit_text("Раздел Самозанятость:", reply_markup=get_samozan_keyboard())
    await callback.answer()

@dp.callback_query(F.data.in_({"ip_how", "ip_tax", "samozan_how", "samozan_tax"}))
async def soon(callback: types.CallbackQuery):
    await callback.answer("🚧 Раздел в разработке!", show_alert=True)

async def main():
    print("Бот запущен !")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
