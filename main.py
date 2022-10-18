import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import keyboard as kb
import database as db


class UserData(StatesGroup):
    task = State()
    subject = State()

class ShowData(StatesGroup):
    show_data_by_subject = State()

class DeleteData(StatesGroup):
    subject_delete = State()
    task_delete = State()

Token = "5503220888:AAFafBXfb72XjCxnGLhhr9HDVAId3C3hhgY"
storage = MemoryStorage()
bot = Bot(token=Token)
dp = Dispatcher(bot, storage = storage)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    id = message.from_user.id
    await  message.answer(f"Привіт, {message.from_user.full_name}, твій id:{id}", reply_markup= kb.manu)
#Add tasks
@dp.message_handler(lambda message: message.text == "✅Додати завдання", state=None)
async def add_homework(message: types.Message):
    await message.answer(f"Введіть текст:")
    await UserData.task.set()

@dp.message_handler(state=UserData.task)
async def set_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['task'] = message.text
    await message.reply("Введіть предмет:", reply_markup=kb.sub_menu)
    await UserData.next()

@dp.message_handler(state=UserData.subject)
async def set_subject(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['subject'] = message.text
        data['id'] = message.from_user.id
    await message.answer(f"Task:{data['task']}\nSubject:{data['subject']}\nYourId:{data['id']}",reply_markup=kb.manu)
    db.add_task(str(data['id']), str(data['task']), str(data['subject']))
    await state.finish()
#Show task
@dp.message_handler(lambda message: message.text == "📜Показати завдання", state=None)
async def show_tasks(message:types.Message):
    await message.answer(f"Введіть назву предмета з якого хочете отримати завдання:")
    await ShowData.show_data_by_subject.set()

@dp.message_handler(state=ShowData.show_data_by_subject)
async def set_show_task_by_subject(message: types.Message, state:FSMContext):
    async  with state.proxy() as show:
        show['sub_for_show'] = message.text
    await  message.answer(db.show_task(show['sub_for_show']))
    await state.finish()

#delete task
@dp.message_handler(lambda message: message.text == "❌Видалити завдання")
async def delete_task(message:types.Message):
    await message.answer("Введіть назву предмета в якому треба удалити завдання:")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

