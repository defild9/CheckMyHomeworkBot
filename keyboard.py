from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

#Menu
button_add_homework = KeyboardButton("✅Додати завдання")
button_show_homework = KeyboardButton("📜Показати завдання")
manu = ReplyKeyboardMarkup(resize_keyboard=True).add(button_add_homework, button_show_homework)
