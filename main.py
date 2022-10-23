import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import keyboard as kb
import database as db


class UserData(StatesGroup):
    subject = State()
    task = State()
    name = State()

class ShowData(StatesGroup):
    show_data_by_subject = State()

class DeleteData(StatesGroup):
    subject_delete = State()
    task_delete = State()
proxy_url = 'http://proxy.server:3128'
Token = "5503220888:AAFafBXfb72XjCxnGLhhr9HDVAId3C3hhgY"
storage = MemoryStorage()
#bot = Bot(token=Token, proxy=proxy_url)
bot = Bot(token=Token)
dp = Dispatcher(bot, storage = storage)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await  message.answer(f"Привіт!, {message.from_user.full_name}, я бот, який запам'ятає домашнє завдання)"
                          f"\n\n{'<b>'}Примітка:{'</b>'} Видаляти завдання можна ті які ти добавляв, не можна видаляти записи інших, "
                          f"якщо навіть спробуєшь видалити, я нічого не видалю\n\n{'<b>'}P.S: знайшов баг чи маєшь пропозицію як покращити мене "
                          f"пиши:{'</b>'} @defild", parse_mode='HTML', reply_markup= kb.manu)
#Add tasks
@dp.message_handler(lambda message: message.text == "✅Додати завдання", state=None)
async def add_homework(message: types.Message):
    await message.answer(f"Виберіть предмет:", reply_markup=kb.sub_menu)
    await UserData.subject.set()

@dp.message_handler(state=UserData.subject)
async def set_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['subject'] = message.text

    if data['subject'] == "🔙Вихід":
        await message.answer("До зустрічі!!",reply_markup=kb.manu)
        await state.finish()
    else:
        await message.reply("Введіть завдання:")
        await UserData.next()

@dp.message_handler(state=UserData.task)
async def set_subject(message: types.Message, state: FSMContext):
    username = message.from_user.username
    if username == None:
        async with state.proxy() as data:
            data['task'] = message.text
            data['id'] = message.from_user.id
        await message.answer("Введіть своє ім'я:")
        await UserData.next()
    else:
        async with state.proxy() as data:
            data['task'] = message.text
            data['id'] = message.from_user.id
            data['username'] = f'@{message.from_user.username}'
        await message.answer(f"✅{'<b>'}Додано!{'</b>'}\n{'<b>'}Завдання:{data['task']}{'</b>'}\n{'<b>'}Предмет:{data['subject']}{'</b>'}",parse_mode='HTML',
                             reply_markup=kb.manu)
        db.add_task(str(data['id']), str(data['task']), str(data['subject']), str(data['username']))
        await state.finish()

@dp.message_handler(state=UserData.name)
async def set_username(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    await message.answer(f"✅{'<b>'}Додано!{'</b>'}\n{'<b>'}Завдання:{'</b>'} {data['task']}\n{'<b>'}Предмет:{'</b>'} {data['subject']}",parse_mode='HTML',
                         reply_markup=kb.manu)
    db.add_task(str(data['id']), str(data['task']), str(data['subject']), str(data['username']))
    await state.finish()


#Show task
@dp.message_handler(lambda message: message.text == "📜Показати завдання", state=None)
async def show_tasks(message:types.Message):
    await message.answer(f"Виберіть назву предмета з якого хочете отримати завдання:",reply_markup=kb.sub_menu)
    await ShowData.show_data_by_subject.set()

@dp.message_handler(state=ShowData.show_data_by_subject)
async def set_show_task_by_subject(message: types.Message, state:FSMContext):
    async  with state.proxy() as show:
        show['sub_for_show'] = message.text

    if show['sub_for_show'] == "🔙Вихід":
        await message.answer("До зустрічі!!", reply_markup=kb.manu)
        await state.finish()
    else:
        await  message.answer(db.show_task(show['sub_for_show']),reply_markup=kb.manu)
        await state.finish()

#delete task
@dp.message_handler(lambda message: message.text == "❌Видалити завдання", state=None)
async def delete_task(message:types.Message):
    await message.answer("Виберіть назву предмета в якому треба удалити завдання:",reply_markup=kb.sub_menu)
    await DeleteData.subject_delete.set()
@dp.message_handler(state=DeleteData.subject_delete)
async def set_delete_sub(message: types.Message,state:FSMContext):
    async  with state.proxy() as delete:
        delete['delete_sub'] = message.text

    if delete['delete_sub'] == "🔙Вихід":
        await message.answer("До зустрічі!!", reply_markup=kb.manu)
        await state.finish()
    else:
        await message.answer((db.show_task(delete['delete_sub'])))
        await message.answer("Введіть повністю завдання яке треба видалити:")
        await DeleteData.next()
@dp.message_handler(state=DeleteData.task_delete)
async def set_delete_task(message: types.Message, state:FSMContext):
    async with state.proxy() as delete:
        delete['delete_task'] = message.text
        delete['user_id'] = message.from_user.id
    db.delete_task(str(delete['delete_task']), str(delete['delete_sub']), delete['user_id'])
    await  message.answer(f"Перевірте оновлений список завдання:")
    await message.answer((db.show_task(delete['delete_sub'])), reply_markup=kb.manu)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

